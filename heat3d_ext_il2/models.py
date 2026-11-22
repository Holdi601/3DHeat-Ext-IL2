"""
`heat3d-il2-level models`: every aircraft, vehicle, gun and ship model of the user's own IL-2 Sturmovik: Great
Battles install as a local 3DHeat model pack (`modelpack.py` for the format).

Per unit folder `graphics/<planes|vehicles|artillery|ships|trains>/<unit>/` in the `.gtp` archives:

- `<unit>.txt` names the LOD files (`lod="..._10_<unit>.mgm",400`) and the default animation arguments
  (`DefArg=<arg>,<value>`, `-1` for all), the pose the game shows the model in;
- `<unit>.mgm` is the full model (with its damage states), `10_`/`20_`/`30_` the game's own levels of detail and
  `80_`/`90_` its far forms.

The pack's three levels are the full model (or `10_`), `20_` and `30_` (or the far form), each posed at the default
arguments and simplified to the viewer's budget. Parts come from the model's own node names: propellers (a node an
animation spins a whole turn, with what hangs under it), landing gear (`gear`/`wheel`/`strut` nodes an animation
moves; fixed gear stays on the hull), a ground unit's turret (yaw) and gun (pitch), and the hit regions (`dm`): each
undamaged piece of the full model (`<piece>_D0...`), kept apart. Muzzle flashes, smoke, lights, glows, decals,
damaged states and pieces the default pose hides are left out; a ground unit's radio aerials are a part of their own
(`aerial`, left out of its size).

A tank the player drives (folder `_<tank>`, Tank Crew) is put together from its hull and its crew stations as its
script attaches them (`tanks.py`): the turret and gun as joints, posed with the gun level, the hatches shut and the
machine guns forward, and the armour plates and modules of its hit bodies, with their thickness, as `dm` pieces.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import mgm, tanks
from .gtp import Entry, read_table
from .modelpack import Pack, simplify, weld

#: graphics/<folder> -> domain.
FOLDERS = {"planes": "air", "vehicles": "ground", "artillery": "ground", "trains": "ground", "ships": "sea"}

#: Pieces left out: muzzle flashes and smoke, lights and their glows, markings, propeller blur, the inner
#: structure shown when a skin piece is shot away (`_wn`, `_nerv`, `stenka`, `_cap`), the cockpit.
_SKIP = re.compile(r"flash|smoke|torec|halo|bano|_light|light_|lamp|glow|decal|fire|trail|shadow|blur|"
                   r"_wn(_|$|\d)|_nerv|stenka|_cap$|^cf_|cockpit|collision|_rot_d|trash", re.I)
#: Damaged and destroyed states: `_D1`.. (a piece shot through), `_D` / `_D_..` / `_d003` (the wreck the game swaps in).
_DAMAGED = re.compile(r"_d[1-9](_|\s*$)|_d_|_d\s*$|_d\d{2,}", re.I)
_GEAR = re.compile(r"gear|wheel|strut|shassi|chassis|oleo|tailwheel|ski(_|\d|$)|truck", re.I)
_TURRET = re.compile(r"turret|tower|bashn|(^|\d_)head", re.I)
_GUN = re.compile(r"gun|barrel|cannon|mantlet|stvol|pushk|(^|\d_)mask", re.I)
_PIECE = re.compile(r"^(.*?)_d0(_|$)", re.I)
#: A ground unit's radio aerials (thin whips standing far above the body): their own part, left out of its size.
_AERIAL = re.compile(r"anten|aerial", re.I)
#: A ground unit's tracks and road wheel carriers (running gear, drawn in the track colour).
_TRACK = re.compile(r"(^|_)track[lr](_|\d|$)|lenta|karetk|caterp", re.I)
#: A drivable vehicle's pieces left out besides `_SKIP`: a track shown broken, the crew compartment's inside (`lc`, the
#: low-detail cockpit, and the rounds stowed in it).
_SKIP_GROUND = re.compile(r"fatal|inside|interior|(^|_)lc(_|\d|$)|lowcockpit|rashod", re.I)


@dataclass
class UnitFiles:
    unit: str
    folder: str
    domain: str
    files: dict = field(default_factory=dict)  # lower-case file name -> Entry

    def get(self, name: str) -> Entry | None:
        return self.files.get(name.lower())

    @property
    def fingerprint(self) -> str:
        h = hashlib.sha256()
        for k in sorted(self.files):
            if k.endswith((".mgm", ".txt")):
                e = self.files[k]
                h.update(f"{k}:{e.size}:{e.archive.name}:{e.offset};".encode())
        return h.hexdigest()[:16]


def scan(root: Path) -> dict[str, UnitFiles]:
    """Every unit folder with a model, from the install's archives."""
    out: dict[str, UnitFiles] = {}
    for archive in sorted((root / "data").glob("*.gtp")):
        low = archive.name.lower()
        if not low.startswith(("planes", "vehicles", "ships", "scripts", "graphics")):
            continue
        for e in read_table(archive):
            parts = e.name.strip("/").split("/")
            if len(parts) != 4 or parts[0] != "graphics" or parts[1] not in FOLDERS:
                continue
            unit = parts[2]
            u = out.get(f"{parts[1]}/{unit}")
            if u is None:
                u = out[f"{parts[1]}/{unit}"] = UnitFiles(unit, parts[1], FOLDERS[parts[1]])
            u.files.setdefault(parts[3], e)
    return {k: u for k, u in out.items() if u.get(f"{u.unit}.mgm") or u.get(f"10_{u.unit}.mgm")}


