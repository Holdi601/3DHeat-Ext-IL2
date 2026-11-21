"""
The standalone app's description of this tool (app/spec.py): the IL-2
Sturmovik installs it reads (Great Battles, and IL-2 Series: Korea as far as
it can), their maps (new ones after an update or a new map are found by
app/manifest.py), and how one map becomes a level.
`python -m heat3d_ext_il2.standalone_spec` runs the app from a checkout; the
release executables run the same.
"""

from __future__ import annotations

from pathlib import Path

from . import __version__
from .app.spec import GameSpec, MapSource, Spec

GREAT_BATTLES, KOREA = "Great Battles", "Korea"


def _finder(which: str):
    def find(given: str | None) -> Path | None:
        from .install import _game_name, find_installs

        return next((r for r in find_installs([given] if given else None) if _game_name(r) == which), None)

    return find


def _maps_great_battles(game: Path) -> list[MapSource]:
    """Every `height.hini` of the archives is a map; its sources are the archives holding its files (no decoding)."""
    from .gtp import read_table
    from .hini import parse_hini

    files = {}
    for archive in sorted((game / "data").glob("*.gtp")):
        if archive.name.lower().startswith(("maps", "locations")):
            for e in read_table(archive):
                files.setdefault(e.name, e)
    out: dict[str, MapSource] = {}
    for name, e in sorted(files.items()):
        if not name.endswith("/height.hini"):
            continue
        hini = parse_hini(e.read())
        hm = files.get(hini.path("height_map") or "")
        folder = name.split("/")[-2]
        if hm is None or folder in out:
            continue
        parts = [e, hm, files.get(hini.path("water_map") or ""), files.get(hini.path("water") or ""),
                 files.get(name.rsplit("/", 1)[0] + "/textures.tini")]
        archives = sorted({p.archive for p in parts if p is not None})
        out[folder] = MapSource(folder, folder, archives)
    return list(out.values())


def _maps_korea(game: Path) -> list[MapSource]:
    """The one Korea map; its heightmap is found by its header in the map archives when it is extracted."""
    archives = sorted((game / "data").glob("Maps*.gtp"))
    return [MapSource("korea", "Korea", archives)] if archives else []


def _extract(game: Path, m: MapSource, out: Path, log) -> list[Path]:
    from . import cli

    code = cli.main(["extract", m.id, "--game", str(game), "-o", str(out)])
    if code != 0:
        raise RuntimeError(f"heat3d-il2-level extract exited {code}")
    folder = out / m.id
    return sorted(p for p in folder.iterdir() if p.is_file() and not p.name.startswith("."))


def _game(key: str, label: str, which: str, maps, subdir: str) -> GameSpec:
    return GameSpec(
        key=key, label=label, find=_finder(which), subdir=subdir, maps=maps, extract=_extract,
        existing_outputs=lambda out, m: [out / m.id / f"{m.id}.glb"],
        output_version="0.2.0",
        platforms=("windows-x64", "linux-x64"),
    )


SPEC = Spec(
    id="heat3d-il2",
    name="3DHeat IL-2",
    repo="Holdi601/3DHeat-Ext-IL2",
    version=__version__,
    tools={"heat3d-il2-level": "heat3d_ext_il2.cli:main"},
    default_tool="heat3d-il2-level",
    description="IL-2 Sturmovik maps as 3D levels for the 3DHeat viewer",
    module="heat3d_ext_il2.standalone_spec",
    games=[
        _game("il2", "IL-2 Sturmovik: Great Battles", GREAT_BATTLES, _maps_great_battles, "il2"),
        _game("il2-korea", "IL-2 Series: Korea", KOREA, _maps_korea, "il2-korea"),
    ],
    min_free_gb=2.0,
    notice="Not affiliated with or endorsed by 1C Game Studios / 777 Studios.",
)

if __name__ == "__main__":
    from . import update
    from .app.entry import main

    raise SystemExit(main(SPEC, apply_source=update.apply))
