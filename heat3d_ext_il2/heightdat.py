"""Decoder for IL-2 Sturmovik terrain height maps (Great Battles and IL-2 Series: Korea).

Reads the payload of ``height.dat`` (full-resolution terrain) and
``distlod/distlod.dat`` (distant-LOD terrain) from the game's ``Maps*.gtp``
archives; the same codec is used by the water-level map (height_w.dat, seen
in the Korea install).  The payload is the ``size`` bytes that follow the 32-byte STRMFILE
header of the archive entry (offset+32 .. offset+32+size).  The format was
worked out from the data files alone and checked bit-exactly against the
uncompressed ``distlod.raw`` files that ship next to some distlod.dat files.

File layout (little endian)
---------------------------
    u32 width, u32 height          samples (columns, rows)
    u32 sectorsX, u32 sectorsY     sector grid, sectorsX*sectorSize >= width
    u32 sectorSize                 32, 64 or 128 samples per sector side
    f32 cellSize                   metres between samples (50, 800, 12.5 ...;
                                   some distlod files carry a wrong value)
    u32 offset[sectorsX*sectorsY]  byte offset of each sector blob from the
                                   start of the payload, row-major (row of
                                   sectors outer, column inner); sector i ends
                                   where sector i+1 starts
    sector blobs

Sector blob
    u16 count                      number of bytes after this field
    u16 mode                       0x0054 with 32-sectors, 0x0064 with 64,
                                   0x0074 with 128 (Korea):
                                   bits 4..7 = log2(sectorSize),
                                   bits 0..3 = LW, width of a literal's
                                   length field (always 4 so far)
    bitstream, MSB first, zero padded to whole bytes

Bitstream: 1-D DPCM with run-length coding of the sector's samples in raster
order (row by row, left to right; a row's first sample is coded relative to
the previous row's last sample).  Values are 16 bit, coded as signed numbers;
read the result modulo 65536 as uint16.

    PRE     2*(log2(sectorSize)-5) bits: 0 for 32-, 2 for 64-, 4 for
            128-sectors; always zero in every file seen
    LIT     first sample (absolute, int16: 33351 is coded as -32185)
    repeat until sectorSize^2 samples exist:
      '0' LIT           next sample = previous + LIT
      '1' RUN           previous sample repeats RUN times (1..256); unless that
                        fills the sector, a LIT follows: next = previous + LIT
                        (it can be 0, after a run capped at 256)
    LIT = s(1) n(LW bits) m(n+1 bits)    value = -m if s else m
    RUN = k(3 bits) m(k+1 bits)          RUN = m + 1

Heights: metres = raw * heightMul / 256 with heightMul from the map's
height.hini (1.28 -> 5 mm per unit, 25.6 -> 0.1 m per unit).
SeaLevel * heightMul and bounds_level * heightMul in height.hini are in the
same scale.  Samples outside width/height (partial edge sectors) are padding
and are cropped.
"""
import re
import struct

import numpy as np

__all__ = ["read_height_dat", "read_region", "read_sampled", "parse_header", "decode_sector",
           "parse_hini", "to_metres"]


def _strip(payload):
    # accept an archive entry that still has its 32-byte STRMFILE header
    if bytes(payload[:8]) == b"STRMFILE":
        return payload[32:]
    return payload


def parse_header(payload):
    payload = _strip(payload)
    w, h, sx, sy, ss = struct.unpack_from("<5I", payload, 0)
    cell = struct.unpack_from("<f", payload, 20)[0]
    n = sx * sy
    if not (0 < ss <= 1024 and 0 < n < 10 ** 7 and w <= sx * ss and h <= sy * ss):
        raise ValueError("not a height.dat payload")
    offs = np.frombuffer(payload, "<u4", n, 24).astype(np.int64)
    ends = np.append(offs[1:], len(payload))
    return dict(width=w, height=h, sectors_x=sx, sectors_y=sy,
                sector_size=ss, cell_size=cell, offsets=offs, ends=ends)


def _prefix_bits(log2ss):
    # 0 bits for 32-sectors, 2 for 64, 4 for 128 (Korea); always zero so far
    return max(0, 2 * (log2ss - 5))


