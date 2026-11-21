"""The model reader, posing, part split and pack writer on a model built by `synth_mgm.py` (no game file)."""

from __future__ import annotations

import json
import struct

import numpy as np
import pytest

import synth
import synth_mgm
from heat3d_ext_il2 import catalog, mgm, models
from heat3d_ext_il2.modelpack import Pack


def _model():
    return mgm.read(synth_mgm.plane())


def test_reads_nodes_chunks_and_animations():
    m = _model()
    names = {n.name for n in m.nodes}
    assert {"Scene Root", "Fuselage_D0_00", "Dummy_Kok", "Blade0", "Blade1", "13300", "GearL0_D0_00"} <= names
    assert len(m.chunks) == 1 and m.chunks[0].nv == 8 * 5
    assert [a.arg for a in m.anims] == [10225, 7]
    body = next(n for n in m.nodes if n.name == "Fuselage_D0_00")
    v, f = mgm.node_mesh(m, body, {})
    assert len(f) == 12 and np.allclose(v.max(0) - v.min(0), [1.0, 8.0, 1.0])


def test_not_a_model_is_refused():
    with pytest.raises(mgm.MgmError):
        mgm.read(b"\x00" * 64)
    data = synth_mgm.plane()
    with pytest.raises(mgm.MgmError):
        mgm.read(data[:300])


def test_parts_in_the_figure_frame():
    m = _model()
    p = models.pose_parts(m, {}, "air", with_pieces=True)
    assert set(p.parts) == {"hull", "rotor.1", "gear"}
    hull = np.concatenate([v for v, _ in p.parts["hull"]])
    # x forward (the long axis), y up, z right
    assert hull[:, 0].max() - hull[:, 0].min() == pytest.approx(8.0, abs=1e-4)
    j = p.joints["rotor.1"]
    assert j["axis"] == pytest.approx([1.0, 0.0, 0.0], abs=1e-3)
    assert j["pivot"][0] == pytest.approx(4.2, abs=1e-3)
    assert j["diameter"] == pytest.approx(4.0, abs=0.05)
    gear = np.concatenate([v for v, _ in p.parts["gear"]])
    # the default argument (0) has the leg folded; the pack has it down: 1.2 m below its hinge
    assert gear[:, 1].min() == pytest.approx(-0.4 - 1.2, abs=0.05)
    assert "gear" in p.pivots
    # the flash is left out
    allv = np.concatenate([v for vs in p.parts.values() for v, _ in vs])
    assert allv[:, 0].max() < 5.5
    assert "Fuselage" in p.pieces


def test_key_interpolation_and_visibility():
    k = [mgm.Key(0.0, False, (0, 0, 0), (0, 0, 0, 1), (1, 1, 1)), mgm.Key(1.0, True, (2, 0, 0), (0, 0, 0, 1), (1, 1, 1))]
    m, shown = mgm.key_at(k, 0.5)
    assert m[3, 0] == pytest.approx(1.0) and shown is False
    m, shown = mgm.key_at(k, 1.0)
    assert shown is True


def test_txt_lods_and_default_args():
    t = mgm.parse_txt('lod="graphics\\Planes\\X\\10_X.MGM",400\nDefArg=-1,0.0\t//all\nDefArg=13300,1.0\n')
    assert t["lods"] == [("graphics/planes/x/10_x.mgm", 400.0)]
    assert t["args"] == {-1: 0.0, 13300: 1.0}


def test_pack_from_a_synthetic_install(tmp_path):
    files = {"/graphics/planes/test/test.mgm": synth_mgm.plane(), "/graphics/planes/test/test.txt": synth_mgm.plane_txt()}
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "Planes.gtp").write_bytes(synth.gtp(files))
    units = models.scan(tmp_path)
    assert list(units) == ["planes/test"]
    u = units["planes/test"]
    pack = Pack(tmp_path / "pack", "il2", "test", "heat3d-ext-il2 test")
    e = models.build_unit(u, pack, "Test 1", "fighter", [], {"names": ["Test One"]})
    pack.save()
    idx = json.loads((tmp_path / "pack" / "model-pack.json").read_text(encoding="utf-8"))
    entry = idx["units"]["test"]
    assert entry["name"] == "Test 1" and entry["names"] == ["Test One"] and entry["gear"] == "retract"
    assert entry["parts"] == ["hull", "gear", "rotor.1"] and entry["domain"] == "air"
    glb = (tmp_path / "pack" / e["file"]).read_bytes()
    n = struct.unpack_from("<I", glb, 12)[0]
    g = json.loads(glb[20:20 + n])
    by = {nd["name"]: nd for nd in g["nodes"]}
    assert {"unit", "lod0", "lod1", "lod2", "hull", "gear", "rotor.1", "dm"} <= set(by)
    assert by["rotor.1"]["extras"]["spin"] == "rotor"
    assert by["gear"]["extras"]["retract"] is True
    assert pack.fresh("test", u.fingerprint)


def test_catalog_entries_carry_real_names():
    e = catalog.entry("planes", "bf109g6")
    assert e["key"] == "Bf 109 G-6" and e["domain"] == "air" and e["type"] == "fighter"
    e = catalog.entry("planes", "spitfiremkixe")
    assert "Spitfire LF Mk IX" in e["aliases"]
    assert catalog.entry("vehicles", "_pziv-g")["type"] == "static"
    unknown = catalog.entry("vehicles", "newtank")
    assert unknown["key"] == "newtank" and unknown["class"] == "vehicle"