_OBJECT_NAME = re.compile(rb'^\s*object_name\s*=\s*"([^"]+)"', re.M | re.I)


def object_names(root: Path) -> dict[str, str]:
    """The names the game itself gives its units (`object_name` in `luascripts/worldobjects/<kind>/<unit>.txt`): what
    its mission files, logs and recordings call them ("Bf 109 G-6"). Unit folder name -> name."""
    out: dict[str, str] = {}
    for archive in sorted((root / "data").glob("Scripts*.gtp")):
        for e in read_table(archive):
            parts = e.name.strip("/").split("/")
            if len(parts) != 4 or parts[:2] != ["luascripts", "worldobjects"] or not parts[3].endswith(".txt"):
                continue
            m = _OBJECT_NAME.search(e.read(4096))
            if m:
                out.setdefault(parts[3][:-4], m.group(1).decode("latin1").strip())
    return out


def _read(e: Entry) -> mgm.Model:
    return mgm.read(e.read())


def _lineage(n: mgm.Node):
    while n is not None:
        yield n
        n = n.parent


def _spin_nodes(model: mgm.Model) -> dict:
    """Nodes an animation turns a whole turn (propellers): node id -> (axis in the node's frame)."""
    by = model.by_index()
    out = {}
    for a in model.anims:
        for ni, keys in a.tracks:
            if len(keys) < 3:
                continue
            # a whole turn: the angles between one key and the next (a quaternion and its negative are the same
            # turn) add up to about 360 degrees
            if not _spins(keys):
                continue
            ax = np.array([k.quat for k in keys])[:, :3]
            k = int(np.argmax(np.linalg.norm(ax, axis=1)))
            axis = ax[k] / (np.linalg.norm(ax[k]) or 1.0)
            n = by.get(ni)
            if n is not None and _has_blades(n):
                out[id(n)] = (n, axis)
    # a wing that tumbles away when shot off also turns whole turns and carries its engine's hub: the hub is the
    # spinning node nearest the blades
    inner = {k: v for k, v in out.items()
             if not any(k2 != k and k in {id(x) for x in _lineage(v2[0])} for k2, v2 in out.items())}
    return inner


_BLADE = re.compile(r"blade|prop|vint|lopa?st|screw|^15[0-9]{3}", re.I)


def _has_blades(n: mgm.Node) -> bool:
    stack = [n]
    while stack:
        x = stack.pop()
        if _BLADE.search(x.name) and not _SKIP.search(x.name):
            return True
        stack.extend(c for c in x.children if c is not None)
    return False


def _moved_nodes(model: mgm.Model) -> set:
    """Nodes an animation turns or moves (not only shows or hides)."""
    by = model.by_index()
    out = set()
    for a in model.anims:
        for ni, keys in a.tracks:
            if len(keys) < 2:
                continue
            qs = np.array([k.quat for k in keys])
            ps = np.array([k.pos for k in keys])
            if np.ptp(qs, axis=0).max() > 0.05 or np.ptp(ps, axis=0).max() > 0.02:
                n = by.get(ni)
                if n is not None:
                    out.add(id(n))
    return out


_INNER = re.compile(r"^(.*?)_wn(?:_?\d+)?$", re.I)


def _region_labels(model: mgm.Model) -> dict:
    """Damage argument -> the piece's name, from the inner structure nodes shown when it is shot away
    (`Win_L_wn_07` with argument 11120 -> "Win_L")."""
    out: dict = {}
    for n in model.nodes:
        m = _INNER.match(n.name)
        if m and n.arg and m.group(1):
            out.setdefault(n.arg, m.group(1).strip("_"))
    return out


def _region(line: list, labels: dict) -> str | None:
    """A hit region: the damage argument a piece (or the first of its parents) is shot away by, named."""
    for x in line:
        if x.arg:
            label = labels.get(x.arg) or re.sub(r"^\^\d_", "", x.name)
            return f"{label}.{x.arg}" if not label.endswith(str(x.arg)) else label
        m = _PIECE.match(x.name)
        if m:
            return m.group(1)
    return None


@dataclass
class Posed:
    parts: dict  # part name -> list of (verts, faces)
    pivots: dict
    joints: dict
    pieces: dict  # dm piece -> (verts, faces, part)
    gear_moves: bool = False


def _subtree_has(n: mgm.Node, pat: re.Pattern) -> bool:
    stack = [n]
    while stack:
        x = stack.pop()
        if pat.search(x.name):
            return True
        stack.extend(c for c in x.children if c is not None)
    return False


def _mostly_gear(n: mgm.Node) -> bool:
    """Whether most of the triangles under a node belong to landing gear (a gear leg's joint, not a wing or a tail
    that carries a wheel)."""
    gear = other = 0
    stack = [(n, bool(_GEAR.search(n.name)))]
    while stack:
        x, g = stack.pop()
        g = g or bool(_GEAR.search(x.name))
        if x.chunk is not None and x.ni and not _SKIP.search(x.name) and not _DAMAGED.search(x.name):
            if g:
                gear += x.ni
            else:
                other += x.ni
        stack.extend((c, g) for c in x.children if c is not None)
    return gear > 0 and gear >= 2 * other


#: The animation arguments that retract an aircraft's landing gear (left, right, nose or tail wheel).
GEAR_ARGS = {13300, 13310, 13320}