# ------------------------------------------------------------ pure python path
_BITS = [format(i, "08b") for i in range(256)]


def decode_sector(blob, n=None):
    """Decode one sector blob (starting at its u16 count field).

    Returns (int64 list of n samples in raster order, info dict).  Raises
    ValueError if the bitstream runs out."""
    cnt = blob[0] | (blob[1] << 8)
    lw, l2 = blob[2] & 15, blob[2] >> 4
    if n is None:
        n = 1 << (2 * l2)
    bits = "".join([_BITS[b] for b in blob[4:2 + cnt]])
    nb = len(bits)
    p = _prefix_bits(l2)
    pre = int(bits[:p], 2) if p else 0
    if nb < p + lw + 2:
        raise ValueError("sector bitstream too short")
    # first literal
    c = int(bits[p + 1:p + 1 + lw], 2)
    m = int(bits[p + 1 + lw:p + 2 + lw + c], 2)
    v = -m if bits[p] == "1" else m
    p += 2 + lw + c
    out = [v]
    append = out.append
    extend = out.extend
    i = 1
    while i < n:
        if p >= nb:
            raise ValueError("sector bitstream overrun")
        if bits[p] == "1":
            k = int(bits[p + 1:p + 4], 2)
            z = int(bits[p + 4:p + 5 + k], 2) + 1
            p += 5 + k
            if i + z >= n:
                extend([v] * (n - i))
                i = n
                break
            extend([v] * z)
            i += z
        else:
            p += 1
        c = int(bits[p + 1:p + 1 + lw], 2)
        m = int(bits[p + 1 + lw:p + 2 + lw + c], 2)
        if bits[p] == "1":
            m = -m
        p += 2 + lw + c
        v += m
        append(v)
        i += 1
    if p > nb:
        raise ValueError("sector bitstream overrun")
    return out, dict(prefix=pre, lw=lw, log2ss=l2, bits_left=nb - p)


# ------------------------------------------------------------ numba path
_nb_decode_all = None
try:  # optional accelerator; the module works without it
    import numba as _nb

    @_nb.njit(cache=True)
    def _rd(buf, p, k):
        v = 0
        for _ in range(k):
            v = (v << 1) | ((buf[p >> 3] >> (7 - (p & 7))) & 1)
            p += 1
        return v

    @_nb.njit(cache=True)
    def _nb_decode_all(buf, offs, ss, out, stat):
        # stat[:,0] = error flag, stat[:,1] = prefix, stat[:,2] = bits left
        n = ss * ss
        for si in range(offs.shape[0]):
            o = offs[si]
            cnt = buf[o] | (buf[o + 1] << 8)
            lw = buf[o + 2] & 15
            l2 = buf[o + 2] >> 4
            end = (o + 2 + cnt) * 8
            if end > buf.shape[0] * 8:
                end = buf.shape[0] * 8
            p = (o + 4) * 8
            if l2 > 5:
                stat[si, 1] = _rd(buf, p, 2 * (l2 - 5))
                p += 2 * (l2 - 5)
            bad = 0
            v = 0
            i = 0
            while i < n:
                if p + 1 + lw > end:
                    bad = 1
                    break
                if i > 0:
                    f = (buf[p >> 3] >> (7 - (p & 7))) & 1
                    p += 1
                    if f:
                        k = _rd(buf, p, 3)
                        z = _rd(buf, p + 3, k + 1) + 1
                        p += 4 + k
                        if i + z >= n:
                            for j in range(i, n):
                                out[si, j] = v
                            i = n
                            break
                        for j in range(i, i + z):
                            out[si, j] = v
                        i += z
                s = (buf[p >> 3] >> (7 - (p & 7))) & 1
                c = _rd(buf, p + 1, lw)
                m = _rd(buf, p + 1 + lw, c + 1)
                p += 2 + lw + c
                if s:
                    m = -m
                v = v + m if i > 0 else m
                out[si, i] = v
                i += 1
            if p > end:
                bad = 1
            stat[si, 0] = bad
            stat[si, 2] = end - p
except Exception:  # numba missing or broken
    _nb_decode_all = None


