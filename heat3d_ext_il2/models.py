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
damaged states and pieces the default pose hides are left out.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import mgm
from .gtp import Entry, read_table
from .modelpack import Pack, simplify, weld

#: graphics/<folder> -> domain.
FOLDERS = {"planes": "air", "vehicles": "ground", "artillery": "ground", "trains": "ground", "ships": "sea"}

#: Pieces left out: muzzle flashes and smoke, lights and their glows, markings, propeller blur, the inner
#: structure shown when a skin piece is shot away (`_wn`, `_nerv`, `stenka`, `_cap`), the cockpit.
_SKIP = re.compile(r"flash|smoke|torec|halo|bano|_light|light_|lamp|glow|decal|fire|trail|shadow|blur|"
                   r"_wn(_|$|\d)|_nerv|stenka|_cap$|^cf_|cockpit|collision|_rot_d|trash", re.I)
#: Damaged and destroyed states: `_D1`.. (a piece shot through), `_D` / `_D_..` / `_d003` (the wreck the game swaps in).
_DAMAGED = re.compile(r"_d[1-9](_|$)|_d_|_d$|_d\d{2,}", re.I)
_GEAR = re.compile(r"gear|wheel|strut|shassi|chassis|oleo|tailwheel|ski(_|\d|$)|truck", re.I)
_TURRET = re.compile(r"turret|tower|bashn|(^|\d_)head", re.I)
_GUN = re.compile(r"gun|barrel|cannon|mantlet|stvol|pushk|(^|\d_)mask", re.I)
_PIECE = re.compile(r"^(.*?)_d0(_|$)", re.I)


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


def pose_parts(model: mgm.Model, args: dict, domain: str, with_pieces: bool = False) -> Posed:
    """The model at its default pose (an aircraft's gear down), split into the viewer's parts."""
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
        elif domain != "air":
            tur = [x for x in line if _TURRET.search(x.name)]
            gun = [x for x in line if _GUN.search(x.name)]
            if gun and tur:
                part = "gun"
                origin.setdefault("gun", world[id(gun[-1])][3, :3])
            elif tur:
                part = "turret"
                origin.setdefault("turret", world[id(tur[-1])][3, :3])
            elif any(_GEAR.search(x.name) for x in line) and domain == "ground":
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


def build_unit(u: UnitFiles, pack: Pack, key: str, kind: str, aliases: list, extra: dict) -> dict:
    """Reads, poses, splits and writes one unit. Raises mgm.MgmError for a model it cannot read."""
    from .modelpack import BUDGET, tris

    args, base = default_args(u)
    srcs = lod_sources(u)
    models: dict = {}
    lods = []
    pivots: dict = {}
    joints: dict = {}
    pieces: dict = {}
    gear_moves = False
    full: dict = {}
    for i, e in enumerate(srcs):
        if e is None:
            continue
        m = models.get(e.name)
        if m is None:
            m = models[e.name] = _read(e)
        posed = _posed(m, args, base, u.domain, with_pieces=(i == 0))
        if i == 0:
            pivots, joints, pieces, gear_moves = posed.pivots, posed.joints, posed.pieces, posed.gear_moves
        parts = {p: weld(*merge_list(v)) for p, v in posed.parts.items()}
        parts = {p: x for p, x in parts.items() if len(x[1])}
        budget = BUDGET.get(u.domain, BUDGET["ground"])[min(i, 2)]
        if i == 0:
            full = parts
        elif full and (tris(parts) < 0.3 * budget or set(full) - set(parts)):
            # the game's coarse form is coarser than the viewer's (some vehicles' 20_ have a few dozen triangles)
            # or has lost a moving part: made from the full model instead
            parts = full
        if not parts:
            continue
        lod = simplify(parts, budget, u.domain)
        if tris(lod) > 1.3 * budget:
            lod = simplify(lod, int(budget * 0.8), u.domain)
        while any(len(v) >= 65535 for v, _ in lod.values()):
            lod = simplify(lod, int(tris(lod) * 0.7), u.domain)
        lods.append(lod)
    if not lods:
        raise mgm.MgmError("no geometry at the default pose")
    while len(lods) < 3:
        lods.append(lods[-1])
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


def _posed(m, args, base, domain, with_pieces):
    # Arguments the .txt does not name stay at its `DefArg=-1` value.
    class _Args(dict):
        def get(self, k, d=None):
            return dict.get(self, k, base)

    return pose_parts(m, _Args(args), domain, with_pieces)
