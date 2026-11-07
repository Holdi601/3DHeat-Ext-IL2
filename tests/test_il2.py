"""The IL-2 readers on built files: the height codec, the archives, height.hini, placement and the whole glb."""

from __future__ import annotations

import json
import struct

import numpy as np
import pytest

import synth
from heat3d_ext_il2 import heightdat, korea
from heat3d_ext_il2.gtp import read_table, scan_chain
from heat3d_ext_il2.hini import parse_hini
from heat3d_ext_il2.level import MapSource, build, inverse_tangent, tangent

CORNERS = {"MapNE": (50.45, 31.0), "MapNW": (50.45, 30.0), "MapSW": (50.0, 30.0), "MapSE": (50.0, 31.0)}


def _terrain(h=70, w=90, seed=3) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:h, 0:w]
    raw = 20000 + 3000 * np.sin(x / 9.0) + 2000 * np.cos(y / 7.0) + rng.integers(0, 40, (h, w))
    raw[:, :12] = 9000  # a flat sea strip, long runs
    return raw.astype(np.uint16)


@pytest.mark.parametrize("sector", [32, 64])
def test_codec_round_trip(sector):
    raw = _terrain()
    payload = synth.height_dat(raw, sector)
    got, info = heightdat.read_height_dat(payload, return_raw=True)
    assert np.array_equal(got, raw)
    assert info["bad_sectors"] == 0 and info["suspicious_sectors"] == 0
    py, _ = heightdat.read_height_dat(payload, return_raw=True, use_numba=False)
    assert np.array_equal(py, raw)


def test_codec_wraps_16_bit_and_handles_capped_runs():
    raw = np.full((32, 32), 65000, np.uint16)  # 1024 equal samples: runs capped at 256, then zero literals
    raw[5, 5] = 3  # a jump past half the 16-bit range
    got, _ = heightdat.read_height_dat(synth.height_dat(raw, 32), return_raw=True)
    assert np.array_equal(got, raw)


def test_sampled_and_bands_match_the_full_decode():
    raw = _terrain()
    payload = synth.height_dat(raw, 32)
    sampled, cols, rows, _ = heightdat.read_sampled(payload, 7)
    assert np.array_equal(sampled, raw[np.ix_(rows, cols)])
    assert cols[-1] == raw.shape[1] - 1 and rows[-1] == raw.shape[0] - 1
    bands = np.concatenate([b for _, b in heightdat.iter_bands(payload)])
    assert np.array_equal(bands, raw)


def test_archive_table_and_chain(tmp_path):
    files = {"/graphics/landscape_x/height.hini": b"a=1", "/graphics/landscape_x/height.dat": b"\1\2\3"}
    p = tmp_path / "Maps.gtp"
    p.write_bytes(synth.gtp(files))
    entries = {e.name: e for e in read_table(p)}
    assert set(entries) == set(files)
    assert entries["/graphics/landscape_x/height.dat"].read() == b"\1\2\3"
    c = tmp_path / "Maps1.gtp"
    c.write_bytes(synth.chain([b"one", b"second"]))
    assert read_table(c) == []
    assert [e.read() for e in scan_chain(c)] == [b"one", b"second"]


def test_hini():
    h = parse_hini(synth.hini(r"graphics\LANDSCAPE_X\height.dat", r"graphics\LANDSCAPE_X\height_w.dat", CORNERS, 1.28, -39.0625))
    assert h.path("height_map") == "/graphics/landscape_x/height.dat"
    assert h.number("heightMul") == pytest.approx(1.28) and h.number("SeaLevel") == pytest.approx(-39.0625)
    assert h.corners()["MapSE"] == (50.0, 31.0)
    assert h.get("bitmap") is not None  # later sections parsed, first value kept


def test_tangent_inverse():
    lat, lon = np.array([50.1, 49.0, 51.3]), np.array([30.2, 28.5, 33.0])
    e, n = tangent(lat, lon, 50.0, 30.0)
    la, lo = inverse_tangent(e, n, 50.0, 30.0)
    assert np.allclose(la, lat, atol=1e-7) and np.allclose(lo, lon, atol=1e-7)


