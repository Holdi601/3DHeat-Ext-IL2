"""
Placing the IL-2 Series: Korea map without its `height.hini`.

Korea's archives keep their file names hashed and its settings files are not
readable, so the map's corner coordinates and height scale are not available
the way Great Battles has them. Both are worked out on the user's machine from
what the game does ship readable, its mission files (`data/Missions/**/*.Mission`):

- **Where it is**: the airfields a mission places (`Airfield { Name = "K-14_Kimpo_AF";
  XPos = ...; ZPos = ...; }`) are matched by name against the real airfields'
  published coordinates below, and an affine map from the game's metres
  (x north, z east) to east/north metres on the earth is fitted to them by least
  squares. The JSON records every landmark's residual; with the four airfields
  of the shipped demo missions they are a few hundred metres.
- **Heights**: ships sit on the sea, so the height missions give ships (their
  most common `YPos`) is the sea's height in the game's metres, and the water
  map's most common value is the sea's raw value: heightMul is their ratio
  (times 256), SeaLevel the raw value / 256.

The coordinates in the table are of the real places (public facts), not game
data; nothing from the game is in this file.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import numpy as np

#: Real airfields of the Korean War (lat, lon), keyed by a word their mission name contains.
REAL_AIRFIELDS: dict[str, tuple[float, float]] = {
    "kimpo": (37.5583, 126.7906),  # K-14, today Gimpo International
    "suwon": (37.2394, 127.0069),  # K-13, Suwon Air Base
    "seoul": (37.5257, 126.9244),  # K-16, Yeouido
    "antung": (40.0247, 124.2860),  # Antung (Dandong Langtou)
    "osan": (37.0906, 127.0297),  # K-55
    "taegu": (35.8941, 128.6589),  # K-2
    "kunsan": (35.9038, 126.6158),  # K-8
}

_BLOCK = re.compile(r"\n\s*(Airfield|Ship)\s*\{(.*?)\n\s*\}", re.S)


def _field(body: str, key: str) -> str | None:
    m = re.search(key + r'\s*=\s*"?([^";]*)', body)
    return m.group(1).strip() if m else None


def mission_objects(root: Path) -> tuple[list[tuple[str, float, float]], list[float]]:
    """Airfields (name, x, z) and ship heights from every mission file under data/Missions."""
    airfields: dict[str, tuple[float, float]] = {}
    ship_y: list[float] = []
    for path in sorted((root / "data" / "Missions").rglob("*.Mission")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for kind, body in _BLOCK.findall(text):
            try:
                x, y, z = (float(_field(body, k) or "nan") for k in ("XPos", "YPos", "ZPos"))
            except ValueError:
                continue
            if kind == "Airfield":
                name = _field(body, "Name") or ""
                airfields.setdefault(name, (x, z))
            else:
                ship_y.append(round(y, 3))
    return [(n, x, z) for n, (x, z) in airfields.items()], ship_y


def fit_affine(airfields: list[tuple[str, float, float]]) -> dict | None:
    """Game (x, z) to east/north metres about the landmarks' centre, or None with fewer than three matches."""
    from .level import tangent

    matched = []
    for name, x, z in airfields:
        key = next((k for k in REAL_AIRFIELDS if k in name.lower()), None)
        if key:
            matched.append((name, x, z, *REAL_AIRFIELDS[key]))
    if len(matched) < 3:
        return None
    lat0 = round(float(np.mean([m[3] for m in matched])), 4)
    lon0 = round(float(np.mean([m[4] for m in matched])), 4)
    a = np.array([[m[1], m[2], 1.0] for m in matched])
    e, n = tangent(np.array([m[3] for m in matched]), np.array([m[4] for m in matched]), lat0, lon0)
    b = np.stack([e, n], 1)
    matrix, *_ = np.linalg.lstsq(a, b, rcond=None)
    resid = np.hypot(*(a @ matrix - b).T)
    return {
        "origin": [lat0, lon0],
        "matrix": matrix.tolist(),
        "landmarks": [{"name": m[0], "lat": m[3], "lon": m[4], "residualMetres": round(float(r))}
                      for m, r in zip(matched, resid)],
        "rmsMetres": round(float(np.sqrt(np.mean(resid**2)))),
    }


def sea_settings(ship_y: list[float], water_mode_raw: int | None) -> dict | None:
    """heightMul and SeaLevel from the ships' height and the water map's commonest value."""
    if not ship_y or not water_mode_raw:
        return None
    afloat = [v for v in ship_y if v > 0]  # ships left at 0 were not put on the water by the editor
    if not afloat:
        return None
    y = Counter(afloat).most_common(1)[0][0]
    return {"heightMul": round(y * 256.0 / water_mode_raw, 4), "SeaLevel": water_mode_raw / 256.0,
            "from": f"ships at the game height {y} m on water whose raw value is {water_mode_raw}"}
