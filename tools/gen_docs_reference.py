"""Write docs/cli-reference.md from the code itself, so the reference cannot drift.

The options come from the program's own `--help`; the level's parts and
`.json` keys from a level built from a synthetic install the tests' writers
make.

    python tools/gen_docs_reference.py          # rewrite the page
    python tools/gen_docs_reference.py --check  # exit 1 when the page is stale
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "cli-reference.md"
COMMAND = "heat3d-il2-level"
VERBS = ["list", "extract"]


def run(args):
    env = dict(os.environ, HEAT3D_NO_UPDATE="1", COLUMNS="88", PYTHONIOENCODING="utf-8",
               PYTHONPATH=str(ROOT) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    r = subprocess.run([sys.executable, "-m", "heat3d_ext_il2"] + args, capture_output=True, text=True,
                       env=env, encoding="utf-8", cwd=ROOT)
    return (r.stdout or r.stderr).rstrip()


def outputs():
    sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
    os.environ["HEAT3D_NO_UPDATE"] = "1"
    import numpy as np
    import synth
    from heat3d_ext_il2 import cli
    yy, xx = np.mgrid[0:70, 0:90].astype(float)
    raw = (9300 + 2200 * np.exp(-(((xx - 55) / 18) ** 2 + ((yy - 30) / 14) ** 2))).astype(np.uint16)
    raw[:, :12] = 9000
    water = raw.copy()
    water[:, :12] = 9500
    water[:, 12:] = 0
    corners = {"MapNW": (50.031, 30.0), "MapNE": (50.031, 30.0625), "MapSE": (50.0, 30.0625), "MapSW": (50.0, 30.0)}
    files = {"/graphics/example_map/height.dat": synth.height_dat(raw, 32),
             "/graphics/example_map/height_w.dat": synth.height_dat(water, 32),
             "/graphics/example_map/height.hini": synth.hini(r"graphics\EXAMPLE_MAP\height.dat",
                                                             r"graphics\EXAMPLE_MAP\height_w.dat", corners, 1.0, 36.0)}
    with tempfile.TemporaryDirectory() as tmp:
        game = Path(tmp) / "IL-2"
        (game / "data").mkdir(parents=True)
        (game / "data" / "Maps.gtp").write_bytes(synth.gtp(files))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            cli.main(["extract", "example_map", "--game", str(game), "-o", str(Path(tmp) / "levels"), "--max-grid", "32"])
        folder = Path(tmp) / "levels" / "example_map"
        doc = json.loads((folder / "example_map.json").read_text(encoding="utf-8"))
        raw_glb = (folder / "example_map.glb").read_bytes()
        n = int.from_bytes(raw_glb[12:16], "little")
        nodes = [x.get("name", "") for x in json.loads(raw_glb[20:20 + n])["nodes"]]
    return ["### `<map>.glb` parts", "",
            "Parts of the test level: " + ", ".join(f"`{x.replace('example_map', '<map>')}`" for x in nodes)
            + " (a map with town footprints adds `ground:<map> towns`).", "",
            "### `<map>.json`", "", "Top-level keys: " + ", ".join(f"`{k}`" for k in doc) + ".", ""]


def build():
    out = ["---", "title: Command reference", "nav_order: 90", "---", "", "# Command reference", "",
           "Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.",
           "The other pages explain each command step by step.", "",
           f"## `{COMMAND}`", "", "```text", run(["--help"]), "```", ""]
    for v in VERBS:
        out += [f"## `{v}`", "", "```text", run([v, "--help"]), "```", ""]
    out += ["## Output", ""]
    return "\n".join(out + outputs())


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text(encoding="utf-8") == text else 1)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT))
