"""
IL-2 Sturmovik's `.gtp` archives, as far as reading files out of them goes.

Worked out from the archives themselves; no game code was read or disassembled.
Two forms are on this machine:

- **Great Battles** (`data/Maps*.gtp` and the rest): a header `S16R`, then a
  table `STRMFAT?` of records, `DIR!` (folders) and `FILE`, each a tag, seven
  32-bit words and a NUL-terminated path. For `FILE` the words are: 1, the
  offset of the entry, its size, a hash, the parent folder's index, the path's
  length with its NUL, 0. At the offset sits a 32-byte entry header
  (`STRMFILE`, the size, zeros, the absolute offset of the data) and then
  `size` bytes of the file, stored as they are (no compression, no encryption).
- **IL-2 Series (Korea)**: the same entries, `STRMFILE` header and data, one
  after another from the start of the file, with no readable name table (the
  archive ends in a block that holds the names hashed). Files are found there
  by what they hold, not by name: `scan_chain` lists every entry's offset and
  size, and the caller sniffs.
"""

from __future__ import annotations

import os
import struct
from dataclasses import dataclass
from pathlib import Path


class GtpError(ValueError):
    pass


@dataclass(frozen=True)
class Entry:
    archive: Path
    name: str  # lower case, '/'-separated, from the archive's own table; '' in a Korea archive
    offset: int  # of the 32-byte STRMFILE header
    size: int  # of the data after it

    def read(self, limit: int | None = None) -> bytes:
        with self.archive.open("rb") as fh:
            fh.seek(self.offset)
            head = fh.read(32)
            if head[:8] != b"STRMFILE":
                raise GtpError(f"{self.archive.name}@{self.offset}: no STRMFILE header")
            return fh.read(self.size if limit is None else min(limit, self.size))


def read_table(archive: str | Path) -> list[Entry]:
    """The named entries of a Great Battles archive; [] for an archive without a table (Korea)."""
    archive = Path(archive)
    with archive.open("rb") as fh:
        head = fh.read(48)
        if head[:4] != b"S16R":
            return []
        if head[32:40] != b"STRMFAT?":
            raise GtpError(f"{archive.name}: S16R without a STRMFAT table")
        (table_size,) = struct.unpack_from("<I", head, 40)
        fh.seek(32)
        table = fh.read(table_size + 64)
    out: list[Entry] = []
    p = 32  # the first record follows the 32-byte STRMFAT header
    while p + 32 <= len(table):
        tag = table[p : p + 4]
        if tag not in (b"DIR!", b"FILE"):
            break
        words = struct.unpack_from("<7I", table, p + 4)
        n = words[5]
        name = table[p + 32 : p + 32 + n].split(b"\0", 1)[0].decode("latin1")
        if tag == b"FILE":
            out.append(Entry(archive, name.lower(), words[1], words[2]))
        p += 32 + n
    return out


def scan_chain(archive: str | Path) -> list[Entry]:
    """Every entry of an archive read as a chain of STRMFILE entries (Korea), unnamed."""
    archive = Path(archive)
    size = os.path.getsize(archive)
    out: list[Entry] = []
    with archive.open("rb") as fh:
        p = 0
        while p + 32 <= size:
            fh.seek(p)
            head = fh.read(32)
            if head[:8] != b"STRMFILE":
                break
            (n,) = struct.unpack_from("<I", head, 8)
            out.append(Entry(archive, "", p, n))
            p += 32 + n
    return out
