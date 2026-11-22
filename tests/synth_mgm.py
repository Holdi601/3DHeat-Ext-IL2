"""Writes small `.mgm` models in the layout `heat3d_ext_il2/mgm.py` reads, for the tests (no game file is used)."""

from __future__ import annotations

import struct

import numpy as np


def _s(text: str) -> bytes:
    b = text.encode("latin1")
    return struct.pack("<I", len(b)) + b


class Writer:
    def __init__(self):
        self.ids: dict = {}
        self.next = 0

    def ref(self, kind: str, obj, body) -> bytes:
        """A reference: the object's fields follow the first time it is written."""
        t = {"model": "class model::Model", "node": "struct model::Node", "chunk": "struct model::Chunk",
             "anim": "struct model::Animation"}[kind]
        key = id(obj)
        if key in self.ids:
            return _s(t) + struct.pack("<I", 0) + _s(self.ids[key])
        self.ids[key] = str(self.next)
        self.next += 1
        return _s(t) + struct.pack("<I", 0) + _s(self.ids[key]) + body()


NULL = _s("") + struct.pack("<I", 0) + _s("")


def mat(t=(0.0, 0.0, 0.0), r=None, s=1.0) -> np.ndarray:
    m = np.eye(4) * s
    m[3, 3] = 1.0
    if r is not None:
        m[:3, :3] = np.asarray(r) * s
    m[3, :3] = t
    return m


class Node:
    def __init__(self, name, parent=None, local=None, arg=0, helper=False):
        self.name = name
        self.parent = parent
        self.local = mat() if local is None else local
        self.offset = mat()
        self.arg = arg
        self.helper = helper
        self.children = []
        self.mesh = None  # (verts, faces)
        self.chunk = None
        self.vrel = self.irel = 0
        if parent is not None:
            parent.children.append(self)


