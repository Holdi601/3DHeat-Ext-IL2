"""
Placing a map on the earth from places whose game position and real position are both known.

For maps whose `height.hini` corners cannot be used (Korea has no readable hini;
one Great Battles map family carries another map's corners), an affine map from
the game's metres (x north, z east) to east/north metres on the WGS-84 tangent
plane is fitted by least squares to landmarks:

- game positions come from the game's own files on the user's machine: mission
  files (`Airfield` blocks) and the career's location databases (`*.ldfbin` in
  the archives: named records, each 4 float64 values (x, y, z, heading), two
  more, a list of ids, and the name);
- real positions come from the tables below: published coordinates of the
  places (public facts, not game data).

The JSON records every landmark with its residual and the fit's rms, so a
placement is as good as it says it is.
"""

from __future__ import annotations

import re
import struct

import numpy as np

#: Towns and airfields of the First World War front in France and Flanders, by the name the
#: game's location database gives them. The coordinates are of the town (or the airfield
#: where the name says so), so expect a kilometre or two between a town and its airfield.
WESTERN_FRONT: dict[str, tuple[float, float]] = {
    "Douai": (50.3714, 3.0800),
    "Kortrijk": (50.8280, 3.2649),
    "Roubaix": (50.6942, 3.1746),
    "St.Omer": (50.7500, 2.2520),
    "Ham": (49.7467, 3.0733),
    "Metz-Frescaty": (49.0717, 6.1317),
    "Ghlin, Mons": (50.4870, 3.9070),
    "Guise, St. Quentin": (49.8992, 3.6283),
    "Champaubert": (48.8806, 3.7781),
    "Jametz": (49.4256, 5.3681),
    "Menin": (50.7967, 3.1213),
    "Halluin": (50.7836, 3.1253),
    "Lomme": (50.6447, 2.9875),
    "Fromelles": (50.6061, 2.8536),
    "Bohain": (49.9864, 3.4533),
    "Cappy": (49.9228, 2.7686),
}

#: Which location databases belong to which map family: their file names start with this.
LOCATION_PREFIX = {"westernfront": "wf_"}

_TEN_TEN = struct.pack("<2d", 10.0, 10.0)


def parse_ldfbin(data: bytes) -> list[tuple[str, float, float]]:
    """(name, x, z) of every named record of a location database."""
    out = []
    for m in re.finditer(re.escape(_TEN_TEN), data):
        p = m.start()
        if p < 32:
            continue
        x, _y, z, _a = struct.unpack_from("<4d", data, p - 32)
        q = m.end()
        if q + 4 > len(data):
            continue
        (n,) = struct.unpack_from("<I", data, q)
        if n > 1000:
            continue
        q += 4 + 4 * n
        if q + 4 > len(data):
            continue
        (length,) = struct.unpack_from("<I", data, q)
        if not 0 < length < 200 or q + 4 + length > len(data):
            continue
        name = data[q + 4 : q + 4 + length].decode("cp1252", "replace")
        if np.isfinite([x, z]).all():
            out.append((name, x, z))
    return out


def fit(points: list[tuple[str, float, float, float, float]]) -> dict | None:
    """Least-squares affine map from (x, z) to tangent-plane metres about the points' mean; None under three points."""
    from .level import tangent

    if len(points) < 3:
        return None
    lat0 = round(float(np.mean([p[3] for p in points])), 4)
    lon0 = round(float(np.mean([p[4] for p in points])), 4)
    a = np.array([[p[1], p[2], 1.0] for p in points])
    e, n = tangent(np.array([p[3] for p in points]), np.array([p[4] for p in points]), lat0, lon0)
    b = np.stack([e, n], 1)
    matrix, *_ = np.linalg.lstsq(a, b, rcond=None)
    resid = np.hypot(*(a @ matrix - b).T)
    return {
        "origin": [lat0, lon0],
        "matrix": matrix.tolist(),
        "landmarks": [{"name": p[0], "lat": p[3], "lon": p[4], "residualMetres": round(float(r))}
                      for p, r in zip(points, resid)],
        "rmsMetres": round(float(np.sqrt(np.mean(resid**2)))),
    }


def fit_named(found: list[tuple[str, float, float]], table: dict[str, tuple[float, float]]) -> dict | None:
    """Fit from game positions whose names are in `table` (exact names)."""
    seen: dict[str, tuple[float, float]] = {}
    for name, x, z in found:
        if name in table and name not in seen:
            seen[name] = (x, z)
    return fit([(k, x, z, *table[k]) for k, (x, z) in seen.items()])
