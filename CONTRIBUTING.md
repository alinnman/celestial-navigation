
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
*Working on this right now. Sight reductions seem to work well.*
1. Better mapping functions.<br/>
*Currently implementing mapping based on the*
*[Folium](https://github.com/python-visualization/folium) framework.*
*Also investigating methods for handling map data without an*
*internet connection.*
1. Create a lightweight web application and/or mobile app without requiring
internet access. <br/>
*A collection of simple Jupyter notebooks have been added, and this may be good*
*enough for practical work. Have also started developing a proper app based*
*on Kivy. This may be a candidate for a proper Android and/or iOS app*
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

Some notes on development [here](DEVELOPMENT.md).

Any contributions are welcome!
