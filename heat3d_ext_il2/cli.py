"""
`heat3d-il2-level list`, `heat3d-il2-level extract <map>... | --all -o <folder>`, `heat3d-il2-level models`,
`heat3d-il2-level catalog` and `heat3d-il2-level --check [--json]`

Reads the maps of IL-2 Sturmovik: Great Battles (and, as far as it can, IL-2
Series: Korea) from the user's own install and writes each as
`<folder>/<map>/<map>.glb` and `.json`. Prints `ok <glb> <triangles>` or
`failed <map>: <why>` per map; exits 1 when any failed, 2 when no install or
no map was found.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import sys
import traceback
from pathlib import Path

from . import __version__
from .install import all_maps, find_installs
from .level import DEFAULT_MAX_GRID, build


def main(argv: list[str] | None = None) -> int:
    try:
        from . import update

        update.startup("heat3d_ext_il2")
    except Exception:  # an update check never stops a conversion
        pass
    ap = argparse.ArgumentParser(prog="heat3d-il2-level", description="IL-2 Sturmovik maps into 3DHeat .glb levels")
    ap.add_argument("--version", action="version", version=f"heat3d-il2-level {__version__}")
    ap.add_argument("--check", action="store_true", help="say what is found and what is missing, then stop")
    ap.add_argument("--json", action="store_true", help="with --check: as one JSON object")
    ap.add_argument("--levels", help="the 3DHeat levels folder (default: HEAT3D_LEVELS)")
    sub = ap.add_subparsers(dest="cmd")
    ls = sub.add_parser("list", help="list the maps found")
    ls.add_argument("--game", action="append", help="an IL-2 folder (repeatable; default: found through Steam)")
    ex = sub.add_parser("extract", help="extract maps")
    ex.add_argument("maps", nargs="*", help="map names as `list` prints them (wildcards allowed)")
    ex.add_argument("--all", action="store_true",
                    help="every map; seasons that share a heightmap and water map are written once")
    ex.add_argument("-o", "--out", type=Path, required=True, help="output folder; each map goes in <out>/<map>/")
    ex.add_argument("--game", action="append", help="an IL-2 folder (repeatable)")
    ex.add_argument("--max-grid", type=int, default=DEFAULT_MAX_GRID,
                    help=f"heightmap samples a side (default {DEFAULT_MAX_GRID})")
    ex.add_argument("--frame", choices=("enu", "game"), default="enu",
                    help="enu: metres east/altitude/north of --origin, like the watcher's Tacview tables (default); "
                         "game: the game's own metres (x north, y up, z east)")
    ex.add_argument("--origin", nargs=2, type=float, metavar=("LAT", "LON"),
                    help="origin of the enu frame (a recording's geo); default: the map's centre")
    ex.add_argument("--no-water", action="store_true", help="leave the water out")
    ex.add_argument("--no-towns", action="store_true", help="leave the town footprints out")
    ex.add_argument("--skip-existing", action="store_true", help="leave maps whose .glb exists")
    mo = sub.add_parser("models", help="every aircraft, vehicle, gun and ship model as a local 3DHeat model pack")
    mo.add_argument("--game", action="append", help="an IL-2 folder (repeatable)")
    mo.add_argument("-o", "--out", help="the pack folder (default: <levels>/model-packs/il2)")
    mo.add_argument("--units", help="only these units, by folder name (bf109g6,pziv-g,...)")
    mo.add_argument("--domains", help="air,ground,sea (default: all)")
    mo.add_argument("--limit", type=int, help="at most this many units")
    mo.add_argument("--force", action="store_true", help="rebuild units that are up to date")
    mo.add_argument("--levels", default=argparse.SUPPRESS, help="the 3DHeat levels folder (default: HEAT3D_LEVELS)")
    ca = sub.add_parser("catalog", help="the units of your install as <levels>/il2/catalog.json")
    ca.add_argument("--game", action="append", help="an IL-2 folder (repeatable)")
    ca.add_argument("-o", "--out", help="the catalogue file (default: <levels>/il2/catalog.json)")
    ca.add_argument("--list", action="store_true", help="print the units instead of writing the file")
    ca.add_argument("--levels", default=argparse.SUPPRESS, help="the 3DHeat levels folder (default: HEAT3D_LEVELS)")
    args = ap.parse_args(argv)
    from . import modelcli

    if args.check:
        return modelcli.print_check(args)
    if args.cmd is None:
        ap.print_help()
        return 2
    if args.cmd == "models":
        return modelcli.cmd_models(args)
    if args.cmd == "catalog":
        return modelcli.cmd_catalog(args)

    roots = find_installs(args.game)
    if not roots:
        print("IL-2 not found: pass --game <folder> or set HEAT3D_IL2_GAME", file=sys.stderr)
        return 2
    maps = all_maps(roots)
    if args.cmd == "list":
        for m in maps:
            corners = m.hini.corners() if m.hini else None
            where = (f"{min(a for a, _ in corners.values()):.2f}..{max(a for a, _ in corners.values()):.2f} N, "
                     f"{min(b for _, b in corners.values()):.2f}..{max(b for _, b in corners.values()):.2f} E") if corners else (
                f"placed by a landmark fit (rms {m.affine['rmsMetres']} m)" if m.affine else "not placed on the earth")
            if corners and m.affine:
                where += f" per height.hini, which looks wrong: landmark fit (rms {m.affine['rmsMetres']} m) used instead"
            print(f"{m.name}\t{m.game}\theight {m.height.name or m.height.archive.name}\t{where}")
        print(f"{len(maps)} {'map' if len(maps) == 1 else 'maps'} in {', '.join(str(r) for r in roots)}", file=sys.stderr)
        return 0

    wanted = [m for m in maps if args.all or any(fnmatch.fnmatch(m.name, w) for w in args.maps)]
    if args.all:
        seen, unique = set(), []
        for m in wanted:
            key = (m.height.archive, m.height.offset, m.water.offset if m.water else None,
                   tuple(sorted((m.hini.corners() or {}).items())) if m.hini else None)
            if key not in seen:
                seen.add(key)
                unique.append(m)
        wanted = unique
    if not wanted:
        print("no map matches (see `heat3d-il2-level list`)", file=sys.stderr)
        return 2
    failed = 0
    for m in wanted:
        dest = args.out / m.name
        if args.skip_existing and (dest / f"{m.name}.glb").exists():
            print(f"skip {dest / (m.name + '.glb')}")
            continue
        try:
            frame = args.frame if (m.hini and m.hini.corners()) else "game"
            rec = build(m, dest, max_grid=args.max_grid, frame=frame,
                        origin=tuple(args.origin) if args.origin else None, water=not args.no_water, towns=not args.no_towns,
                        log=lambda s: print(s, flush=True))
            tris = sum(p.get("triangles", p.get("cells", 0) * 2) for p in rec["parts"].values())
            print(f"ok {dest / (m.name + '.glb')} {tris} triangles ({rec['frame']['name']} frame)", flush=True)
        except Exception as e:
            failed += 1
            print(f"failed {m.name}: {type(e).__name__}: {e}", flush=True)
            if "HEAT3D_DEBUG" in os.environ:
                traceback.print_exc()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
