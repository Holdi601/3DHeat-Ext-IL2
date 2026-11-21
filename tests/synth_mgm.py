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
