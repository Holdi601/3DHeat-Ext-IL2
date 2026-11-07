"""
`height.hini`: a map's settings, as plain `key=value` text (Windows-1251, `//`
comments). What is used here: the files it names (`height_map`, `water_map`),
`heightMul`, `SeaLevel`, the play limits, and the four corners' latitude and
longitude (`MapNE`, `MapNW`, `MapSW`, `MapSE`), which tie the map to the earth.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_CORNERS = ("MapNW", "MapNE", "MapSE", "MapSW")


@dataclass
class Hini:
    values: dict[str, str] = field(default_factory=dict)

    def get(self, key: str, default=None):
        return self.values.get(key.lower(), default)

    def number(self, key: str, default: float | None = None) -> float | None:
        v = self.get(key)
        try:
            return float(v) if v is not None else default
        except ValueError:
            return default

    def path(self, key: str) -> str | None:
        """A file the map names, as the archive's table spells it (`/graphics/landscape_x/height.dat`)."""
        v = self.get(key)
        if not v:
            return None
        return "/" + v.strip('"').replace("\\", "/").lower().lstrip("/")

    def corners(self) -> dict[str, tuple[float, float]] | None:
        """(lat, lon) of the four corners, or None if the map does not give all four."""
        out = {}
        for k in _CORNERS:
            v = self.get(k)
            if v is None:
                return None
            nums = re.findall(r"-?\d+(?:\.\d+)?", v)
            if len(nums) < 2:
                return None
            out[k] = (float(nums[0]), float(nums[1]))
        return out


def parse_hini(text: str | bytes) -> Hini:
    if isinstance(text, bytes):
        text = text.decode("cp1251", "replace")
    values: dict[str, str] = {}
    for line in text.splitlines():
        line = line.split("//", 1)[0].strip()
        if not line or line.startswith("[") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip().lower()
        if k and k not in values:  # the first wins: later sections repeat keys for other things
            values[k] = v.strip()
    return Hini(values)