def build(root: Node, anims: list, stride: int = 36) -> bytes:
    """anims: [(arg, [(node, [(t, shown, pos, quat_xyzw_as_written, scale)])])]."""
    nodes = []

    def walk(n):
        nodes.append(n)
        for c in n.children:
            walk(c)

    walk(root)
    for i, n in enumerate(nodes):
        n.index = i
    meshed = [n for n in nodes if n.mesh is not None]
    # one chunk for every mesh, vertices and indices one after another
    verts, idx, voff = [], [], 0
    for n in meshed:
        v, f = n.mesh
        n.vrel = voff * stride
        n.irel = len(idx) * 2
        idx.extend((np.asarray(f).reshape(-1) + voff).tolist())
        verts.append(np.asarray(v, np.float32))
        voff += len(v)
    chunk = object()
    w = Writer()
    body_parts: list[bytes] = []

    def node_body(n):
        def body():
            out = struct.pack("<I", n.index) + _s(n.name) + struct.pack("<6f", *([0.0] * 6))
            out += NULL if n.parent is None else w.ref("node", n.parent, node_body(n.parent))
            out += struct.pack("<I", 0x80000001 if n.helper else (0 if n.mesh is not None else 1))
            out += struct.pack("<16f", *n.local.reshape(-1)) + struct.pack("<I", 0)
            out += struct.pack("<16f", *n.offset.reshape(-1))
            nv = len(n.mesh[0]) if n.mesh is not None else 0
            ni = len(np.asarray(n.mesh[1]).reshape(-1)) if n.mesh is not None else 0
            out += struct.pack("<12I", 0, 0, n.arg, 0, 0, 0, 0, 0, nv, ni, n.vrel, n.irel)
            out += struct.pack("<I", stride) + _s("Specular")
            out += struct.pack("<I", len(n.children))
            for c in n.children:
                out += w.ref("node", c, node_body(c))
            out += bytes([1, 0]) + b"\xff\xff\xff\xff"
            if n.mesh is not None:
                out += w.ref("chunk", chunk, chunk_body) + struct.pack("<I", meshed.index(n))
            else:
                out += NULL
            return out

        return body

    def chunk_body():
        out = _s("Specular") + bytes(16) + struct.pack("<I", 1) + _s("skin.tga")
        out += struct.pack("<IIII", voff, len(idx), VOFF[0], IOFF[0]) + b"\0" + struct.pack("<I", stride)
        out += struct.pack("<I", len(meshed))
        for n in meshed:
            out += w.ref("node", n, node_body(n))
        out += struct.pack("<I", len(meshed))
        for k, n in enumerate(meshed):
            out += struct.pack("<II", n.index, k)
        return out + struct.pack("<I", 0)

    def anim_body(tracks):
        def body():
            out = struct.pack("<I", len(tracks))
            for n, keys in tracks:
                out += struct.pack("<II", n.index | 0x01000000, 36 * len(keys))
                for t, shown, pos, q, sc in keys:
                    out += struct.pack("<f", t) + bytes([0, 0, 1 if shown else 0, 0]) + struct.pack("<3f", *pos)
                    out += struct.pack("<4h", *(int(round(x * 32767)) for x in q))
                    out += struct.pack("<3H", *(int(round(x * 1000)) for x in sc)) + b"\0\0"
            out += struct.pack("<I", len(tracks))
            for n, _ in tracks:
                out += struct.pack("<II", n.index, 0)
            return out

        return body

    VOFF = [0]
    IOFF = [0]
    anim_objs = [object() for _ in anims]
    model_obj = object()
    for _ in range(2):  # the second pass knows where the data lands
        w.ids.clear()
        w.next = 0
        head = w.ref("model", model_obj, lambda: b"")
        head += w.ref("node", root, node_body(root))
        head += struct.pack("<I", len(anims))
        for i, (arg, tracks) in enumerate(anims):
            head += struct.pack("<I", arg) + w.ref("anim", anim_objs[i], anim_body(tracks))
        head += struct.pack("<I", 1) + w.ref("chunk", chunk, chunk_body)
        vbytes = b"".join(np.c_[v, np.zeros((len(v), stride // 4 - 3), np.float32)].astype("<f4").tobytes()
                          for v in verts)
        VOFF[0] = len(head)
        IOFF[0] = len(head) + len(vbytes)
    body_parts = [head, vbytes, np.asarray(idx, "<u2").tobytes()]
    return b"".join(body_parts)


def box(c=(0.0, 0.0, 0.0), s=(1.0, 1.0, 1.0)):
    c, s = np.asarray(c, float), np.asarray(s, float) / 2
    v = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float) * s + c
    f = [[0, 1, 3], [0, 3, 2], [4, 6, 7], [4, 7, 5], [0, 4, 5], [0, 5, 1], [2, 3, 7], [2, 7, 6], [0, 2, 6], [0, 6, 4],
         [1, 5, 7], [1, 7, 3]]
    return v, np.array(f)


def plane() -> bytes:
    """A small aircraft in the game's own node frame (x span, y back, z up under the root's axis turn): a fuselage, a
    propeller hub with two blades spinning about the hub's y (the aircraft's long axis), and a gear leg folding 90 degrees with argument 7.
    Default arguments 0: the gear as modelled (folded up); argument 7 = 1 puts it down."""
    root = Node("Scene Root", local=np.array([[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float))
    body = Node("Fuselage_D0_00", root)
    body.mesh = box((0, 0, 0), (1.0, 8.0, 1.0))
    hub = Node("Dummy_Kok", root, local=mat((0, -4.2, 0)), arg=0)
    for i, ang in enumerate((0.0, np.pi)):
        b = Node(f"Blade{i}", hub, local=mat(r=[[np.cos(ang), np.sin(ang), 0], [-np.sin(ang), np.cos(ang), 0], [0, 0, 1]]))
        b.mesh = box((1.0, 0, 0), (2.0, 0.05, 0.2))
    gear = Node("13300", root, local=mat((1.5, -1.0, -0.4)))
    leg = Node("GearL0_D0_00", gear)
    leg.mesh = box((0, 0.6, 0), (0.15, 1.2, 0.15))  # folded: lying along y (back)
    flash = Node("Flash_20mm", root)
    flash.mesh = box((0, -5, 0), (0.3, 0.3, 0.3))
    spin = [(0.0, True, (0, 0, 0), (0, 0, 0, 1), (1, 1, 1)),
            (0.25, True, (0, 0, 0), (0, 0.7071, 0, 0.7071), (1, 1, 1)),
            (0.5, True, (0, 0, 0), (0, 1, 0, 0), (1, 1, 1)),
            (0.75, True, (0, 0, 0), (0, 0.7071, 0, -0.7071), (1, 1, 1)),
            (1.0, True, (0, 0, 0), (0, 0, 0, -1), (1, 1, 1))]
    # as written: the inverse turn of the gear's swing down about x (the reader turns it back)
    fold = [(0.0, True, (0, 0, 0), (0, 0, 0, 1), (1, 1, 1)),
            (1.0, True, (0, 0, 0), (0.7071, 0, 0, 0.7071), (1, 1, 1))]
    return build(root, [(10225, [(hub, spin)]), (7, [(gear, fold)])])


def plane_txt() -> bytes:
    return b'lod="graphics\\Planes\\Test\\10_Test.MGM",400\r\nDefArg=-1,0.0\r\n'


def _rot_z(deg: float) -> tuple:
    """A turn about z as the file writes it (the reader takes the inverse)."""
    a = np.radians(deg) / 2
    return (0.0, 0.0, -np.sin(a), np.cos(a))


def tank_hull() -> bytes:
    """A drivable tank's hull (x forward, y up, z right; no root turn): a 6 x 1.2 x 3 m body on two tracks, and a 2 m
    whip aerial at the back."""
    root = Node("Scene Root")
    body = Node("body_d0", root)
    body.mesh = box((0, 1.0, 0), (6.0, 1.2, 3.0))
    for side, z in (("L", -1.2), ("R", 1.2)):
        t = Node(f"track{side}_lenta_d0", root)
        t.mesh = box((0, 0.4, z), (6.0, 0.8, 0.5))
    aerial = Node("antenna", root, local=mat((-2.5, 1.6, -1.0)))
    aerial.mesh = box((0, 1.0, 0), (0.02, 2.0, 0.02))
    return build(root, [])


def tank_turret() -> bytes:
    """Its turret, in the turret's own frame (origin on the ring): a 2 x 0.8 x 2 m body, a gun mount 1 m ahead and
    0.3 m up whose 3 m barrel argument 30 turns from 30 degrees up (0) through level (0.5) to 30 degrees down (1),
    and a hatch on the roof that argument 31 swings open (1) or shut (0)."""
    root = Node("Scene Root")
    tur = Node("Dummy_turret", root)
    shell = Node("turret_d0", tur)
    shell.mesh = box((0, 0.4, 0), (2.0, 0.8, 2.0))
    mask = Node("Dummy_gunmask", tur, local=mat((1.0, 0.3, 0.0)))
    gun = Node("gun_d0", mask)
    gun.mesh = box((1.5, 0, 0), (3.0, 0.1, 0.1))
    hatch = Node("Dummy_hatch", tur, local=mat((-0.5, 0.8, 0.0)))
    lid = Node("hatch_d0", hatch)
    lid.mesh = box((0.25, 0.01, 0), (0.5, 0.02, 0.5))
    elev = [(0.0, True, (0, 0, 0), _rot_z(30), (1, 1, 1)),
            (0.5, True, (0, 0, 0), _rot_z(0), (1, 1, 1)),
            (1.0, True, (0, 0, 0), _rot_z(-30), (1, 1, 1))]
    swing = [(0.0, True, (0, 0, 0), _rot_z(0), (1, 1, 1)),
             (1.0, True, (0, 0, 0), _rot_z(90), (1, 1, 1))]
    return build(root, [(30, [(mask, elev)]), (31, [(hatch, swing)])])


def col(objects: dict) -> bytes:
    """A hit body `.col` text file: {name: (verts, faces)}."""
    out = [f"AllObjects = {len(objects)}", ""]
    for i, (name, (v, f)) in enumerate(objects.items()):
        out += [f"[Object = {i}]", f'\tName="{name}"', "", "\tAX=1.0, 0.0, 0.0", "\tPIVOT=0.0, 0.0, 0.0", ""]
        out += [f"\tVertex={k}: {x:.4f}, {y:.4f}, {z:.4f}" for k, (x, y, z) in enumerate(v)]
        out += [""] + [f"\tFace={k}: {a}, {b}, {c}" for k, (a, b, c) in enumerate(f)] + ["", "[End]", ""]
    return "\r\n".join(out).encode("latin1")


def tank_files() -> dict:
    """A drivable tank `_test` as an install holds it: models, hit bodies and scripts (none of them a game file)."""
    g = "/graphics/vehicles/_test/"
    s = "/luascripts/worldobjects/vehicles/"
    hull_col = col({"front_1": box((3.0, 1.0, 0), (0.05, 1.0, 2.8)), "left_1": box((0, 1.0, -1.5), (5.8, 1.0, 0.04)),
                    "ammunition_01": box((0, 0.8, 0.5), (0.6, 0.3, 0.4)), "#wL1": box((1, 0.3, -1.2), (0.6, 0.6, 0.2)),
                    "#^body1000_coll": box((0, 1, 0), (1, 1, 1)), "Dummy_hull": box((0, 1, 0), (5, 1, 2))})
    turret_col = col({"front_1a": box((1.0, 0.4, 0), (0.05, 0.7, 1.8)), "mask_1": box((1.05, 0.3, 0), (0.1, 0.4, 0.5)),
                      "top_1": box((0, 0.8, 0), (1.8, 0.03, 1.8))})
    return {
        g + "_test.mgm": tank_hull(), g + "_10_test.mgm": tank_hull(), g + "_20_test.mgm": tank_hull(),
        g + "_test.txt": b'lod="graphics\\Vehicles\\_Test\\_10_Test.MGM",200\r\nlod="graphics\\Vehicles\\_Test\\_20_Test.MGM",20'
                         b"\r\nDefArg=-1,0\r\n",
        g + "_test-c1-low.mgm": tank_turret(),
        g + "_test-c1-low.txt": b"DefArg=-1,0\r\nDefArg=30,0.4\r\nDefArg=31,1.0\r\n",
        g + "_test_detcoll.col": hull_col, g + "_test-c1_detcoll.col": turret_col,
        s + "_test.txt": (b'object_name = "Test Tank"\r\nVisualImage=0,"graphics\\Vehicles\\_Test\\_Test.mgm",true\r\n'
                          b'HitBody="graphics\\Vehicles\\_Test\\_Test_DetColl.col"\r\n'
                          b'energyloss="front_1",false,50,1\t// x\r\nenergyloss="left_1",false,30,1\r\n'
                          b'energyloss="ammunition_01",true,2,20000\r\nenergyloss="#wL1",true,5,1\r\n'
                          b'energyloss="#^body1000_coll",false,0,1\r\n'
                          b'[attach=1]\r\n\tposition= 0.5,1.6,0.0\r\n\trotation= 0, 0, 0\r\n'
                          b'\tobject = "LuaScripts/WorldObjects/Vehicles/Turrets/_Test_T0.txt"\r\n[end]\r\n'),
        s + "turrets/_test_t0.txt": (b'VisualImage=0,"graphics\\Vehicles\\_Test\\_Test-C1-low.mgm",97\r\n'
                                     b'HitBody="graphics\\Vehicles\\_Test\\_Test-C1_DetColl.col"\r\n'
                                     b"[TurretsPos=0]\r\n\t[Joint=0]\r\n\t\tSectorAngleMin = -180.0\r\n"
                                     b"\t\tSectorAngleMax = 180.0\r\n\t\tAnimationArgNum = 10020\r\n\t[end]\r\n"
                                     b"\t[Joint=1]\r\n\t\tSectorAngleMin = -20.0\r\n\t\tSectorAngleMax = 8.0\r\n"
                                     b"\t\tAnimationArgNum = 301\r\n\t[end]\r\n"
                                     b"\tAimSector=-180, 180, -8, 20\t//AI aim limits\r\n[end]\r\n"
                                     b'energyloss="front_1a",false,50,1\r\nenergyloss="mask_1",false,43,1\r\n'
                                     b'energyloss="top_1",false,10,1\r\n'),
    }
