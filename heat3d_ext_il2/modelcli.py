"""
The `models`, `catalog` and `--check` commands of `heat3d-il2-level`.

`models` writes `<levels>/model-packs/il2/` (one `.glb` per unit and `model-pack.json`), `catalog` writes
`<levels>/il2/catalog.json`. `<levels>` is `--levels`, else `HEAT3D_LEVELS`. Both read the user's own Great Battles
install only; a model that does not read as described in `mgm.py` is skipped and named. IL-2 Series (Korea) keeps
its file names hashed, so its models are not found and the run says so.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

from . import __version__, catalog, mgm, models
from .install import find_installs
from .modelpack import Pack, write_catalog

GAME = "il2"
SOURCE = f"heat3d-ext-il2 {__version__}"


def _great_battles(roots: list[Path]) -> tuple[Path | None, list[str]]:
    notes = []
    gb = None
    for r in roots:
        if (r / "bin" / "game" / "IL2Series.exe").exists():
            notes.append(f"{r}: IL-2 Series (Korea) keeps its archives' file names hashed; its models are not read")
        elif gb is None and any((r / "data").glob("Planes*.gtp")):
            gb = r
    return gb, notes


def game_build(root: Path) -> str:
    """A fingerprint of the install's model archives (their names, sizes and dates): changes with a game update."""
    h = hashlib.sha256()
    for a in sorted((root / "data").glob("*.gtp")):
        if a.name.lower().startswith(("planes", "vehicles", "ships", "scripts")):
            st = a.stat()
            h.update(f"{a.name}:{st.st_size}:{int(st.st_mtime)};".encode())
    return "gtp-" + h.hexdigest()[:12]


def levels_folder(given: str | None) -> Path | None:
    lv = given or os.environ.get("HEAT3D_LEVELS")
    return Path(lv) if lv else None


def _pick(units: dict, args) -> list:
    out = []
    want = {u.strip().lower() for u in (args.units or "").split(",") if u.strip()}
    domains = {d.strip() for d in (args.domains or "air,ground,sea").split(",") if d.strip()}
    for key, u in sorted(units.items(), key=lambda kv: (["air", "ground", "sea"].index(kv[1].domain), kv[0])):
        if want and u.unit.lower() not in want and key.lower() not in want:
            continue
        if u.domain not in domains:
            continue
        out.append(u)
    return out[: args.limit] if args.limit else out


def cmd_models(args) -> int:
    roots = find_installs(args.game)
    gb, notes = _great_battles(roots)
    for n in notes:
        print(n, file=sys.stderr)
    if gb is None:
        print("IL-2 Sturmovik: Great Battles not found: pass --game <folder> or set HEAT3D_IL2_GAME", file=sys.stderr)
        return 2
    lv = levels_folder(args.levels)
    out = Path(args.out) if args.out else (lv / "model-packs" / GAME if lv else None)
    if out is None:
        print("no output folder: pass -o <folder> or --levels <levels folder>, or set HEAT3D_LEVELS", file=sys.stderr)
        return 2
    units = models.scan(gb)
    picked = _pick(units, args)
    if not picked:
        print("no unit matches (see `heat3d-il2-level catalog --list`)", file=sys.stderr)
        return 2
    pack = Pack(out, GAME, game_build(gb), SOURCE)
    names = models.object_names(gb)
    scripts = models.vehicle_scripts(gb)
    done = skipped = failed = 0
    t0 = time.time()
    for i, u in enumerate(picked):
        e = catalog.entry(u.folder, u.unit, names.get(u.unit, ""))
        if not args.force and pack.fresh(u.unit, models.fingerprint(u, scripts)):
            skipped += 1
            continue
        try:
            # the game's own name is also an id its recordings give the unit
            entry = models.build_unit(
                u, pack, e["key"], e["type"], [e["gameName"]] if e["gameName"] != u.unit else [],
                {"displayName": e["gameName"], "names": e["aliases"], "class": e["class"], "nation": e["nation"],
                 "folder": u.folder}, scripts=scripts)
            done += 1
            print(f"ok {u.folder}/{u.unit} {entry['file']} {'/'.join(map(str, entry['tris']))} triangles"
                  f"{' ' + ','.join(entry['parts']) if len(entry['parts']) > 1 else ''}", flush=True)
        except mgm.MgmError as err:
            failed += 1
            print(f"skipped {u.folder}/{u.unit}: {err}", flush=True)
        except Exception as err:  # noqa: BLE001 - one unit never stops the run
            failed += 1
            print(f"failed {u.folder}/{u.unit}: {type(err).__name__}: {err}", flush=True)
        if (i + 1) % 20 == 0:
            pack.save()
    pack.save()
    size = sum((out / x["file"]).stat().st_size for x in pack.index["units"].values() if (out / x["file"]).is_file())
    print(f"{done} written, {skipped} up to date, {failed} skipped or failed; {len(pack.index['units'])} units in "
          f"{out} ({size / 1e6:.0f} MB) in {time.time() - t0:.0f} s", file=sys.stderr)
    return 1 if failed and not done and not skipped else 0


