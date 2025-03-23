
<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Contributing to the project

Anyone is invited to contribute to this project,
either by supplying sight reduction algorithm-related material,
including improvements of the existing code.

Actual sights are also welcome, in addition to the samples provided.

I have started a
[discussion forum](https://github.com/alinnman/celestial-navigation/discussions)
where anyone is invited to discuss anything related to celestial navigation.

# Future plans

Regarding future plans for this project.
These are some things I may consider doing (or have already started)

1. Building on WGS-84 ellipsoid model.<br/>
*Working on this right now. Sight reductions seems to work well but accurate*
*mapping does not work yet.*
1. Better mapping functions.<br/>
*Currently using the*
*[MapDevelopers circle functions](https://www.mapdevelopers.com/draw-circle-tool.php) (web-based). Considering*
*building functionality on GeoPandas or similar framework.*
1. Create machine-readable Nautical Almanac<br/>
*This will greatly improve workflow speed*
1. Create a lightweight web application and/or mobile app without requiring
internet access. <br/>
*A collection of simple Jupyter notebooks have been added, and this may be good*
*enough for practical work. There are however bugs in current Jupyter*
*implementations on Android.*
1. Diagnostic output for describing the underlying maths.
(Mainly for the notebooks)<br/>
*Working on this right now.*
1. Diagnostic code for measuring accuracy<br/>
*Working on this right now.*
1. More elaborate sextant calibration code.
1. Code for Lunar Distance measurements.

But the design goal is **portability and a small footprint**,
with no dependency on an internet connection.
Keeping it runnable in a lightweigth Python environment is desirable,
with the mobile phone as the natural choice of hardware.

Any contributions are welcome!