def read_height_dat(payload, height_mul=None, use_numba=True, return_raw=False):
    """Decode a height.dat / distlod.dat payload.

    Returns (array[height, width], info).  The array is float32 raw units
    (0..65535) unless ``height_mul`` (heightMul from height.hini) is given,
    then float32 metres = raw * height_mul / 256.  ``return_raw=True`` gives
    the uint16 raw array instead.  Row 0 is the first row of the file."""
    payload = _strip(bytes(payload))
    hd = parse_header(payload)
    w, h = hd["width"], hd["height"]
    sx, sy, ss = hd["sectors_x"], hd["sectors_y"], hd["sector_size"]
    n = ss * ss
    nsec = sx * sy
    flat = np.zeros((nsec, n), np.int32)
    stat = np.zeros((nsec, 3), np.int64)
    if use_numba and _nb_decode_all is not None:
        _nb_decode_all(np.frombuffer(payload, np.uint8), hd["offsets"], ss, flat, stat)
    else:
        for i in range(nsec):
            try:
                vals, inf = decode_sector(payload[hd["offsets"][i]:hd["ends"][i]], n)
                flat[i] = vals
                stat[i, 1] = inf["prefix"]
                stat[i, 2] = inf["bits_left"]
            except (ValueError, IndexError):
                stat[i, 0] = 1
    raw = (flat & 0xFFFF).astype(np.uint16)
    img = raw.reshape(sy, sx, ss, ss).transpose(0, 2, 1, 3).reshape(sy * ss, sx * ss)[:h, :w]
    info = {k: v for k, v in hd.items() if k not in ("offsets", "ends")}
    info["bad_sectors"] = int(stat[:, 0].sum())
    info["nonzero_prefix_sectors"] = int((stat[:, 1] != 0).sum())
    # a correctly parsed sector leaves at most one byte of zero padding
    info["suspicious_sectors"] = int(((stat[:, 2] < 0) | (stat[:, 2] > 8)).sum())
    if return_raw:
        info["units"] = "raw uint16"
        return np.ascontiguousarray(img), info
    if height_mul is not None:
        info["units"] = "metres"
        info["height_mul"] = height_mul
        return to_metres(img, height_mul), info
    info["units"] = "raw (metres = raw * heightMul / 256)"
    return img.astype(np.float32), info


def read_region(payload, x0, y0, x1, y1, use_numba=True):
    """Decode only the sectors covering samples [y0:y1, x0:x1] (raw uint16).

    Useful for very large maps (Korea: 19968^2) to keep memory low."""
    payload = _strip(payload)
    hd = parse_header(payload)
    w, h, sx, ss = hd["width"], hd["height"], hd["sectors_x"], hd["sector_size"]
    x1, y1 = min(x1, w), min(y1, h)
    c0, c1 = x0 // ss, (x1 - 1) // ss + 1
    r0, r1 = y0 // ss, (y1 - 1) // ss + 1
    idx = np.array([r * sx + c for r in range(r0, r1) for c in range(c0, c1)], np.int64)
    n = ss * ss
    flat = np.zeros((len(idx), n), np.int32)
    stat = np.zeros((len(idx), 3), np.int64)
    if use_numba and _nb_decode_all is not None:
        _nb_decode_all(np.frombuffer(payload, np.uint8), hd["offsets"][idx], ss, flat, stat)
    else:
        for j, i in enumerate(idx):
            flat[j] = decode_sector(payload[hd["offsets"][i]:hd["ends"][i]], n)[0]
    raw = (flat & 0xFFFF).astype(np.uint16)
    big = raw.reshape(r1 - r0, c1 - c0, ss, ss).transpose(0, 2, 1, 3).reshape((r1 - r0) * ss, (c1 - c0) * ss)
    return np.ascontiguousarray(big[y0 - r0 * ss:y1 - r0 * ss, x0 - c0 * ss:x1 - c0 * ss])


