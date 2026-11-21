"""
IL-2 Sturmovik: Great Battles' `.mgm` models, as far as drawing them goes.

Worked out from the files themselves; no game code was read or disassembled.
An `.mgm` is a serialised object graph. Every object is written where it is
first reached and only named after that:

- a reference is a string (u32 length + bytes) naming the type
  (`class model::Model`, `struct model::Node`, `struct model::Chunk`,
  `struct model::Animation`), a u32 (0) and a string id ("1", "17", ...);
  an empty type string and an empty id stand for no object. When the
  (type, id) pair has not been seen before, the object's fields follow at
  once, other objects among them written inline in the same way.
- **Model**: the root node; u32 count and that many (u32 argument,
  animation); u32 count and that many chunks; then the vertex and index
  data, which fill the rest of the file.
- **Node**: u32 index, name, 6 floats (a box), the parent node, u32 kind
  (bit 31: a helper point, no geometry), a 4x4 float matrix (the node's own
  transform against its parent, row vectors), u32, a second 4x4 matrix (the
  geometry's offset from the node: applied to its own vertices only), 12 u32
  (2: the animation argument the node is named for, 3: a sub-index, 8..11:
  vertex count, index count, byte offsets of its vertices and indices within
  its chunk), u32 vertex size, material name, u32 child count and the
  children, two bytes (the first: shown), 4 unused bytes, its chunk and u32
  its place in the chunk's node list.
- **Chunk**: material name, 16 bytes of colours, u32 count and that many
  texture names, u32 vertex count, u32 index count, u32 file offsets of the
  vertices and the indices, a byte, u32 vertex size, u32 count and that many
  nodes (the nodes drawn from it), u32 count and that many (node index, place)
  pairs, u32 count and that many bone nodes (a skinned chunk's; 0 for others). A vertex starts with its position (3 floats); indices are
  16-bit and count from the chunk's first vertex, three to a triangle.
- **Animation**: u32 track count; per track a u32 (low 24 bits: the node
  index, the top byte the key form) and u32 byte length of its keys. Form 1:
  36-byte keys (float time 0..1, three bytes of which the third is 1 when the
  node is shown, a pad byte, 3 floats position, 4 int16 rotation quaternion
  x, y, z, w over 32767, 3 uint16 scale over 1000, a pad). Form 0: 100-byte
  keys (time, 4 bytes, position, quaternion and, at byte 52, scale as floats,
  further values, and at byte 96 the shown flag). Then u32 count and that many (node index, u32) pairs. The
  argument that drives it (0..1 across the keys) is written before it in the
  model. A key's transform applies in the node's own frame, before its
  matrix.

The model's own frame (after the root node's matrix) is x forward, y up and
z right, in metres, about the unit's origin.
"""

from __future__ import annotations

import struct
import sys
from dataclasses import dataclass, field

import numpy as np

_MODEL = "class model::Model"
_NODE = "struct model::Node"
_CHUNK = "struct model::Chunk"
_ANIM = "struct model::Animation"


class MgmError(ValueError):
    pass


@dataclass(eq=False)
class Chunk:
    material: str = ""
    textures: list = field(default_factory=list)
    nv: int = 0
    ni: int = 0
    voff: int = 0
    ioff: int = 0
    stride: int = 0
    nodes: list = field(default_factory=list)
    bones: list = field(default_factory=list)


@dataclass(eq=False)
class Node:
    index: int = 0
    name: str = ""
    parent: "Node | None" = None
    kind: int = 0
    local: np.ndarray = None  # 4x4, row vectors
    offset: np.ndarray = None  # 4x4, the geometry's own offset
    arg: int = 0
    sub: int = 0
    nv: int = 0
    ni: int = 0
    vrel: int = 0
    irel: int = 0
    stride: int = 0
    material: str = ""
    children: list = field(default_factory=list)
    shown: bool = True
    chunk: Chunk | None = None

    @property
    def helper(self) -> bool:
        return bool(self.kind & 0x80000000)


