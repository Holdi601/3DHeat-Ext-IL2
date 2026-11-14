---
title: Speed, tests, terms
nav_order: 7
---

# Speed, tests, terms

## Speed

Decoding is pure Python unless numba is installed (`pip install -e .[fast]`):
a 5632-sample map takes about 15 s without it and about a second with it; the
Korea map's 400 million samples about 7 s with it (the first run also compiles).
Memory stays at one row of sectors plus the output grid.

## Tests

```bash
python -m pytest -q
```

`tests/synth.py` builds archives, heightmaps (an encoder for the codec above),
`height.hini` files and Korea-style archives in code.

## The terms

The licence agreement of IL-2 Sturmovik: Great Battles and IL-2 Series (1C Game
Studios / 777 Studios) was **not found**: not in the install (whose
`data/Licenses.txt` holds only third-party licences), not on the publisher's site,
and the Steam EULA page did not load. Check it yourself before relying on this.
This tool only reads the archives and never changes them. The levels it writes stay
on your machine: **never publish them**. Nothing here ships any game data, and the
tests build every file they read.

## Licence

MIT - see [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Uses numpy (BSD-3-Clause) and, optionally,
numba (BSD-2-Clause). `heat3d_update` is the 3DHeat tools' shared updater.
