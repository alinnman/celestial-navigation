<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

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

$\arctan(h) \approx h$ (when $x$ is small)

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

From this we can also calculate the radius, if we know the coefficient of the square root formula. 

So we observe

$d_{\text{am}}(h) \approx k \times \sqrt{h}$<br>
where $k = 1.75$ (refraction) or $1.93$ (no refraction)

From the calculation above it is easy to calculate the radius $R$

$k = \sqrt{\frac{2}{R}} \times \frac{180}{\pi}
\times 60$

from which we get

$R = \frac{{180}^2 \times {60}^2 \times 2}{{\pi}^2 \times k^2}
\approx \frac {2.364 \times 10^7}{k^2}$

From this we can easily get the radius of the Earth ($R$) just like Al-Biruni did in 1017 AD (it is about $6300$ km)