@dataclass
class Key:
    t: float
    shown: bool
    pos: tuple
    quat: tuple  # x, y, z, w
    scale: tuple


@dataclass
class Animation:
    arg: int
    tracks: list  # (node index, [Key])
    nodes: list


@dataclass
class Model:
    root: Node
    nodes: list
    chunks: list
    anims: list
    data: bytes

    def by_index(self) -> dict:
        return {n.index: n for n in self.nodes}


class _Reader:
    def __init__(self, data: bytes):
        self.d = data
        self.p = 0
        self.seen: dict = {}
        self.nodes: list = []
        self.chunks: list = []

    def u32(self) -> int:
        if self.p + 4 > len(self.d):
            raise MgmError("truncated")
        (v,) = struct.unpack_from("<I", self.d, self.p)
        self.p += 4
        return v

    def u8(self) -> int:
        v = self.d[self.p]
        self.p += 1
        return v

    def floats(self, n: int) -> tuple:
        v = struct.unpack_from(f"<{n}f", self.d, self.p)
        self.p += 4 * n
        return v

    def string(self) -> str:
        n = self.u32()
        if n > 4096 or self.p + n > len(self.d):
            raise MgmError(f"bad string length {n} at {self.p - 4}")
        s = self.d[self.p:self.p + n].decode("latin1")
        self.p += n
        return s

    def ref(self, want: str | None = None):
        t = self.string()
        self.u32()
        ident = self.string()
        if not t:
            return None
        if want and t != want:
            raise MgmError(f"expected {want}, found {t!r} at {self.p}")
        key = (t, ident)
        if key in self.seen:
            return self.seen[key]
        if t == _NODE:
            o = Node()
            self.seen[key] = o
            self.node(o)
        elif t == _CHUNK:
            o = Chunk()
            self.seen[key] = o
            self.chunk(o)
        elif t == _ANIM:
            o = self.anim()
            self.seen[key] = o
        else:
            raise MgmError(f"unknown object type {t!r}")
        return o

    def node(self, o: Node) -> None:
        o.index = self.u32()
        o.name = self.string()
        self.floats(6)
        o.parent = self.ref(_NODE)
        o.kind = self.u32()
        o.local = np.array(self.floats(16), np.float64).reshape(4, 4)
        self.u32()
        o.offset = np.array(self.floats(16), np.float64).reshape(4, 4)
        w = struct.unpack_from("<12I", self.d, self.p)
        self.p += 48
        o.arg, o.sub = w[2], w[3]
        o.nv, o.ni, o.vrel, o.irel = w[8:12]
        o.stride = self.u32()
        o.material = self.string()
        n = self.u32()
        if n > 100000:
            raise MgmError(f"bad child count {n}")
        o.children = [self.ref(_NODE) for _ in range(n)]
        o.shown = bool(self.u8())
        self.p += 5
        o.chunk = self.ref(_CHUNK)
        if o.chunk is not None:
            self.u32()
        self.nodes.append(o)

    def chunk(self, o: Chunk) -> None:
        o.material = self.string()
        self.p += 16
        n = self.u32()
        if n > 64:
            raise MgmError(f"bad texture count {n}")
        o.textures = [self.string() for _ in range(n)]
        o.nv, o.ni, o.voff, o.ioff = (self.u32() for _ in range(4))
        self.u8()
        o.stride = self.u32()
        n = self.u32()
        if n > 1_000_000:
            raise MgmError(f"bad node count {n}")
        o.nodes = [self.ref(_NODE) for _ in range(n)]
        m = self.u32()
        if m > 1_000_000:
            raise MgmError(f"bad pair count {m}")
        self.p += 8 * m
        # a skinned chunk's bones (`SkinSpecular`: vertices weighted to several nodes)
        nb = self.u32()
        if nb > 100000:
            raise MgmError(f"bad bone count {nb}")
        o.bones = [self.ref(_NODE) for _ in range(nb)]
        self.chunks.append(o)

    def anim(self) -> Animation:
        n = self.u32()
        if n > 100000:
            raise MgmError(f"bad track count {n}")
        tracks = []
        for _ in range(n):
            h = self.u32()
            ln = self.u32()
            packed = h >> 24 == 1
            size = 36 if packed else 100
            if ln % size or self.p + ln > len(self.d):
                raise MgmError(f"bad key block {ln} (form {h >> 24})")
            keys = []
            for k in range(ln // size):
                at = self.p + size * k
                (t,) = struct.unpack_from("<f", self.d, at)
                pos = struct.unpack_from("<3f", self.d, at + 8)
                if packed:
                    shown = self.d[at + 6] != 0
                    q = [x / 32767.0 for x in struct.unpack_from("<4h", self.d, at + 20)]
                    sc = tuple(x / 1000.0 for x in struct.unpack_from("<3H", self.d, at + 28))
                else:
                    # the full form: floats, and further per-key values (tangents) not used here
                    shown = self.d[at + 96] != 0
                    q = list(struct.unpack_from("<4f", self.d, at + 20))
                    sc = struct.unpack_from("<3f", self.d, at + 52)
                # stored as the inverse turn (a gear leg posed with it as written folds up through the wing)
                keys.append(Key(t, shown, pos, (-q[0], -q[1], -q[2], q[3]), sc))
            self.p += ln
            tracks.append((h & 0xFFFFFF, keys))
        m = self.u32()
        if m > 100000:
            raise MgmError(f"bad node count {m}")
        nodes = [self.u32() for _ in range(2 * m)][::2]
        return Animation(0, tracks, nodes)


def read(data: bytes) -> Model:
    """Reads an `.mgm`; raises MgmError on anything not in the form above (encrypted or another layout)."""
    if data[4:4 + len(_MODEL)] != _MODEL.encode():
        raise MgmError("not a model::Model file (encrypted or another format)")
    r = _Reader(data)
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 20000))
    try:
        t = r.string()
        r.u32()
        r.string()
        root = r.ref(_NODE)
        if root is None:
            raise MgmError("no root node")
        na = r.u32()
        if na > 100000:
            raise MgmError(f"bad animation count {na}")
        anims = []
        for _ in range(na):
            arg = r.u32()
            a = r.ref(_ANIM)
            if a is not None:
                a.arg = arg
                anims.append(a)
        nc = r.u32()
        if nc > 100000:
            raise MgmError(f"bad chunk count {nc}")
        for _ in range(nc):
            r.ref(_CHUNK)
    except (struct.error, IndexError, RecursionError) as e:
        raise MgmError(f"unreadable at {r.p}: {type(e).__name__}") from None
    finally:
        sys.setrecursionlimit(old)
    del t
    return Model(root, r.nodes, r.chunks, anims, data)