def gear_down(model: mgm.Model, args) -> tuple[dict, set]:
    """The argument values that put the landing gear down (of each animation that turns or moves a node holding
    gear, the end, 0 or 1, at which the gear's lowest point is lowest; the game's default pose may have it up), and
    the nodes those animations move: the retracting gear."""
    by = model.by_index()
    moved = _moved_nodes(model)
    gear_args = set()
    legs: set = set()
    # The game's own gear arguments (left, right, nose or tail: what every aircraft's `.txt` sets to 1.0, gear down),
    # else any animation that moves mostly gear-named nodes.
    own = {a.arg for a in model.anims} & GEAR_ARGS
    for a in model.anims:
        for ni, keys in a.tracks:
            n = by.get(ni)
            if n is None or id(n) not in moved:
                continue
            if a.arg in own or (not own and _mostly_gear(n)):
                gear_args.add(a.arg)
                # a turn of more than 30 degrees retracts; less is a strut compressing or a wheel's steering
                qs = np.array([k.quat for k in keys])
                if 2 * np.degrees(np.arccos(np.abs(qs @ qs[0]).clip(0, 1))).max() > 30 and not _spins(keys):
                    legs.add(id(n))
    if not gear_args or not legs:
        return {}, set()
    cache: dict = {}
    meshes = []
    for n in model.nodes:
        if n.chunk is not None and n.ni and any(id(x) in legs for x in _lineage(n)):
            m = mgm.node_mesh(model, n, cache)
            if m is not None:
                meshes.append((n, m))
    if not meshes:
        return {}, set()

    def lowest(values: dict) -> float:
        class _A(dict):
            def get(self, k, d=None):
                return values[k] if k in values else args.get(k, d)

        anim, _ = mgm.pose(model, _A())
        world = mgm.world_matrices(model, anim)
        low = np.inf
        for n, (v, _f) in meshes:
            y = (np.c_[v, np.ones(len(v))] @ world[id(n)])[:, 1]
            low = min(low, float(y.min()))
        return low

    out = {}
    for a in sorted(gear_args):
        out[a] = 0.0 if lowest({**out, a: 0.0}) <= lowest({**out, a: 1.0}) - 1e-3 else 1.0
    return out, legs


def _spins(keys: list) -> bool:
    qs = np.array([k.quat for k in keys])
    if len(qs) < 3:
        return False
    qs = qs / np.linalg.norm(qs, axis=1, keepdims=True).clip(1e-9)
    dots = np.abs((qs[1:] * qs[:-1]).sum(1)).clip(0, 1)
    return 2 * np.arccos(dots).sum() >= 1.8 * np.pi


def pose_parts(model: mgm.Model, args: dict, domain: str, with_pieces: bool = False, assign=None) -> Posed:
    """The model at its default pose (an aircraft's gear down), split into the viewer's parts. `assign(line)` (the
    node and its parents) names the part of a drivable vehicle's piece instead of the node names' guess."""
    legs: set = set()
    if domain == "air":
        down, legs = gear_down(model, args)
        if down:
            base_args = args

            class _Down(dict):
                def get(self, k, d=None):
                    return down[k] if k in down else base_args.get(k, d)

            args = _Down()
    anim, shown = mgm.pose(model, args)
    world = mgm.world_matrices(model, anim)
    spins = _spin_nodes(model) if domain == "air" else {}
    cache: dict = {}
    parts: dict = {}
    pieces: dict = {}
    rotor_of: dict = {}
    for i, (nid, (n, axis)) in enumerate(sorted(spins.items(), key=lambda x: x[1][0].index)):
        rotor_of[nid] = f"rotor.{i + 1}"
    gear_moves = False
    origin: dict = {}
    labels = _region_labels(model) if with_pieces else {}
    for n in model.nodes:
        if n.helper or n.chunk is None or not n.ni:
            continue
        line = list(_lineage(n))
        if any(not shown.get(id(x), True) for x in line):
            continue
        if any(_SKIP.search(x.name) or _DAMAGED.search(x.name) for x in line):
            continue
        if assign is not None and (n.chunk.bones or any(_SKIP_GROUND.search(x.name) for x in line)):
            # a drivable vehicle's skinned pieces (tracks, a whip aerial) are drawn by the game from their bones'
            # pose, not read here
            continue
        mesh = mgm.node_mesh(model, n, cache)
        if mesh is None:
            continue
        v, f = mesh
        v = (np.c_[v, np.ones(len(v))] @ world[id(n)])[:, :3]
        part = "hull"
        rot = next((rotor_of[id(x)] for x in line if id(x) in rotor_of), None)
        if rot:
            part = rot
        elif domain == "air" and any(id(x) in legs for x in line):
            part = "gear"
            gear_moves = True
        elif domain == "ground" and any(_AERIAL.search(x.name) for x in line):
            part = "aerial"
        elif assign is not None:
            part = assign(line)
            if part is None:
                continue
            if part == "hull" and any(_GEAR.search(x.name) or _TRACK.search(x.name) for x in line):
                part = "gear"
        elif domain != "air":
            tur = [x for x in line if _TURRET.search(x.name)]
            gun = [x for x in line if _GUN.search(x.name)]
            if gun and tur:
                part = "gun"
                origin.setdefault("gun", world[id(gun[-1])][3, :3])
            elif tur:
                part = "turret"
                origin.setdefault("turret", world[id(tur[-1])][3, :3])
            elif domain == "ground" and any(_GEAR.search(x.name) or _TRACK.search(x.name) for x in line):
                part = "gear"
        parts.setdefault(part, []).append((v, f))
        if with_pieces:
            region = _region(line, labels)
            if region:
                pieces.setdefault(region, ([], part))[0].append((v, f))
    pivots: dict = {}
    joints: dict = {}
    for nid, (n, axis) in spins.items():
        name = rotor_of[nid]
        if name not in parts:
            continue
        w = world[nid]
        at = w[3, :3]
        ax = axis @ w[:3, :3]
        ax = ax / (np.linalg.norm(ax) or 1.0)
        if ax[0] < 0:
            ax = -ax
        vs = np.concatenate([v for v, _ in parts[name]])
        rel = vs - at
        radial = rel - np.outer(rel @ ax, ax)
        joints[name] = {"spin": "rotor", "pivot": [round(float(x), 4) for x in at],
                        "axis": [round(float(x), 4) for x in ax],
                        "diameter": round(float(2 * np.linalg.norm(radial, axis=1).max()), 3)}
    if "gear" in parts:
        vs = np.concatenate([v for v, _ in parts["gear"]])
        lo, hi = vs.min(0), vs.max(0)
        pivots["gear"] = [round(float((lo[0] + hi[0]) / 2), 4), round(float(hi[1]), 4),
                          round(float((lo[2] + hi[2]) / 2), 4)]
    for p in ("turret", "gun"):
        if p in parts and p in origin:
            pivots[p] = [round(float(x), 4) for x in origin[p]]
        elif p in parts:
            vs = np.concatenate([v for v, _ in parts[p]])
            lo, hi = vs.min(0), vs.max(0)
            if p == "turret":
                pivots[p] = [round(float((lo[0] + hi[0]) / 2), 4), round(float(lo[1]), 4), round(float((lo[2] + hi[2]) / 2), 4)]
            else:
                pivots[p] = [round(float(lo[0]), 4), round(float((lo[1] + hi[1]) / 2), 4), round(float((lo[2] + hi[2]) / 2), 4)]
    if "gun" in parts and "turret" not in parts:
        parts["hull"] = parts.get("hull", []) + parts.pop("gun")
        pivots.pop("gun", None)
    return Posed(parts, pivots, joints, {k: (merge_list(v), p) for k, (v, p) in pieces.items()}, gear_moves)