def cmd_catalog(args) -> int:
    roots = find_installs(args.game)
    gb, notes = _great_battles(roots)
    for n in notes:
        print(n, file=sys.stderr)
    if gb is None:
        print("IL-2 Sturmovik: Great Battles not found: pass --game <folder> or set HEAT3D_IL2_GAME", file=sys.stderr)
        return 2
    units = models.scan(gb)
    names = models.object_names(gb)
    items = []
    taken: set = set()
    # A unit's id is what the game's own logs and recordings call it (its object name, "Bf 109 G-6"); a second folder
    # of the same name keeps its folder name.
    for key, u in sorted(units.items(), key=lambda kv: (kv[1].unit.startswith("_"), kv[0])):
        e = catalog.entry(u.folder, u.unit, names.get(u.unit, ""))
        uid = e["gameName"] if e["type"] != "static" and e["gameName"].lower() not in taken else u.unit
        taken.add(uid.lower())
        items.append({"id": uid, "kind": "vehicle", "name": e["gameName"], "key": e["key"], "names": e["aliases"],
                      "aliases": e["aliases"], "class": e["class"], "nation": e["nation"], "domain": e["domain"],
                      "type": e["type"], "folder": u.folder, "unit": u.unit,
                      "model": f"model-packs/{GAME}/{catalog.safe_id(u.unit)}.glb"})
    if args.list:
        for it in items:
            print(f"{it['folder']}/{it['unit']}\t{it['key']}\t{it['name']}\t{it['class']}\t{it['nation']}\t"
                  f"{', '.join(it['aliases'])}")
        return 0
    lv = levels_folder(args.levels)
    path = Path(args.out) if args.out else (lv / GAME / "catalog.json" if lv else None)
    if path is None:
        print("no output: pass -o <catalog.json> or --levels <levels folder>, or set HEAT3D_LEVELS", file=sys.stderr)
        return 2
    write_catalog(path, GAME, game_build(gb), SOURCE, items)
    print(f"{len(items)} units -> {path}", file=sys.stderr)
    return 0


def check(args) -> dict:
    """What the tool needs and whether it is there, as the 3DHeat extractor manager reads it."""
    roots = find_installs(getattr(args, "game", None))
    gb, notes = _great_battles(roots)
    lv = levels_folder(getattr(args, "levels", None))
    checks = [{"id": "install", "label": "IL-2 Sturmovik: Great Battles", "ok": gb is not None,
               "detail": str(gb) if gb else "not found: pass --game <folder> or set HEAT3D_IL2_GAME"}]
    if gb is not None:
        arch = sorted(p.name for p in (gb / "data").glob("*.gtp") if p.name.lower().startswith(("planes", "vehicles")))
        checks.append({"id": "models", "label": "Model archives", "ok": bool(arch),
                       "detail": f"{len(arch)} archives" if arch else "no Planes*.gtp / Vehicles*.gtp in data"})
        maps = sorted(p.name for p in (gb / "data").glob("Maps*.gtp"))
        checks.append({"id": "maps", "label": "Map archives", "ok": bool(maps),
                       "detail": f"{len(maps)} archives" if maps else "no Maps*.gtp in data"})
    for n in notes:
        checks.append({"id": "korea", "label": "IL-2 Series (Korea)", "ok": True, "detail": n})
    if lv is not None:
        free = shutil.disk_usage(lv if lv.exists() else lv.anchor).free
        checks.append({"id": "disk", "label": "Free disk space", "ok": free > 2e9,
                       "detail": f"{free / 1e9:.0f} GB free; a full model pack takes about 0.3 GB, a map 1-2 GB"})
    return {"version": __version__, "levels": str(lv) if lv else None, "checks": checks}


def print_check(args) -> int:
    c = check(args)
    if getattr(args, "json", False):
        print(json.dumps(c))
    else:
        for x in c["checks"]:
            print(f"{'ok' if x['ok'] else 'MISSING':8s}{x['label']}: {x['detail']}")
    return 0 if all(x["ok"] for x in c["checks"]) else 1