def test_korea_fit_and_sea():
    # Game metres built from the real coordinates through a known affine map; the fit must find it again.
    m = np.array([[0.01, 1.01], [1.009, 0.015], [-1000.0, 2000.0]])
    lat0, lon0 = 38.0, 126.0
    fields = []
    for key, (la, lo) in list(korea.REAL_AIRFIELDS.items())[:4]:
        e, n = tangent(np.array(la), np.array(lo), lat0, lon0)
        x, z = np.linalg.solve(m[:2].T, np.array([float(e), float(n)]) - m[2])
        fields.append((f"K-00_{key.title()}_AF", x, z))
    fields.append(("Nowhere_AF", 1.0, 2.0))
    fit = korea.fit_affine(fields)
    # The fit works on its own tangent plane (about the landmarks), so a few metres off over 300 km.
    assert fit and len(fit["landmarks"]) == 4 and fit["rmsMetres"] < 10
    s = korea.sea_settings([319.051, 319.051, 0.0, 0.0, 0.0], 9959)
    assert s["heightMul"] == pytest.approx(8.2013, abs=1e-3) and s["SeaLevel"] == pytest.approx(9959 / 256)
    assert korea.fit_affine(fields[:2]) is None


def _source(tmp_path) -> MapSource:
    raw = _terrain()
    water = raw.copy()
    water[:, :12] = 9500  # water above the sea strip's floor
    water[:, 12:] = 0
    files = {
        "/graphics/landscape_x/height.dat": synth.height_dat(raw, 32),
        "/graphics/landscape_x/height_w.dat": synth.height_dat(water, 32),
        "/graphics/landscape_x/height.hini": synth.hini(r"graphics\LANDSCAPE_X\height.dat",
                                                        r"graphics\LANDSCAPE_X\height_w.dat", CORNERS, 1.0, 36.0),
    }
    # 90 x 70 samples at 50 m: 4.45 km by 3.45 km; give corners of that size.
    corners = {"MapNW": (50.031, 30.0), "MapNE": (50.031, 30.0625), "MapSE": (50.0, 30.0625), "MapSW": (50.0, 30.0)}
    files["/graphics/landscape_x/height.hini"] = synth.hini(r"graphics\LANDSCAPE_X\height.dat",
                                                             r"graphics\LANDSCAPE_X\height_w.dat", corners, 1.0, 36.0)
    p = tmp_path / "Maps.gtp"
    p.write_bytes(synth.gtp(files))
    e = {x.name: x for x in read_table(p)}
    return MapSource("landscape_x", parse_hini(e["/graphics/landscape_x/height.hini"].read()),
                     e["/graphics/landscape_x/height.dat"], e["/graphics/landscape_x/height_w.dat"], "Great Battles")


def _doc(path):
    raw = path.read_bytes()
    (n,) = struct.unpack_from("<I", raw, 12)
    return json.loads(raw[20:20 + n])


def test_build_enu(tmp_path):
    src = _source(tmp_path)
    rec = build(src, tmp_path / "out", max_grid=40, log=lambda s: None)
    doc = _doc(tmp_path / "out" / "landscape_x.glb")
    names = [n["name"] for n in doc["nodes"]]
    assert names == ["ground:landscape_x", "water:landscape_x"]
    assert rec["frame"]["name"] == "enu" and rec["geo"]["lat0"] == pytest.approx(50.0155, abs=1e-3)
    assert rec["extent"]["west"] == pytest.approx(30.0) and rec["extent"]["north"] == pytest.approx(50.031)
    # Altitude = raw / 256 - 36: the sea strip's floor at 9000 is about -0.84 m, the water over it at 1.11 m.
    assert rec["parts"]["ground"]["height"][0] == pytest.approx(9000 / 256 - 36, abs=1e-3)
    acc = doc["accessors"][doc["meshes"][1]["primitives"][0]["attributes"]["POSITION"]]
    assert acc["min"][1] == pytest.approx(9500 / 256 - 36, abs=1e-3)
    # The map is about 4.45 km east-west, centred on the origin; the water strip is at its west edge.
    g = doc["accessors"][doc["meshes"][0]["primitives"][0]["attributes"]["POSITION"]]
    assert g["max"][0] - g["min"][0] == pytest.approx(89 * 50, rel=0.02)
    assert acc["max"][0] < g["min"][0] + 13 * 50 * 1.05


def test_build_game_frame_and_bad_corners(tmp_path):
    src = _source(tmp_path)
    src.hini.values["mapne"] = "10.0, 10.0"  # corners of another map: ignored, so no earth placement
    rec = build(src, tmp_path / "out", max_grid=40, frame="enu", log=lambda s: None)
    assert rec["frame"]["name"] == "game" and any("do not span" in n for n in rec["notes"])
    doc = _doc(tmp_path / "out" / "landscape_x.glb")
    g = doc["accessors"][doc["meshes"][0]["primitives"][0]["attributes"]["POSITION"]]
    assert g["min"][0] == pytest.approx(0.0) and g["max"][0] == pytest.approx(69 * 50)  # x north
    assert g["max"][2] == pytest.approx(89 * 50)  # z east
