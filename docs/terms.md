---
title: Speed, tests, terms
nav_order: 7
---

# Speed, tests, terms

## Speed

Decoding is pure Python unless numba is installed (`python -m pip install -e .[fast]`):
a mid-sized map takes about 15 s without it and about a second with it; the
largest map, several hundred million samples, about 7 s with it (the first
run also compiles). Memory stays at one row of sectors plus the output grid.

## Tests

```bash
python -m pytest -q
```

`tests/synth.py` builds archives, heightmaps (an encoder for the codec above),
`height.hini` files and archives without a file table in code.

## The terms

This tool reads the archives of your own IL-2 Sturmovik: Great Battles
installation on your computer and never changes them.

Nothing from the game is shipped or redistributed: no game files, no game
code, no DLLs; the tests build every file they read. The levels it writes stay
on your machine.

3DHeat IL-2 is not affiliated with or endorsed by 1C Game Studios / 777
Studios. IL-2 Sturmovik and related names and trademarks belong to their
owners.

Rights holders: open an issue at
[github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) -
we respond quickly and remove anything on request.

## Licence

MIT - see [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Uses numpy (BSD-3-Clause) and, optionally,
numba (BSD-2-Clause). `heat3d_ext_il2.update` is the 3DHeat tools' shared updater.