def merge_list(items: list) -> tuple[np.ndarray, np.ndarray]:
    vs, fs, at = [], [], 0
    for v, f in items:
        vs.append(v)
        fs.append(f + at)
        at += len(v)
    if not vs:
        return np.zeros((0, 3)), np.zeros((0, 3), np.int64)
    return np.concatenate(vs), np.concatenate(fs)


def lod_sources(u: UnitFiles) -> list[Entry]:
    """The game's files for the pack's three levels: full, coarse, far."""
    # `10_` is the game's own full exterior; the plain file adds cockpit and crew stations (a bomber's fuselage
    # glazing lives in those), so for aircraft it is taken only where there is no `10_`; a vehicle's or a ship's
    # plain file is its full model and `10_` already a coarser one
    if u.domain == "air":
        main = u.get(f"10_{u.unit}.mgm") or u.get(f"{u.unit}.mgm")
    else:
        main = u.get(f"{u.unit}.mgm") or u.get(f"10_{u.unit}.mgm")
    coarse = u.get(f"20_{u.unit}.mgm") or u.get(f"10_{u.unit}.mgm") or main
    far = u.get(f"30_{u.unit}.mgm") or u.get(f"80_{u.unit}.mgm") or u.get(f"90_{u.unit}.mgm") or coarse
    return [main, coarse, far]


def default_args(u: UnitFiles) -> tuple[dict, float]:
    e = u.get(f"{u.unit}.txt")
    if e is None:
        return {}, 0.0
    t = mgm.parse_txt(e.read().decode("latin1", "replace"))
    args = dict(t["args"])
    base = args.pop(-1, 0.0)
    return args, base


DM_BUDGET = 400


def _simplified(levels: list, domain: str) -> list:
    """The pack's three levels from the posed ones ({part: [(verts, faces)]} each, full first): each simplified to
    the viewer's budget; a coarse level coarser than the viewer's or without a moving part is made from the full."""
    from .modelpack import BUDGET, tris

    lods = []
    full: dict = {}
    for i, posed_parts in enumerate(levels):
        parts = {p: weld(*merge_list(v)) for p, v in posed_parts.items()}
        parts = {p: x for p, x in parts.items() if len(x[1])}
        budget = BUDGET.get(domain, BUDGET["ground"])[min(i, 2)]
        if i == 0:
            full = parts
        elif full and (tris(parts) < 0.3 * budget or set(full) - set(parts)):
            # the game's coarse form is coarser than the viewer's (some vehicles' 20_ have a few dozen triangles)
            # or has lost a moving part: made from the full model instead
            parts = full
        if not parts:
            continue
        lod = simplify(parts, budget, domain)
        if tris(lod) > 1.3 * budget:
            lod = simplify(lod, int(budget * 0.8), domain)
        while any(len(v) >= 65535 for v, _ in lod.values()):
            lod = simplify(lod, int(tris(lod) * 0.7), domain)
        lods.append(lod)
    if not lods:
        raise mgm.MgmError("no geometry at the default pose")
    while len(lods) < 3:
        lods.append(lods[-1])
    return lods[:3]


def _turret_joints(pivots: dict) -> dict:
    """A ground unit's turret and gun as joints (yaw, pitch on the turret) from their pivots."""
    out = {}
    if "turret" in pivots:
        out["turret"] = {"joint": "yaw", "pivot": pivots["turret"]}
    if "gun" in pivots:
        out["gun"] = {"joint": "pitch", "pivot": pivots["gun"], **({"parent": "turret"} if "turret" in pivots else {})}
    return out


