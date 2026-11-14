---
title: IL-2 Series: Korea
nav_order: 6
---

# IL-2 Series: Korea

Korea's archives have no readable file table (the names are hashed in a block at
the end of each archive) and its settings files are not stored readable, so:

- its heightmap and water map are found by their header (`height.dat` layout,
  sectors of 128 samples; 19,968 samples a side at 25 m);
- it is placed on the earth by fitting the airfields its missions place
  (`data/Missions/**/*.Mission`, read on your machine) to the real airfields'
  published coordinates (`korea.py`): with the four of the shipped demo missions
  the residuals are 20 to 330 m. The JSON lists each landmark and its residual;
- heightMul and SeaLevel are estimated: ships in the missions sit on the sea, so
  their height over the water map's commonest (sea) value gives the scale. Heights
  of known places come out plausible (the Yellow Sea below sea level, Pyongyang
  and Sinuiju at a few metres), not checked further. The JSON marks them estimated.
