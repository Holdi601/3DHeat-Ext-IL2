"""The standalone app on a synthetic Great Battles install: its maps, a real extraction, and a new map found as new."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

import synth
from heat3d_ext_il2.app import entry, paths
from heat3d_ext_il2.standalone_spec import SPEC


def _archive(path: Path, folder: str) -> None:
    yy, xx = np.mgrid[0:40, 0:50]
    raw = (9000 + 30 * xx + 20 * yy).astype(np.uint16)
    corners = {"MapNW": (50.0175, 30.0), "MapNE": (50.0175, 30.035), "MapSE": (50.0, 30.035), "MapSW": (50.0, 30.0)}
    up = folder.upper()
    path.write_bytes(synth.gtp({
        f"/graphics/{folder}/height.dat": synth.height_dat(raw, 32),
        f"/graphics/{folder}/height.hini": synth.hini(rf"graphics\{up}\height.dat", None, corners, 1.0, 36.0),
    }))


@pytest.fixture
def game(tmp_path, monkeypatch):
    lib = tmp_path / "Steam"
    root = lib / "steamapps" / "common" / "IL-2 Sturmovik Battle of Stalingrad"
    (root / "data").mkdir(parents=True)
    _archive(root / "data" / "Maps.gtp", "landscape_x")
    monkeypatch.setattr(paths, "steam_roots", lambda: [lib])
    monkeypatch.delenv("HEAT3D_IL2_GAME", raising=False)
    monkeypatch.setattr("heat3d_ext_il2.install._launcher_folders", lambda: [])
    monkeypatch.setattr("heat3d_ext_il2.update.startup", lambda *a, **k: None)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "appdata"))
    monkeypatch.setenv("HEAT3D_LEVELS", str(tmp_path / "levels"))
    monkeypatch.setenv("HEAT3D_NO_UPDATE", "1")
    return root


def status(capsys) -> dict:
    assert entry.main(SPEC, ["status", "--json"]) == 0
    return {g["game"]: g for g in json.loads(capsys.readouterr().out)["games"]}


def test_find_and_maps(game):
    gb, korea = SPEC.games
    assert gb.find(None) == game and korea.find(None) is None
    maps = gb.maps(game)
    assert [m.id for m in maps] == ["landscape_x"] and maps[0].sources == [game / "data" / "Maps.gtp"]


def test_install_that_gains_a_map(game, tmp_path, capsys):
    g = status(capsys)
    assert g["il2"]["found"] and not g["il2-korea"]["found"] and g["il2"]["counts"]["new"] == 1

    assert entry.main(SPEC, ["extract", "--game", "il2", "--new", "--progress-json"]) == 0
    events = [json.loads(l) for l in capsys.readouterr().out.splitlines() if l.startswith('{"event"')]
    assert events[-1] == {"event": "done", "ok": 1, "failed": 0}
    out = tmp_path / "levels" / "il2"
    assert (out / "landscape_x" / "landscape_x.glb").is_file()
    man = json.loads((out / ".heat3d-extract.json").read_text(encoding="utf-8"))
    assert "il2/landscape_x/landscape_x.glb" in man["entries"]["landscape_x"]["outputs"]

    # An update brings a map in an archive of its own: it is new, the extracted one stays current.
    _archive(game / "data" / "Maps2.gtp", "landscape_y")
    states = {m["id"]: m["state"] for m in status(capsys)["il2"]["maps"]}
    assert states == {"landscape_x": "current", "landscape_y": "new"}
