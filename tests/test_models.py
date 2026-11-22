"""The model reader, posing, part split and pack writer on a model built by `synth_mgm.py` (no game file)."""

from __future__ import annotations

import json
import struct

import numpy as np
import pytest

import synth
import synth_mgm
from heat3d_ext_il2 import catalog, mgm, models, tanks
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
    # a folder starting with "_" is the vehicle the player drives (Tank Crew), not scenery
    e = catalog.entry("vehicles", "_pziv-g")
    assert e["type"] == catalog.entry("vehicles", "pziv-g")["type"] != "static" and e["drivable"] is True
    unknown = catalog.entry("vehicles", "newtank")
    assert unknown["key"] == "newtank" and unknown["class"] == "vehicle"


def _tank_pack(tmp_path):
    files = synth_mgm.tank_files()
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "Vehicles.gtp").write_bytes(synth.gtp({k: v for k, v in files.items() if k.endswith(".mgm")}))
    (tmp_path / "data" / "Scripts.gtp").write_bytes(synth.gtp({k: v for k, v in files.items() if not k.endswith(".mgm")}))
    units = models.scan(tmp_path)
    scripts = models.vehicle_scripts(tmp_path)
    u = units["vehicles/_test"]
    pack = Pack(tmp_path / "pack", "il2", "test", "heat3d-ext-il2 test")
    e = models.build_unit(u, pack, "Test", "tank", [], {}, scripts=scripts)
    glb = (tmp_path / "pack" / e["file"]).read_bytes()
    n = struct.unpack_from("<I", glb, 12)[0]
    return e, json.loads(glb[20:20 + n]), glb[20 + n + 8:], u, scripts


def test_hit_body_and_scripts():
    files = synth_mgm.tank_files()
    objs = tanks.read_col(files["/graphics/vehicles/_test/_test_detcoll.col"].decode("latin1"))
    assert [o[0] for o in objs][:3] == ["front_1", "left_1", "ammunition_01"] and objs[0][1].shape == (8, 3)
    el = tanks.energyloss(files["/luascripts/worldobjects/vehicles/_test.txt"].decode("latin1"))
    assert el["front_1"] == (False, 50.0, 1.0) and el["ammunition_01"] == (True, 2.0, 20000.0)
    hits = tanks.hit_objects(files["/graphics/vehicles/_test/_test_detcoll.col"].decode("latin1"), el)
    # the 0 mm dummy, the helper without a thickness and the unnamed one are left out
    assert {h[0]: (h[3], h[4]) for h in hits} == {"front_1": (50.0, "armour"), "left_1": (30.0, "armour"),
                                                 "ammunition_01": (2.0, "ammo"), "#wL1": (5.0, "wheel")}
    assert tanks.clean_name("#^1HullScreenL_01") == "HullScreenL_01" and tanks.clean_name("front_4a") == "front_4a"
    assert [tanks.group_of(n) for n in ("fueltank_1", "engine", "transmission_2", "radiator", "#track_L_bot",
                                        "#trackCover1004_coll", "sight1_1050", "#^gun", "turretGN_01", "#mask_3b")] ==         ["fuel", "engine", "transmission", "radiator", "tracks", "structure", "optics", "gun", "drive", "armour"]


def test_drivable_tank_put_together(tmp_path):
    e, g, _bin, u, scripts = _tank_pack(tmp_path)
    assert e["parts"] == ["hull", "aerial", "gear", "turret", "gun"] and e["drivable"] is True
    # the hull from the listed levels (its plain model holds the inside), the turret at its attach point
    assert e["joints"]["turret"] == {"joint": "yaw", "pivot": [0.5, 1.6, 0.0]}
    assert e["joints"]["gun"]["pivot"] == pytest.approx([1.5, 1.9, 0.0], abs=1e-3)
    assert e["joints"]["gun"]["parent"] == "turret"
    assert e["yawLimits"] == [-180.0, 180.0] and e["pitchLimits"] == [-8.0, 20.0]
    # the body's size (hull and gun) leaves the aerial out; the hatch the defaults open is shut (roof at 1.6 + 0.8 m)
    assert e["length"] == pytest.approx(7.5, abs=0.02) and e["height"] == pytest.approx(2.42, abs=0.02)
    by = {n["name"]: n for n in g["nodes"]}
    assert by["turret"]["extras"]["joint"] == "yaw" and by["gun"]["extras"]["joint"] == "pitch"
    # the gun level (the default argument would have it 6 degrees off): the muzzle as high as the trunnion
    assert e["box"][3] == pytest.approx(0.5 + 1.0 + 3.0, abs=0.02)
    dm = {n["name"][3:]: n["extras"] for n in g["nodes"] if n.get("name", "").startswith("dm:")}
    assert dm["hull_front_1"] == {"part": "hull", "group": "armour", "mm": 50.0}
    assert dm["hull_ammunition_01"]["group"] == "ammo" and dm["hull_wL1"]["group"] == "wheel"
    assert dm["turret_mask_1"]["part"] == "gun" and dm["turret_top_1"] == {"part": "turret", "group": "armour", "mm": 10.0}
    assert "hull_body1000_coll" not in dm and "hull_Dummy_hull" not in dm
    assert e["armoured"] == 5 and e["armourMm"] == [10.0, 50.0]
    assert models.fingerprint(u, scripts) == e["fingerprint"] != u.fingerprint