def build_unit(u: UnitFiles, pack: Pack, key: str, kind: str, aliases: list, extra: dict,
               scripts: dict | None = None) -> dict:
    """Reads, poses, splits and writes one unit. Raises mgm.MgmError for a model it cannot read. `scripts`
    (`vehicle_scripts`) lets a drivable vehicle be put together from its hull and crew stations (`tanks.py`)."""
    if u.domain == "ground" and scripts:
        veh = drivable(u, scripts)
        if veh is not None:
            return build_drivable(u, veh, scripts, pack, key, kind, aliases, extra)
    args, base = default_args(u)
    srcs = lod_sources(u)
    models: dict = {}
    levels = []
    pivots: dict = {}
    joints: dict = {}
    pieces: dict = {}
    gear_moves = False
    for i, e in enumerate(srcs):
        if e is None:
            continue
        m = models.get(e.name)
        if m is None:
            m = models[e.name] = _read(e)
        posed = _posed(m, args, base, u.domain, with_pieces=(i == 0))
        if i == 0:
            pivots, joints, pieces, gear_moves = posed.pivots, posed.joints, posed.pieces, posed.gear_moves
        levels.append(posed.parts)
    lods = _simplified(levels, u.domain)
    if u.domain != "air":
        joints = {**_turret_joints({p: v for p, v in pivots.items() if p in lods[0]}), **joints}
    dm = []
    for name, ((v, f), part) in sorted(pieces.items()):
        if not len(f):
            continue
        v, f = weld(v, f)
        if len(f) > DM_BUDGET:
            v, f = simplify({"hull": (v, f)}, DM_BUDGET)["hull"]
        if len(f):
            dm.append((name, v, f, {"part": part, "group": name}))
    if not gear_moves:
        pivots.pop("gear", None)
    # crew stations the game models apart (`<unit>-c2.mgm`; `-wm`: with its weapon mount, a gunner's turret)
    crew = sorted({k[len(u.unit) + 1:].split("-")[0] for k in u.files
                   if k.startswith(f"{u.unit}-c") and k.endswith(".mgm")})
    turrets = sorted({k[len(u.unit) + 1:].split("-")[0] for k in u.files
                      if k.startswith(f"{u.unit}-c") and "-wm" in k and k.endswith(".mgm")})
    if crew:
        extra = {**extra, "crew": crew, **({"gunnerTurrets": turrets} if turrets else {})}
    return pack.add_lods(u.unit, lods, u.domain, kind, key=key, pivots=pivots, joints=joints, aliases=aliases, dm=dm,
                         fingerprint=u.fingerprint, extra=extra)


# --- drivable vehicles (Tank Crew) ---------------------------------------------------------------------------------


def vehicle_scripts(root: Path) -> dict:
    """The install's vehicle scripts (`luascripts/worldobjects/vehicles/`, with `turrets/`): lower-case path ->
    Entry."""
    out: dict = {}
    for archive in sorted((root / "data").glob("Scripts*.gtp")):
        for e in read_table(archive):
            name = e.name.strip("/")
            if name.startswith(tanks.SCRIPTS) and name.endswith(".txt"):
                out.setdefault(name, e)
    return out


def drivable(u: UnitFiles, scripts: dict) -> tanks.Vehicle | None:
    """A unit the player drives (its script attaches crew stations with weapons to the hull), or None."""
    e = scripts.get(f"{tanks.SCRIPTS}{u.unit}.txt")
    if e is None:
        return None

    def read(path: str) -> str | None:
        x = scripts.get(path)
        return x.read().decode("latin1", "replace") if x is not None else None

    veh = tanks.parse_vehicle(u.unit, e.read().decode("latin1", "replace"), read)
    if veh is None or veh.main is None or not u.get(veh.visual.rsplit("/", 1)[-1]):
        return None
    return veh


def _component_levels(u: UnitFiles, visual: str, plain_first: bool = False) -> tuple[list, dict, float]:
    """A component model's levels and its default arguments: the game's own list in its `.txt` (full first), after
    the plain model when `plain_first` (a crew station's outside model, whose own levels of detail may lose its
    gun's animation), the plain model alone when the `.txt` names none. A hull's plain model holds the inside and
    the tracks drawn by skinning, so a hull's levels are the listed ones."""
    name = visual.rsplit("/", 1)[-1]
    txt = u.get(name[:-4] + ".txt") if name.endswith(".mgm") else None
    args: dict = {}
    base, files = 0.0, []
    if txt is not None:
        t = mgm.parse_txt(txt.read().decode("latin1", "replace"))
        args = dict(t["args"])
        base = args.pop(-1, 0.0)
        files = [u.get(p.rsplit("/", 1)[-1]) for p, _px in t["lods"]]
    files = [f for f in files if f is not None]
    if plain_first or not files:
        files = [u.get(name), *files]
    files = [f for f in files if f is not None]
    if not files:
        raise mgm.MgmError(f"{name} not found")
    return [files[0], files[min(1, len(files) - 1)], files[-1]], args, base


