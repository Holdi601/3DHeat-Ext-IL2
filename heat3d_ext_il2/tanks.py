"""
The player-drivable tanks and assault guns of IL-2 Sturmovik: Great Battles (Tank Crew): how a vehicle is put
together from its parts, and its armour and modules.

Worked out from the files themselves; no game code was read or disassembled.

A drivable vehicle's folder is `graphics/vehicles/_<tank>/` (a leading `_`); its script is
`luascripts/worldobjects/vehicles/_<tank>.txt`:

- `VisualImage=0,"<hull>.mgm",...` is the hull as seen from outside (ID 1 is the crew's view from inside). The
  hull model's `.txt` names the game's own exterior levels of detail (`lod="..._10_<tank>.MGM",200`); the plain
  `.mgm` holds the interior and tracks drawn by skinning, so the levels are taken from that list.
- `HitBody="<tank>_DetColl.col"` is the hit geometry: a text file of named objects (`[Object = n]`, `Name="..."`,
  `Vertex=i: x, y, z`, `Face=i: a, b, c`) in the hull's frame.
- `energyloss="<object>",<inner>,<mm>,<k>` gives each hit object's armour: the third value is the thickness the
  game counts for it, in millimetres of armour steel (a glass block or a spaced plate already scaled down), the
  fourth a module's strength. `#` marks an outside part (tracks, wheels, covers, spare parts), `^` one shown
  shot away; an object with 0 mm is a dummy for visual damage only.
- `[attach=n] position=x,y,z rotation=... object="LuaScripts/WorldObjects/Vehicles/Turrets/_<tank>_T<k>.txt"`
  attaches each crew station with a weapon: the main turret (or an assault gun's mount), the commander's cupola,
  the hull machine gun. A station's own script has its `VisualImage=0` model, its `HitBody` (in the station's frame,
  which sits at the attach position), its `energyloss` lines, and `[Joint=0]`/`[Joint=1]` (traverse and
  elevation: `SectorAngleMin/Max`, `AnimationArgNum`) and `AimSector=left, right, down, up`.

In a station's model the gun is the node the elevation animation turns (argument 30, or the joint's own argument
where the model has it); an assault gun's mount is the node the traverse animation turns (argument 20). Both are
posed with the gun level and straight ahead (`models.py`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np

#: The folder the vehicles' scripts are in (and `turrets/` under it).
SCRIPTS = "luascripts/worldobjects/vehicles/"

_ATTACH = re.compile(r"\[attach\s*=\s*(\d+)\](.*?)\[end\]", re.S | re.I)
_VISUAL = re.compile(r'^\s*VisualImage\s*=\s*(\d+)\s*,\s*"([^"]+)"', re.M | re.I)
_HITBODY = re.compile(r'^\s*HitBody\s*=\s*"([^"]+)"', re.M | re.I)
_ELOSS = re.compile(r'^\s*energyloss\s*=\s*"([^"]*)"\s*,\s*(\w+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)', re.M | re.I)
_JOINT = re.compile(r"\[Joint\s*=\s*(\d+)\](.*?)\[end\]", re.S | re.I)
_AIM = re.compile(r"^\s*AimSector\s*=\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)", re.M | re.I)


def _path(p: str) -> str:
    return p.strip().replace("\\", "/").lower().lstrip("/")


def _floats(s: str | None, n: int = 3) -> tuple | None:
    if not s:
        return None
    try:
        v = tuple(float(x) for x in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s)[:n])
    except ValueError:
        return None
    return v if len(v) == n else None


def energyloss(text: str) -> dict:
    """`energyloss` lines: object name (lower case, as written) -> (inner, mm, k)."""
    out: dict = {}
    for m in _ELOSS.finditer(text):
        name = m.group(1).strip()
        if not name:
            continue
        try:
            out.setdefault(name.lower(), (m.group(2).lower() == "true", float(m.group(3)), float(m.group(4))))
        except ValueError:
            pass
    return out


@dataclass
class Joint:
    index: int
    arg: int
    lo: float
    hi: float


@dataclass
class Station:
    """A crew station with a weapon attached to the hull: its script, place and model."""
    index: int
    script: str
    at: np.ndarray
    rotation: tuple
    visual: str | None = None
    hitbody: str | None = None
    eloss: dict = field(default_factory=dict)
    joints: list = field(default_factory=list)
    aim: tuple | None = None  # left, right, down, up (degrees)

    @property
    def traverse(self) -> Joint | None:
        return next((j for j in self.joints if j.index == 0), None)

    @property
    def elevation(self) -> Joint | None:
        return next((j for j in self.joints if j.index == 1), None)

    @property
    def full_turn(self) -> bool:
        t = self.traverse
        return bool(t and t.hi - t.lo >= 359.0)


@dataclass
class Vehicle:
    unit: str
    visual: str
    hitbody: str | None
    eloss: dict
    stations: list

    @property
    def main(self) -> Station | None:
        """The station that carries the main gun: the first one with a model and both joints."""
        return next((s for s in self.stations if s.visual and s.traverse and s.elevation), None)


def _joints(text: str) -> list:
    out = []
    for m in _JOINT.finditer(text):
        body = m.group(2)

        def val(key, d=0.0):
            mm = re.search(rf"^\s*{key}\s*=\s*([-\d.]+)", body, re.M | re.I)
            return float(mm.group(1)) if mm else d

        out.append(Joint(int(m.group(1)), int(val("AnimationArgNum", -1)), val("SectorAngleMin"), val("SectorAngleMax")))
    return out


def parse_vehicle(unit: str, text: str, read) -> Vehicle | None:
    """A drivable vehicle's script; `read(path)` gives another script's text (or None). None for a script without
    an outside model."""
    vis = {int(i): _path(p) for i, p in _VISUAL.findall(text)}
    if 0 not in vis:
        return None
    hb = _HITBODY.search(text)
    stations = []
    for m in _ATTACH.finditer(text):
        body = m.group(2)
        obj = re.search(r'object\s*=\s*"([^"]+)"', body, re.I)
        if not obj or "/turrets/" not in _path(obj.group(1)):
            continue
        pos = _floats(re.search(r"position\s*=\s*([^\n/]+)", body, re.I).group(1)
                      if re.search(r"position\s*=", body, re.I) else None) or (0.0, 0.0, 0.0)
        rot = _floats(re.search(r"rotation\s*=\s*([^\n/]+)", body, re.I).group(1)
                      if re.search(r"rotation\s*=", body, re.I) else None) or (0.0, 0.0, 0.0)
        script = _path(obj.group(1))
        st = Station(int(m.group(1)), script, np.array(pos, np.float64), rot)
        t = read(script)
        if t:
            v = {int(i): _path(p) for i, p in _VISUAL.findall(t)}
            st.visual = v.get(0)
            h = _HITBODY.search(t)
            st.hitbody = _path(h.group(1)) if h else None
            st.eloss = energyloss(t)
            st.joints = _joints(t)
            a = _AIM.search(t)
            st.aim = tuple(float(x) for x in a.groups()) if a else None
        stations.append(st)
    return Vehicle(unit, vis[0], _path(hb.group(1)) if hb else None, energyloss(text), stations)


# --- hit geometry --------------------------------------------------------------------------------------------------

_OBJ = re.compile(r"\[Object\s*=\s*\d+\](.*?)\[End\]", re.S | re.I)
_VERT = re.compile(r"^\s*Vertex\s*=\s*(\d+)\s*:\s*([-\d.eE+]+)\s*,\s*([-\d.eE+]+)\s*,\s*([-\d.eE+]+)", re.M)
_FACE = re.compile(r"^\s*Face\s*=\s*\d+\s*:\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", re.M)


def read_col(text: str) -> list:
    """A `.col` text file's objects: [(name, verts (n, 3), faces (m, 3))], in the file's own frame."""
    out = []
    for m in _OBJ.finditer(text):
        body = m.group(1)
        nm = re.search(r'Name\s*=\s*"([^"]*)"', body)
        verts: dict = {}
        for v in _VERT.finditer(body):
            verts[int(v.group(1))] = (float(v.group(2)), float(v.group(3)), float(v.group(4)))
        if not nm or not verts:
            continue
        n = max(verts) + 1
        vs = np.zeros((n, 3))
        for i, p in verts.items():
            vs[i] = p
        fs = np.array([[int(x) for x in f.groups()] for f in _FACE.finditer(body)], np.int64).reshape(-1, 3)
        if len(fs) and fs.max() < n:
            out.append((nm.group(1), vs, fs))
    return out


def clean_name(name: str) -> str:
    """An object's name without the game's markers (`#` outside part, `^`/`^1` shown shot away, `~`)."""
    return re.sub(r"^[#^~\d]*(?=[A-Za-z])", "", name.strip()) if re.match(r"^[#^~]", name.strip()) else name.strip()


_GROUPS = [
    ("ammo", re.compile(r"ammo|ammun|shell|round|boekompl|snaryad", re.I)),
    ("fuel", re.compile(r"fuel|oiltank|oil_?tank|benz|tank_fuel", re.I)),
    ("engine", re.compile(r"engine|motor|dvigat", re.I)),
    ("transmission", re.compile(r"transmis|gearbox|gear_?box|final_?drive|brake|kpp", re.I)),
    ("radiator", re.compile(r"radiator|cooler", re.I)),
    ("electrics", re.compile(r"electric|battery|^radio(_?\d*)$|generator", re.I)),
    ("optics", re.compile(r"sight|visor|periscop|vision|tripleks|glass", re.I)),
    ("gun", re.compile(r"^(gun|mg\d*|mg_|cannon|barrel|tormoz|nakatnik|recuperator)", re.I)),
    ("drive", re.compile(r"^turret[gv]n|traverse|elevat|hydraul", re.I)),
    ("tracks", re.compile(r"^tr[au]ck_?[lr](_|\d|$)|caterp", re.I)),
    ("wheel", re.compile(r"^w[lr]\d|wheel|sprocket|idler|roller", re.I)),
    ("structure", re.compile(r"cover|screen|exhaust|headlight|antenna|_coll?$|spare|box|tool|fender|mudguard|smok|"
                             r"intake|rear_4|left_10|right_10", re.I)),
]

#: Hit body objects that are helpers, not parts: dummies, the crew's seat, the vision and size boxes.
_HELPER = re.compile(r"^dummy|^#?dummy|collsize|bot_pos|^visor\d*$|^gunsight\d*$", re.I)


def group_of(name: str) -> str:
    """What an object is: `armour` (a plate), a module (`ammo`, `fuel`, `engine`, `transmission`, `radiator`,
    `electrics`, `optics`, `gun`, `drive`) or an outside part that is no armour plate (`tracks`, `wheel`,
    `structure`: covers, side screens, spare parts, stowage, exhausts)."""
    n = clean_name(name)
    for g, pat in _GROUPS:
        if pat.search(n):
            return g
    return "armour"


def hit_objects(col_text: str, eloss: dict) -> list:
    """The objects of a hit body the script gives a thickness: [(name, verts, faces, mm, group)]. Dummies (0 mm,
    shown only when shot away) and objects the script names no thickness for are left out."""
    out = []
    for name, v, f in read_col(col_text):
        e = eloss.get(name.lower())
        if e is None or e[1] <= 0 or not len(f) or _HELPER.search(clean_name(name)):
            continue
        out.append((name, v, f, e[1], group_of(name)))
    return out
