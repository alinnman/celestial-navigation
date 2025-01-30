# Some notes on horizon dip (Al-Biruni)

The dip of the horizon can be calculated with the exact geometric formula

$d(h) = \arccos \left( \frac{R}{R+h}\right)$

where $R$ is the radius for the Earth (${6.378}\times{10^6}$ m),
$h$ is observer elevation.

This expression can also (using simple trigonometrics and application
of Pythagoras' formula) be written as:

$d(h) = \arctan \sqrt{\frac{h^2 + 2h}{R}}$

A common observation is that this formula for lower elevations seems to be
well approximated by this formula for the dip in arcminutes
$d_{\text{amR}}$ where you take **refraction** into account:

$d_{\text{amR}}(h) \approx 1.75 \times \sqrt{h}$

Now let us deduce this approximation.

Let's see what happens for small values of $h$:

$d(h)=\arctan\sqrt\frac{h^2 + 2h}{R} \approx \arctan \sqrt\frac{{2h}}{R}$

It is easy to see that $\arctan$ behaves like a linear function
with derivative $=1$ for low values of $h$:

$\arctan(x) \approx x$

From this we can deduce the approximation:

$d(h) \approx \sqrt{\frac{2}{R}} \times \sqrt{h}$

From this we get the dip in arcminutes:

$d_{\text{am}}(h) \approx \sqrt{\frac{2}{R}} \times \frac{180}{\pi}
\times 60 \times \sqrt{h}$

Calculating this gives this formula where there is **no refraction**:

$d_{\text{am}}(h) \approx 1.93 \times \sqrt{h}$

So we see a difference, for no refraction vs refraction ($1.93$ vs $1.75$).
This can easily be explained through a larger "perceived radius" of
the Earth when refraction is active, and this leads to a lower coeffient in
the formula applicable for refraction above.