def _turned_nodes(m: mgm.Model, wanted: list, args) -> tuple:
    """The nodes an animation of the first of the `wanted` arguments the model has turns (a gun, an assault gun's
    mount; hatches it also swings left out), the one among them reaching farthest from its pivot (the barrel), the
    argument and that node's keys."""
    by = m.by_index()
    anim, _shown = mgm.pose(m, args)
    world = mgm.world_matrices(m, anim)
    cache: dict = {}

    def reach(n: mgm.Node) -> float:
        inv = np.linalg.inv(world[id(n)])
        far, stack = 0.0, [n]
        while stack:
            x = stack.pop()
            if x.chunk is not None and x.ni and not x.helper and not _SKIP.search(x.name)                     and not _DAMAGED.search(x.name):
                r = mgm.node_mesh(m, x, cache)
                if r is not None:
                    v = (np.c_[r[0], np.ones(len(r[0]))] @ world[id(x)] @ inv)[:, :3]
                    far = max(far, float(np.linalg.norm(v, axis=1).max()))
            stack.extend(c for c in x.children if c is not None)
        return far

    for arg in wanted:
        turned = []
        for a in m.anims:
            if a.arg != arg:
                continue
            for ni, keys in a.tracks:
                n = by.get(ni)
                if n is None or len(keys) < 2 or _HATCH.search(n.name):
                    continue
                qs = np.array([k.quat for k in keys])
                if 2 * np.degrees(np.arccos(np.abs(qs @ qs[0]).clip(0, 1))).max() >= 2:
                    turned.append((n, keys))
        if turned:
            far = max(turned, key=lambda nk: reach(nk[0]))
            return far[0], arg, far[1], {id(n) for n, _k in turned}
    return None, None, [], set()


def _aim_value(m: mgm.Model, node: mgm.Node, keys: list, args, pitch: bool) -> float | None:
    """The value of the argument that turns `node` (a gun, an assault gun's mount) at which the gun points straight
    ahead and level: from the pivot to the far end of what the node carries (the muzzle), level for the elevation,
    along the hull for the traverse. None when no value points it forward."""
    anim, _shown = mgm.pose(m, args)
    world = mgm.world_matrices(m, anim)
    inv = np.linalg.inv(world[id(node)])
    cache: dict = {}
    pts = []
    stack = [node]
    while stack:
        x = stack.pop()
        if x.chunk is not None and x.ni and not x.helper and not _SKIP.search(x.name) and not _DAMAGED.search(x.name):
            r = mgm.node_mesh(m, x, cache)
            if r is not None:
                pts.append(np.c_[r[0], np.ones(len(r[0]))] @ world[id(x)] @ inv)
        stack.extend(c for c in x.children if c is not None)
    if not pts:
        return None
    local = np.concatenate(pts)
    parent = world[id(node.parent)] if node.parent is not None else np.eye(4)
    # the far end, as the node is posed now: the 2 % of points farthest from the pivot
    d = np.linalg.norm(local[:, :3], axis=1)
    far = local[d >= np.quantile(d, 0.98)].mean(0)

    # every animation that moves the node, in the order `mgm.pose` applies them (a machine gun's elevation and its
    # mode can turn the same node)
    tracks = [(a.arg, ks) for a in m.anims for ni, ks in a.tracks if ni == node.index]

    def aim(t: float) -> tuple[float, float]:
        k = None
        for a, ks in tracks:
            mk, _s = mgm.key_at(ks, t if ks is keys else args.get(a, 0.0))
            k = mk if k is None else mk @ k
        w = (np.eye(4) if k is None else k) @ node.local @ parent
        p = far @ w - w[3]
        horiz = float(np.hypot(p[0], p[2]))
        if pitch:
            return float(np.degrees(np.arctan2(p[1], horiz))), float(p[0])
        return float(np.degrees(np.arctan2(p[2], p[0]))), float(p[0])

    best, best_t = np.inf, None
    for t in np.linspace(0.0, 1.0, 361):
        a, fwd = aim(float(t))
        if fwd > 0 and abs(a) < best:
            best, best_t = abs(a), float(t)
    return best_t if best < 2.0 else None


_HATCH = re.compile(r"hatch|hutch|lyuk|(^|_)luk(_|\d|$)|door|lid(_|\d|$)", re.I)


def _closed_hatches(m: mgm.Model, args, keep: set) -> dict:
    """Argument values that close the hatches (the `.txt`'s defaults open some, the commander's among them): of
    each animation that swings a hatch, the end (0 or 1) at which what it moves stands lowest (a hatch opens up),
    else stands out least to the side."""
    by = m.by_index()
    hatch_args = set()
    for a in m.anims:
        if a.arg in keep:
            continue
        for ni, keys in a.tracks:
            n = by.get(ni)
            # the turned node is the hatch, or a helper holding it
            if n is None or len(keys) < 2 or not (_HATCH.search(n.name) or any(
                    c is not None and _HATCH.search(c.name) for c in n.children)):
                continue
            qs = np.array([k.quat for k in keys])
            # a hatch swings open (a turn); a piece only shown or hidden by an argument is no hatch
            if 2 * np.degrees(np.arccos(np.abs(qs @ qs[0]).clip(0, 1))).max() > 10:
                hatch_args.add(a.arg)
    if not hatch_args:
        return {}
    cache: dict = {}
    meshes = [(n, r) for n in m.nodes if n.chunk is not None and n.ni and not n.helper
              for r in [mgm.node_mesh(m, n, cache)] if r is not None]
    moved = {a.arg: {ni for ni, _k in a.tracks} for a in m.anims if a.arg in hatch_args}

    def reach(values: dict, arg: int) -> tuple[float, float]:
        anim, shown = mgm.pose(m, _Defaults({**args, **values}, args.base))
        world = mgm.world_matrices(m, anim)
        ids = {id(by[i]) for i in moved[arg] if i in by}
        top = side = -np.inf
        for n, (v, _f) in meshes:
            if any(id(x) in ids for x in _lineage(n)) and all(shown.get(id(x), True) for x in _lineage(n)):
                w = (np.c_[v, np.ones(len(v))] @ world[id(n)])[:, :3]
                top = max(top, float(w[:, 1].max()))
                side = max(side, float(np.hypot(w[:, 0], w[:, 2]).max()))
        return top, side

    out: dict = {}
    for arg in sorted(hatch_args):
        (t0, s0), (t1, s1) = reach({**out, arg: 0.0}, arg), reach({**out, arg: 1.0}, arg)
        if abs(t0 - t1) > 0.01:
            out[arg] = 0.0 if t0 < t1 else 1.0
        elif abs(s0 - s1) > 0.01:
            out[arg] = 0.0 if s0 < s1 else 1.0
    return out


