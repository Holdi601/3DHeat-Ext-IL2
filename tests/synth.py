"""Builders for IL-2's formats, to the layouts the readers document, so the tests need no game files."""

from __future__ import annotations

import struct

import numpy as np


class _Bits:
    def __init__(self):
        self.bits: list[str] = []

    def put(self, value: int, width: int):
        if width:
            self.bits.append(format(value, f"0{width}b"))

    def lit(self, value: int, lw: int = 4):
        m = abs(value)
        n = max(m.bit_length() - 1, 0)
        assert n < (1 << lw)
        self.put(1 if value < 0 else 0, 1)
        self.put(n, lw)
        self.put(m, n + 1)

    def run(self, z: int):
        m = z - 1
        k = max(m.bit_length() - 1, 0)
        self.put(k, 3)
        self.put(m, k + 1)

    def bytes(self) -> bytes:
        s = "".join(self.bits)
        s += "0" * (-len(s) % 8)
        return bytes(int(s[i:i + 8], 2) for i in range(0, len(s), 8))


def _signed16(v: int) -> int:
    v &= 0xFFFF
    return v - 0x10000 if v >= 0x8000 else v


def encode_sector(values: np.ndarray, l2: int) -> bytes:
    """One sector: delta literals and runs, as `heightdat.py` decodes them."""
    v = [int(x) for x in values.ravel()]
    n = len(v)
    out = _Bits()
    out.put(0, max(0, 2 * (l2 - 5)))
    out.lit(_signed16(v[0]))
    i, prev = 1, v[0]
    while i < n:
        z = 0
        while i + z < n and v[i + z] == prev and z < 256:
            z += 1
        if z:
            out.put(1, 1)
            out.run(z)
            i += z
            if i >= n:
                break
        else:
            out.put(0, 1)
        out.lit(_signed16(v[i] - prev))
        prev = v[i]
        i += 1
    body = struct.pack("<H", (l2 << 4) | 4) + out.bytes()
    return struct.pack("<H", len(body)) + body


def height_dat(raw: np.ndarray, sector: int = 32, cell: float = 50.0) -> bytes:
    """A whole height.dat payload; edge sectors padded with the edge values."""
    h, w = raw.shape
    sx, sy = -(-w // sector), -(-h // sector)
    padded = np.pad(raw, ((0, sy * sector - h), (0, sx * sector - w)), mode="edge")
    l2 = sector.bit_length() - 1
    blobs = [encode_sector(padded[r * sector:(r + 1) * sector, c * sector:(c + 1) * sector], l2)
             for r in range(sy) for c in range(sx)]
    head = struct.pack("<5If", w, h, sx, sy, sector, cell)
    at = len(head) + 4 * len(blobs)
    offsets = []
    for b in blobs:
        offsets.append(at)
        at += len(b)
    return head + struct.pack(f"<{len(blobs)}I", *offsets) + b"".join(blobs)


def _entry(data: bytes, at: int) -> bytes:
    return b"STRMFILE" + struct.pack("<I", len(data)) + b"\0" * 16 + struct.pack("<I", at + 32) + data


def gtp(files: dict[str, bytes]) -> bytes:
    """A Great Battles archive: S16R, a STRMFAT table of FILE records, then the entries."""
    records = bytearray()
    names = list(files)
    table_len = sum(32 + len(n) + 1 for n in names)
    at = 64 + table_len
    for n in names:
        name = n.encode() + b"\0"
        records += b"FILE" + struct.pack("<7I", 1, at, len(files[n]), 0, 0, len(name), 0) + name
        at += 32 + len(files[n])
    out = b"S16R" + b"\0" * 28 + b"STRMFAT?" + struct.pack("<I", len(records)) + b"\0" * 20 + bytes(records)
    for n in names:
        out += _entry(files[n], len(out))
    return out


def chain(blobs: list[bytes]) -> bytes:
    """A Korea-style archive: entries one after another, no table."""
    out = b""
    for b in blobs:
        out += _entry(b, len(out))
    return out + b"\x13" * 40  # the hashed name block at the end


def hini(height: str, water: str | None, corners: dict[str, tuple[float, float]], mul: float, sea: float) -> bytes:
    lines = [f' height_map="{height}"']
    if water:
        lines.append(f' water_map="{water}"')
    lines += [f" heightMul={mul} //comment", f" SeaLevel={sea}", " limitMaxX=1000", " limitMaxZ=2000"]
    lines += [f" {k}={a}, {b}" for k, (a, b) in corners.items()]
    lines += ["[Distortions]", ' bitmap="x.bmp"']
    return "\r\n".join(lines).encode("cp1251")