# --- posing ------------------------------------------------------------------------------------------------------


def quat_matrix(q) -> np.ndarray:
    """A 4x4 row-vector rotation from a quaternion (x, y, z, w)."""
    x, y, z, w = q
    n = (x * x + y * y + z * z + w * w) ** 0.5 or 1.0
    x, y, z, w = x / n, y / n, z / n, w / n
    r = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y + z * w), 2 * (x * z - y * w)],
                  [2 * (x * y - z * w), 1 - 2 * (x * x + z * z), 2 * (y * z + x * w)],
                  [2 * (x * z + y * w), 2 * (y * z - x * w), 1 - 2 * (x * x + y * y)]])
    m = np.eye(4)
    m[:3, :3] = r
    return m


def _slerp(a, b, f):
    a = np.array(a, np.float64)
    b = np.array(b, np.float64)
    d = float(a @ b)
    if d < 0:
        b, d = -b, -d
    if d > 0.9995:
        q = a + f * (b - a)
    else:
        th = np.arccos(min(1.0, d))
        q = (np.sin((1 - f) * th) * a + np.sin(f * th) * b) / np.sin(th)
    return q / (np.linalg.norm(q) or 1.0)


def key_at(keys: list, t: float) -> tuple[np.ndarray, bool]:
    """A track's transform (4x4, row vectors) and shown flag at argument value `t`: linear between keys, the first
    or last key outside them; shown steps."""
    if not keys:
        return np.eye(4), True
    if t <= keys[0].t:
        a = b = keys[0]
        f = 0.0
    elif t >= keys[-1].t:
        a = b = keys[-1]
        f = 0.0
    else:
        i = next(i for i in range(1, len(keys)) if keys[i].t >= t)
        a, b = keys[i - 1], keys[i]
        f = (t - a.t) / ((b.t - a.t) or 1.0)
    pos = np.array(a.pos) * (1 - f) + np.array(b.pos) * f
    sc = np.array(a.scale) * (1 - f) + np.array(b.scale) * f
    q = _slerp(a.quat, b.quat, f)
    m = np.diag([*sc, 1.0]) @ quat_matrix(q)
    m[3, :3] = pos
    return m, (a.shown if f < 1.0 else b.shown)


