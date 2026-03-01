# Background

This is written as a response to [this discussion entry](https://github.com/alinnman/celestial-navigation/discussions/43)
The question is interesting, and the solution might be useful for the software repository in the future. 

**IMPORTANT: This note is just a sketch. Not completely worked-out, and it might even be a non-optimal algorithm for the problem at hand.**

# A sketch for an algorithm

## Numerical approach

I have a strong suspicion the problem cannot be solved analytically. Let's apply a numerical solution based on the [Newton-Raphson method (NR)](https://en.wikipedia.org/wiki/Newton%27s_method)

This method solves the equation $F(x)=0$ in this way. 

$x_{n+1}=x_n-\frac{F(x_n)}{F'(x_n)}$

Repeat until<br> $\left| x_{m+1} - x_m \right|<\delta$ or<br> $x_m \notin \left[x_{min}, x_{max}\right]$ or<br> $m > I$<br>

Where $I$ is maximal number of iterations. 
The solution will be $x_m$

Define the NR as a function

$${NR}_1 (F,x_{start},x_{min}, x_{max}, \delta, I)$$

where $F$ is a function (callable)<br>
The function $F$ is called over a range $\left[ x_{min}, x_{max}\right]$ and is started in the point $x_{start}$<br>
(This is since we anticipate $F$ to be executed over a circle $\left[0,2\pi\right]$)

We can simply introduce

$$NR (F,x_{start}, \delta, I) = {NR}_1 (F,x_{start},0, 2\pi, \delta, I)$$

## The calculation 

### Deducing the GP

You need to deduce the Ground Position (GP) of the Sun. 
This is done through interpolation of ephimeris / nautical almanac data. 

### Iterating over the small circle

We iterate over all angles from the GP, and calculate great circles corresponding to all angles $\in [0, 2\pi]$

Now assume we have an angle $\phi$

Let $g$ be the unit vector of the GP on the unit sphere, $N = [0,0,1]$ the North Pole vector, and $r = \frac{\pi}{2} - h$ the angular radius of the small circle of equal altitude (where $h$ is the measured altitude).

First construct the local frame at GP:

$e_g = \mathcal{N}(N \times g)$ (East at GP)

$n_g = \mathcal{N}(g \times e_g)$ (North at GP)

where $\mathcal{N}(\cdot)$ denotes normalization.

The outgoing direction from GP at angle $\phi$ is:

$d_\phi = \sin(\phi) \cdot e_g + \cos(\phi) \cdot n_g$

The great circle extending from the GP with angle $\phi$ is the set of all points reachable by walking from $g$ in direction $d_\phi$. It lies in the plane with normal:

$k_\phi = \mathcal{N}(g \times d_\phi)$

$${\text{circle}_{\text{great}}}_\phi = \lbrace p \in \mathbb{R}^3 \mid p \cdot k_\phi = 0 \land \left|\left|p\right|\right| = 1 \rbrace$$

#### Getting the intersection point

We walk from $g$ along the great circle in direction $d_\phi$ by the angular distance $r$, using the [Rodrigues rotation formula](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula):

$$X_{\text{int}_\phi} = g \cos(r) + d_\phi \sin(r)$$

This point lies simultaneously on the small circle of equal altitude (by construction, since we walked exactly $r$ from GP) and on the great circle defined by $\phi$.

#### Getting the azimuth at the intersection point

Let $p = X_{\text{int}_\phi}$. The local frame at $p$ is:

$e_p = \mathcal{N}(N \times p)$ (East at $p$)

$n_p = \mathcal{N}(p \times e_p)$ (North at $p$)

The direction from $p$ toward GP is:

$d_p = \mathcal{N}(g - p)$

The azimuth at the intersection point is then:

$$A_\phi = \text{arctan2}(d_p \cdot e_p,\ d_p \cdot n_p) \mod 2\pi$$

#### Putting things together for iteration

Now we can model an expression for the NR:

$F_{\text{az},\phi} = A_\phi - A_{\text{measured}}$

Since both $A_\phi$ and $A_{\text{measured}}$ are angles on $[0, 2\pi]$, care must be taken with wrap-around. The residual should be normalised to $(-\pi, \pi]$ to ensure NR steps in the correct direction:

$F_{\text{az},\phi} = \left( A_\phi - A_{\text{measured}} + \pi \right) \mod 2\pi\ - \pi$

### Applying NR to get the result

Choose a starting angle $\phi_{\text{start}}$. A reasonable default is $\phi_{\text{start}} = 0$ (i.e. walking due North from GP), though a better seed can be obtained by a coarse sweep of $F$ over a few sample angles to find the approximate zero crossing.

Then apply:

$$\phi^* = NR\left(F_{\text{az}},\ \phi_{\text{start}},\ \delta,\ I\right)$$

The estimated observer position is:

$$P = X_{\text{int}_{\phi^*}} = g\cos(r) + d_{\phi^*}\sin(r)$$

Convert $P$ back to geodetic latitude and longitude using the standard inverse transformation.

### Possible scenarios where NR might not terminate

**Circumpolar objects (e.g. Polaris).** When the GP is near a pole, the azimuth $A_\phi$ is nearly identical for all points on the small circle. The function $F_{\text{az},\phi}$ becomes essentially flat, its derivative approaches zero, and NR either stalls or diverges. This is the most important failure mode. It can be detected by evaluating the total variation of $F_{\text{az}}$ over a coarse sweep of $\phi \in [0, 2\pi]$ before invoking NR — if the variation is below a threshold $\epsilon$, the measurement carries insufficient positional information and the result should be flagged as unreliable.

**Antipodal GP.** If the observer is near the antipode of GP (altitude $\approx -90°$), the small circle degenerates to a point and the problem is ill-posed.

**Low altitude objects near the horizon.** Atmospheric refraction is largest and least predictable near the horizon, introducing systematic errors into $h$ that propagate directly into the radius $r$ of the small circle, and therefore into $P$.

**Multiple zero crossings.** $F_{\text{az},\phi}$ may have two zero crossings on $[0, 2\pi]$, corresponding to two geometrically valid candidate positions (one in each hemisphere relative to the GP–pole plane). NR will converge to whichever zero is closest to $\phi_{\text{start}}$. A coarse pre-sweep is recommended to identify all approximate zeros, and the physically plausible solution should be selected using any available prior knowledge of the observer's approximate location.

---

## Accuracy Considerations

### Sensor errors

With ~1° error in both azimuth and elevation, the positional accuracy will be
roughly **60–120 nautical miles (110–220 km)**. This is consistent with what
classical celestial navigation achieves with a single sight. Taking multiple
readings over time and combining them as the Sun moves improves accuracy
significantly through the intersection of multiple circles of equal altitude.

### Spherical vs. ellipsoidal Earth

The algorithm above works on a perfect sphere, but the real Earth is a
**WGS-84 ellipsoid**. The GP from the ephemeris is given in geodetic coordinates,
while the algorithm operates in geocentric (spherical) coordinates. The difference
between geodetic and geocentric latitude can reach up to **~11–12 arcminutes
(~20 km)**, which is comparable to or larger than the error from a 1° sensor.

If geodetic GP coordinates are mixed with a spherical solver without conversion,
a **systematic bias** is introduced that will not average out with more
measurements. At ~1° accuracy this is tolerable, but it becomes the dominant
error source if the sensor improves.

### Vertical deflection

The geoid (the true equipotential surface of Earth's gravity) deviates locally
from the ellipsoid. This means that "straight up" — the direction the sensor
references — is not exactly the ellipsoidal normal. This effect is typically a
few arcseconds to about one arcminute, so it is smaller than the current error
budget, but worth being aware of if pushing toward higher accuracy.

### Practical summary

| Error source | Typical magnitude | Dominates at |
|---|---|---|
| Sensor azimuth/elevation (~1°) | 110–220 km | Current level |
| Geocentric vs. geodetic latitude | ~20 km | Sub-1° sensor |
| Geoid vertical deflection | ~0.5–2 km | High-precision work |

At ~1° sensor accuracy the spherical approximation is good enough, but
understanding these layers will help anticipate where the next accuracy wall
is as the hardware improves.

## Final note

I haven't ruled out there is an analytical solution to this problem. 