def read_sampled(payload, step, use_numba=True):
    """Every `step`-th sample of every `step`-th row (raw uint16), decoded one row of
    sectors at a time, so a map of hundreds of millions of samples (Korea) needs
    the memory of one row of sectors and the result, not of the whole map.
    Also returns the sample indices taken along x and along y."""
    payload = _strip(bytes(payload))
    hd = parse_header(payload)
    w, h, sx, sy, ss = hd["width"], hd["height"], hd["sectors_x"], hd["sectors_y"], hd["sector_size"]
    cols = np.unique(np.r_[np.arange(0, w, step), w - 1])
    rows = np.unique(np.r_[np.arange(0, h, step), h - 1])
    out = np.zeros((len(rows), len(cols)), np.uint16)
    n = ss * ss
    buf = np.frombuffer(payload, np.uint8)
    bad = suspicious = 0
    for sr in range(sy):
        r0, r1 = sr * ss, min((sr + 1) * ss, h)
        take = np.nonzero((rows >= r0) & (rows < r1))[0]
        if not len(take):
            continue
        idx = np.arange(sr * sx, (sr + 1) * sx, dtype=np.int64)
        flat = np.zeros((sx, n), np.int32)
        stat = np.zeros((sx, 3), np.int64)
        if use_numba and _nb_decode_all is not None:
            _nb_decode_all(buf, hd["offsets"][idx], ss, flat, stat)
        else:
            for j, i in enumerate(idx):
                try:
                    vals, inf = decode_sector(payload[hd["offsets"][i]:hd["ends"][i]], n)
                    flat[j] = vals
                    stat[j, 2] = inf["bits_left"]
                except (ValueError, IndexError):
                    stat[j, 0] = 1
        bad += int(stat[:, 0].sum())
        suspicious += int(((stat[:, 2] < 0) | (stat[:, 2] > 8)).sum())
        band = (flat & 0xFFFF).astype(np.uint16).reshape(sx, ss, ss).transpose(1, 0, 2).reshape(ss, sx * ss)
        out[take] = band[rows[take] - r0][:, cols]
    info = {k: v for k, v in hd.items() if k not in ("offsets", "ends")}
    info["bad_sectors"], info["suspicious_sectors"] = bad, suspicious
    return out, cols, rows, info


def iter_bands(payload, use_numba=True):
    """(first row, band) for each row of sectors, raw uint16, cropped to the map: the
    whole map at full resolution, one row of sectors in memory at a time."""
    payload = _strip(bytes(payload))
    hd = parse_header(payload)
    w, h, sx, sy, ss = hd["width"], hd["height"], hd["sectors_x"], hd["sectors_y"], hd["sector_size"]
    n = ss * ss
    buf = np.frombuffer(payload, np.uint8)
    for sr in range(sy):
        r0, r1 = sr * ss, min((sr + 1) * ss, h)
        if r0 >= h:
            break
        idx = np.arange(sr * sx, (sr + 1) * sx, dtype=np.int64)
        flat = np.zeros((sx, n), np.int32)
        stat = np.zeros((sx, 3), np.int64)
        if use_numba and _nb_decode_all is not None:
            _nb_decode_all(buf, hd["offsets"][idx], ss, flat, stat)
        else:
            for j, i in enumerate(idx):
                flat[j] = decode_sector(payload[hd["offsets"][i]:hd["ends"][i]], n)[0]
        band = (flat & 0xFFFF).astype(np.uint16).reshape(sx, ss, ss).transpose(1, 0, 2).reshape(ss, sx * ss)
        yield r0, band[: r1 - r0, :w]


def to_metres(raw, height_mul):
    return raw.astype(np.float32) * np.float32(height_mul / 256.0)


def parse_hini(text):
    """heightMul / SeaLevel / bounds_level from a height.hini text (values as
    written; multiply SeaLevel and bounds_level by heightMul for metres)."""
    out = {}
    for key in ("heightMul", "SeaLevel", "bounds_level"):
        m = re.search(r"^[ \t]*" + key + r"[ \t]*=[ \t]*([-0-9.]+)", text, re.M)
        if m:
            out[key] = float(m.group(1))
    return out


if __name__ == "__main__":
    import sys
    a, info = read_height_dat(open(sys.argv[1], "rb").read(), return_raw=True)
    print(info, int(a.min()), int(a.max()))
