---
title: Archives without a file table
nav_order: 6
---

# A game whose archives have no file table

IL-2 Series: Korea keeps no readable file table in its archives (the names
are hashed in a block at the end of each archive), and its settings files are
not stored readable. `list` shows its map with the game `Korea`. So:

- its heightmap and water map are found by their header (the `height.dat`
  layout, sectors of 128 samples; a very large grid at a fine cell size);
- it is placed on the earth by fitting the airfields its missions place
  (`data/Missions/**/*.Mission`, read on your machine) to the real airfields'
  published coordinates (`korea.py`): residuals of tens to a few hundred
  metres. The JSON lists each landmark and its residual;
- heightMul and SeaLevel are estimated: ships in the missions sit on the sea,
  so their height over the water map's commonest (sea) value gives the scale.
  Heights come out plausible (the sea below sea level, coastal towns at a few
  metres), not checked further. The JSON marks them estimated.