def _still_barrels(m: mgm.Model, args, gun: mgm.Node, guns: set) -> set:
    """Pieces outside the gun that reach out along it to well past its mantlet: a second, fixed copy of the barrel
    some older station models keep in a turret shell of their own (a gun that would not elevate). Left out."""
    anim, shown = mgm.pose(m, args)
    world = mgm.world_matrices(m, anim)
    pivot = world[id(gun)][3, :3]
    cache: dict = {}
    reach = 0.0
    rows = []
    for n in m.nodes:
        if n.helper or n.chunk is None or not n.ni:
            continue
        r = mgm.node_mesh(m, n, cache)
        if r is None:
            continue
        line = list(_lineage(n))
        if any(not shown.get(id(x), True) for x in line):
            continue
        v = (np.c_[r[0], np.ones(len(r[0]))] @ world[id(n)])[:, :3]
        if {id(x) for x in line} & guns:
            reach = max(reach, float(v[:, 0].max() - pivot[0]))
        else:
            rows.append((n, float(v[:, 0].max() - pivot[0])))
    return {id(n) for n, ahead in rows if reach > 1.0 and ahead > 0.6 * reach}


@dataclass
class _Component:
    parts: list  # per level: {part: [(verts, faces)]}, in the hull's frame
    pivots: dict = field(default_factory=dict)


class _Defaults(dict):
    """Arguments; those not named stay at the `.txt`'s `DefArg=-1` value."""

    def __init__(self, values: dict, base: float):
        super().__init__(values)
        self.base = base

    def get(self, k, d=None):
        return dict.get(self, k, self.base)


def _station_component(u: UnitFiles, st: tanks.Station, main: bool, on_turret: bool) -> _Component:
    """A crew station's model posed at rest (gun level, straight ahead) and moved to its place on the hull; the main
    station's parts are `turret` and `gun` (an assault gun's mount: `turret` is what traverses, the rest `hull`)."""
    files, args, base = _component_levels(u, st.visual, plain_first=True)
    comp = _Component([])
    for i, e in enumerate(files):
        m = _read(e)
        gun = mount = None
        guns: set = set()
        mounts: set = set()
        rest: dict = {}
        tr, el = st.traverse, st.elevation
        if main:
            if not st.full_turn:
                mount, arg, keys, mounts = _turned_nodes(m, [a for a in (tr.arg if tr else -1, 20) if a >= 0],
                                                         _Defaults(args, base))
                if mount is not None:
                    r = _aim_value(m, mount, keys, _Defaults({**args, **rest}, base), pitch=False)
                    if r is not None:
                        rest[arg] = r
            gun, arg, keys, guns = _turned_nodes(m, [a for a in (el.arg if el else -1, 30) if a >= 0],
                                                 _Defaults({**args, **rest}, base))
            if gun is not None:
                r = _aim_value(m, gun, keys, _Defaults({**args, **rest}, base), pitch=True)
                if r is not None:
                    rest[arg] = r
        else:
            # a machine gun's mount: straight ahead and level, as the main gun (the game's arguments for a machine
            # gun's traverse and elevation)
            for own, pitch in (((21006,), False), ((21002, 21102), True)):
                n, arg, keys, _all = _turned_nodes(m, list(own), _Defaults({**args, **rest}, base))
                if n is not None:
                    r = _aim_value(m, n, keys, _Defaults({**args, **rest}, base), pitch=pitch)
                    if r is not None:
                        rest[arg] = r
        pose_args = _Defaults({**args, **rest}, base)
        pose_args.update(_closed_hatches(m, pose_args, set(rest)))
        still = _still_barrels(m, pose_args, gun, guns) if gun is not None else set()

        def assign(line, guns=guns, mounts=mounts, still=still):
            ids = {id(x) for x in line}
            if ids & still:
                return None
            if ids & guns:
                return "gun"
            if ids & mounts:
                return "turret"
            if main and st.full_turn:
                return "turret"
            return "turret" if on_turret else "hull"

        posed = pose_parts(m, pose_args, "ground", assign=assign)
        comp.parts.append({p: [(v + st.at, f) for v, f in vs] for p, vs in posed.parts.items()})
        if i == 0 and main:
            anim, _shown = mgm.pose(m, pose_args)
            world = mgm.world_matrices(m, anim)
            if gun is not None:
                comp.pivots["gun"] = world[id(gun)][3, :3] + st.at
            if st.full_turn:
                comp.pivots["turret"] = st.at.copy()
            elif mount is not None:
                comp.pivots["turret"] = world[id(mount)][3, :3] + st.at
    return comp


def _nearest_part(points: np.ndarray, parts: dict) -> str:
    """The part whose surface (its vertices) lies nearest the middle of `points`."""
    c = points.mean(0)
    best, best_d = "hull", np.inf
    for p, vs in parts.items():
        if p not in ("hull", "turret", "gun") or not vs:
            continue
        v = np.concatenate([x for x, _ in vs])
        d = float(np.min(np.einsum("ij,ij->i", v - c, v - c)))
        if d < best_d:
            best, best_d = p, d
    return best


