# Short description of the workflow and maths of celestial navigation

This is a short description (checklist) of the steps you take when performing
celestial navigation.

*Before we start: All symbols below are in vector notation
and vector algebraic operations are used.
All angles are measured in radians. 
You need to know the difference between spherical coordinates (on a sphere)
and cartesian (3D) coordinates and the conversion formula between them. 
If you don't know these concepts you need to brush up or add up to your maths knowledge*

1. Make (at least) two observations of celestial objects.
<br><br>Using your **sextant** measure the altitude to two celestial objects.
If you use the same celestial object (such as the Sun during daytime)
you need to wait for a while between the measurements.
An hour will typically be sufficient. 
<br>For both measurements take note of the measured altitude, $f_1$ and $f_2$.
<br>Define angles $\alpha$ and $\beta$ this way:
$\alpha = \frac{\pi}{2} - f_1$, $\beta = \frac{\pi}{2} - f_2$
<br><br>Using your **clock** register the corresponding times $t_1$ and $t_2$ 
for the two measurements.<br><br>
1. Look up ground points (GP) in Nautical Almanac
<br><br>
You find the Nautical Almanac [here](NAtrad(A4)_2024.pdf).
You will now need the timestamps $t_1$ and $t_2$ from the step above.<br>
*NOTE: [The toolkit](starfix.py) will take care of the GP calculation,
you just have to extract the tabular data for the current and next hour
if you use the code in the toolkit.*
<br><br>The ground points are represented by two vectors $a$ and $b$.<br>
*The coordinates must be converted from spherical to cartesian before you start.*<br>
*NOTE: You will also need to take care of atmospheric refraction and horizon dip.
For more info see the [readme file](README.md)*
<br><br>
1. Perform a sight reduction
*NOTE: [The toolkit](starfix.py) will take care of the sight reducion work.*
<br><br>Two circles $A$ and $B$ define the
circles of equal altitude defined from the sighting data as described above.
<br><br>
$A = \lbrace p \in \mathbb{R}^3 \mid p \cdot a = \cos \alpha \land |p| = 1 \rbrace$ <br/>
$B = \lbrace p \in \mathbb{R}^3 \mid p \cdot b = \cos \beta \land |p| = 1 \rbrace$<br><br>
Calculate the midpoint $q$ between intersections<br><br>
$q = \mathrm{normalize}((a \times b) \times (a \cos \beta - b \cos \alpha))$<br><br>
Calculate a rotation vector $r$ and a rotation angle $\rho$<br><br>
$r = (a \times b) \times q$ <br/>
$\rho = \arccos\left(\frac{\cos \alpha}{a \cdot q}\right)$<br><br>
Finally apply a rotation operation<br><br>
$p_{\mathrm{rot}} = q \cos \rho + \left( r \times q \right) \sin \rho + r \left(r \cdot q \right)\left(1 - \cos \rho \right)$
<br><br>
Apply the formula above for $\rho$ and $-\rho$ and you will **get the two 
intersection points $p_1$ and $p_2$**.
Convert these vectors back to spherical coordinates. One of these coordinates matches your physical location. 
<br><br>
For more details and background see the [Readme File](README.md).