def pose(model: Model, args: dict, default: float = 0.0) -> tuple[dict, dict]:
    """Each node's animation transform and shown flag at the given argument values ({arg: value}, others
    `default`)."""
    by = model.by_index()
    tm: dict = {}
    shown: dict = {}
    for a in model.anims:
        v = args.get(a.arg, default)
        for ni, keys in a.tracks:
            n = by.get(ni)
            if n is None:
                continue
            m, s = key_at(keys, v)
            tm[id(n)] = m if id(n) not in tm else m @ tm[id(n)]
            shown[id(n)] = shown.get(id(n), True) and s
    return tm, shown


def world_matrices(model: Model, anim: dict | None = None) -> dict:
    """Each node's transform to the model frame (row vectors): its animation, its own matrix, then its parents'."""
    anim = anim or {}
    out: dict = {}

    def get(n: Node) -> np.ndarray:
        w = out.get(id(n))
        if w is not None:
            return w
        loc = n.local
        a = anim.get(id(n))
        if a is not None:
            loc = a @ loc
        w = loc if n.parent is None else loc @ get(n.parent)
        out[id(n)] = w
        return w

    for n in model.nodes:
        get(n)
    return out


def chunk_positions(model: Model, c: Chunk) -> np.ndarray:
    if c.stride < 12 or c.voff + c.nv * c.stride > len(model.data):
        raise MgmError("chunk vertices outside the file")
    a = np.frombuffer(model.data, np.uint8, c.nv * c.stride, c.voff).reshape(c.nv, c.stride)
    return a[:, :12].copy().view("<f4").reshape(c.nv, 3).astype(np.float64)


def node_mesh(model: Model, n: Node, cache: dict) -> tuple[np.ndarray, np.ndarray] | None:
    """A node's own triangles: (vertices in the node's frame after its offset, faces), or None."""
    c = n.chunk
    if c is None or not n.ni or not n.nv:
        return None
    pos = cache.get(id(c))
    if pos is None:
        pos = cache[id(c)] = chunk_positions(model, c)
    start = c.ioff + n.irel
    if start + 2 * n.ni > len(model.data):
        return None
    idx = np.frombuffer(model.data, "<u2", n.ni - n.ni % 3, start).astype(np.int64)
    if not len(idx) or idx.max() >= len(pos):
        return None
    used, inv = np.unique(idx, return_inverse=True)
    v = np.c_[pos[used], np.ones(len(used))] @ n.offset
    return v[:, :3], inv.reshape(-1, 3)


def parse_txt(text: str) -> dict:
    """A unit's `.txt`: LOD files (lod="path",pixels), default arguments (DefArg=arg,value, -1 for all)."""
    lods, args = [], {}
    for line in text.splitlines():
        line = line.split("//", 1)[0].strip()
        if not line or "=" not in line:
            continue
        k, v = (s.strip() for s in line.split("=", 1))
        kl = k.lower()
        if kl == "lod":
            path, _, px = v.rpartition(",")
            lods.append((path.strip().strip('"').replace("\\", "/").lower(), float(px or 0)))
        elif kl == "defarg":
            a, _, val = v.partition(",")
            try:
                args[int(a)] = float(val)
            except ValueError:
                pass
    return {"lods": lods, "args": args}