def _on_turret(st: tanks.Station, main: tanks.Station | None) -> bool:
    """A station that turns with the main turret (a commander's cupola): attached where the turret is."""
    return bool(main is not None and main.full_turn and st is not main and np.allclose(st.at, main.at, atol=1e-3))


def build_drivable(u: UnitFiles, veh: tanks.Vehicle, scripts: dict, pack: Pack, key: str, kind: str, aliases: list,
                   extra: dict) -> dict:
    """A drivable vehicle put together: the hull, each crew station's model at its place (the main gun's turret and
    gun as joints), and its hit body's armour plates and modules with their thickness as `dm` pieces."""
    files, args, base = _component_levels(u, veh.visual)
    levels: list = [{} for _ in range(3)]
    for i, e in enumerate(files):
        m = _read(e)
        hull_args = _Defaults(args, base)
        hull_args.update(_closed_hatches(m, hull_args, set()))
        posed = pose_parts(m, hull_args, "ground", assign=lambda line: "hull")
        for p, vs in posed.parts.items():
            levels[i].setdefault(p, []).extend(vs)
    main = veh.main
    pivots: dict = {}
    comps: dict = {}
    for st in veh.stations:
        if not st.visual or not u.get(st.visual.rsplit("/", 1)[-1]):
            continue
        comp = _station_component(u, st, st is main, _on_turret(st, main))
        comps[st.index] = comp
        for i in range(3):
            for p, vs in comp.parts[i].items():
                levels[i].setdefault(p, []).extend(vs)
        if st is main:
            pivots.update({p: [round(float(x), 4) for x in v] for p, v in comp.pivots.items()})
    lods = _simplified(levels, "ground")
    pivots = {p: v for p, v in pivots.items() if p in lods[0]}
    joints = _turret_joints(pivots)

    # armour plates and modules, from the hull's and each station's hit body
    dm: list = []
    taken: set = set()

    def add(prefix: str, objs: list, offset: np.ndarray, part_of) -> None:
        for name, v, f, mm, group in objs:
            v = v + offset
            stem = f"{prefix}_{tanks.clean_name(name)}"
            nm, k = stem, 2
            while nm.lower() in taken:
                nm, k = f"{stem}_{k}", k + 1
            taken.add(nm.lower())
            v2, f2 = weld(v, f, 1e-5)
            if len(f2) > DM_BUDGET:
                v2, f2 = simplify({"hull": (v2, f2)}, DM_BUDGET)["hull"]
            if len(f2):
                dm.append((nm, v2, f2, {"part": part_of(v), "group": group, "mm": round(float(mm), 1)}))

    def col_text(path: str | None) -> str | None:
        e = u.get(path.rsplit("/", 1)[-1]) if path else None
        return e.read().decode("latin1", "replace") if e is not None else None

    t = col_text(veh.hitbody)
    if t:
        add("hull", tanks.hit_objects(t, veh.eloss), np.zeros(3), lambda v: "hull")
    for st in veh.stations:
        t = col_text(st.hitbody)
        comp = comps.get(st.index)
        if not t or comp is None:
            continue
        on_turret = _on_turret(st, main)
        if st is main:
            prefix = "turret" if st.full_turn else "mount"
            own = comp.parts[0]

            def part_of(v, own=own):
                return _nearest_part(v, own)
        else:
            prefix = "cupola" if on_turret else "hull"

            def part_of(v, p=("turret" if on_turret else "hull")):
                return p
        add(prefix, tanks.hit_objects(t, st.eloss), st.at, part_of)
    armour = [x for x in dm if x[3]["group"] == "armour"]
    extra = {**extra, "drivable": True, "stations": len(comps)}
    if armour:
        mms = [x[3]["mm"] for x in armour]
        extra.update({"armoured": len(armour), "armourMm": [min(mms), max(mms)]})
    if main is not None and main.aim:
        left, right, down, up = main.aim
        extra.update({"yawLimits": [left, right], "pitchLimits": [-abs(down), up]})
    return pack.add_lods(u.unit, lods, "ground", kind, key=key, pivots=pivots, joints=joints, aliases=aliases, dm=dm,
                         fingerprint=_drivable_fingerprint(u, veh, scripts), extra=extra)


def fingerprint(u: UnitFiles, scripts: dict | None = None) -> str:
    """What a unit's pack entry is made from: its own files, and for a drivable vehicle the scripts it is put together
    from (`Pack.fresh` compares it)."""
    if u.domain == "ground" and scripts:
        veh = drivable(u, scripts)
        if veh is not None:
            return _drivable_fingerprint(u, veh, scripts)
    return u.fingerprint


def _drivable_fingerprint(u: UnitFiles, veh: tanks.Vehicle, scripts: dict) -> str:
    """The unit's own files and the scripts it is put together from."""
    h = hashlib.sha256(u.fingerprint.encode())
    for p in sorted({f"{tanks.SCRIPTS}{u.unit}.txt", *(s.script for s in veh.stations)}):
        e = scripts.get(p)
        if e is not None:
            h.update(f"{p}:{e.size}:{e.archive.name}:{e.offset};".encode())
    for k in sorted(u.files):
        if k.endswith(".col"):
            h.update(f"{k}:{u.files[k].size};".encode())
    return h.hexdigest()[:16]


def _posed(m, args, base, domain, with_pieces):
    # Arguments the .txt does not name stay at its `DefArg=-1` value.
    class _Args(dict):
        def get(self, k, d=None):
            return dict.get(self, k, base)

    return pose_parts(m, _Args(args), domain, with_pieces)
