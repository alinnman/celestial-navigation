<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Short description of the workflow and maths of celestial navigation

This is a short description of the steps you take when performing
celestial navigation.

*Before we start: All symbols below are in vector notation
and vector algebraic operations are used.
(dot and cross products, absolute values, trigonometrics).
All angles are measured in radians.
You need to know the difference between spherical coordinates (on a sphere)
and cartesian (3D) coordinates and the conversion formula between them.
If you don't know these concepts you need to brush up or
add up to your maths knowledge*

1. Make (at least) two observations of celestial objects.
<br><br>Using your **sextant** measure the altitude to two celestial objects.
If you use the same celestial object (such as the Sun during daytime)
you need to wait for a while between the measurements.
An hour will typically be sufficient.
<br>For both measurements take note of the measured altitude, $f_1$ and $f_2$.
<br>Define angles $\alpha$ and $\beta$ this way:
$\alpha = \frac{\pi}{2} - f_1$, $\beta = \frac{\pi}{2} - f_2$
<br><br>Using your **chronometer** (clock) register the corresponding times
$t_1$ and $t_2$
for the two measurements.<br><br>
1. Look up geographic positions (GP) in the **Nautical Almanac**
<br><br>
*You find digital (PDF) Nautical Almanacs bundled in this repository and you can buy hard-copies (for 2024) [here](https://www.amazon.com/Nautical-Almanac-2024-Year/dp/1951116690/ref=sr_1_1?crid=2TIHPIQYLTMSP&dib=eyJ2IjoiMSJ9.d3xFA2pQJx8dny0H5kmiZLliYeANWFYB9BZ8He317-o6bo-502TzFBFZ53Z-urSD2yU0G4GWMfNzJGBe_H332Fm4m7P1csqConMxBzK2PrFKKlWK4lgfJQg6yz6ChRGMazwrBs_sFjCPsPZO70yoju7daDJEfIkEnapIbSINaxPVotcCFWwCbsUZykR9a41qx7pt6f_BF3H2phdzmDyQc91EzxYspG6EUhy4rKSDV84._yKQxdQUbiOyz16NzLeFG1_ZmjRXS9ZH1Cf_qHssoTE&dib_tag=se&keywords=nautical+almanac+2024&qid=1722754135&sprefix=nautical+almanac+2024%2Caps%2C243&sr=8-1).*<br><br>
You will now need the timestamps $t_1$ and $t_2$ from the step above.
Since the Nautical Almanac lists hourly values you will need to perform
[linear interpolation](https://en.wikipedia.org/wiki/Linear_interpolation).
<br><br>
The GP:s are represented by two vectors $a$ and $b$.<br><br>
*NOTE: The coordinates from the Nautical Almanac must be converted from
spherical to cartesian before you start.*<br>
*NOTE: You will also need to take care of atmospheric refraction and horizon
dip.*<br>
*NOTE: [The toolkit](starfix.py) will take care of the GP calculation (with linear interpolation), atmospheric refraction and horizon dip.
You just have to extract the tabular data for the current and next hour
if you use the code in the toolkit.*<br><br>
For more info see the [Readme File](README.md).
<br><br>
1. Perform a sight reduction
<br><br>*NOTE: [The toolkit](starfix.py) will take care of the sight reducion work.*<br>
*NOTE: Old-school celestial navigation on a ship uses*
**sight reduction tables** *as a "cheat" to avoid complex hand-calculations of
the formulas below, and this works perfectly. You can learn about this
[here](https://www.youtube.com/watch?v=hDd1es5oQto&list=PLWcAZhCRTMByW_XEQ0y0OlGmxO3jp0LyE).*
<br><br>Two circles $A$ and $B$ define the
circles of equal altitude defined from the sighting data as described above.
<br><br>
$A = \lbrace p \in \mathbb{R}^3 \mid p \cdot a =
\cos \alpha \land \left|p\right| = 1 \rbrace$ <br/>
$B = \lbrace p \in \mathbb{R}^3 \mid p \cdot b =
\cos \beta \land \left|p\right| = 1 \rbrace$<br><br>
Calculate the midpoint $q$ between intersections of $A$ and $B$.<br><br>
$q = N((a \times b) \times (a \cos \beta - b \cos \alpha))\space;\space N(x) =
\frac{x}{\left|x\right|}$<br><br>
Calculate a rotation vector $r$ and a rotation angle $\rho$<br><br>
$r = \left( a \times b \right) \times q$ <br/>
$\rho = \arccos\left(\frac{\cos \alpha}{a \cdot q}\right)$<br><br>
Finally apply a rotation operation<br><br>
$p_{\mathrm{rot}} = q \cos \rho + \left( r \times q \right) \sin \rho +
r \left(r \cdot q \right)\left(1 - \cos \rho \right)$
<br><br>
Apply the formula above for $\rho$ and $-\rho$ and you will **get the two
intersection points $p_1$ and $p_2$**.
Convert these vectors back to spherical coordinates.
One of these coordinates matches your physical location.
See **yellow markers** in picture below.<br><br>
*The sight reduction can be illustrated with a simple drawing of two circles on
a sphere, with a divider, and then finding the intersections.
The radius of the circles correspond to the measured altitude
of the celestial object, just like Eratosthenes
[found out](https://ui.adsabs.harvard.edu/abs/2018EGUGA..20.5417K/abstract) in 230 BC.*
<br><br>
![Intersection of small circles.](pics/globe-intersect.png "Intersection of small circles.")
<br><br>
For more details, proof of maths used and background see the
[Readme File](README.md). Also note: The shape of the Earth isn't perfectly
spheric. The small deviation (oblateness) is taken care of in this toolkit.
