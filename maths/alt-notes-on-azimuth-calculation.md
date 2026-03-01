# Analytical Solution: Deducing a Unique Lat/Lon from Solar Position

This document defines the mathematical procedure to determine an observer's **Latitude ($\phi$)** and **Longitude ($\lambda$)**. Given a unique timestamp and the sun's position in the sky, there is only one physical location on Earth where these variables coincide.

## 1. Known Variables
The calculation requires four inputs:
*   **$A$**: Solar Azimuth (Degrees clockwise from North).
*   **$\alpha$**: Solar Altitude (Degrees above the horizon).
*   **$\delta$**: Solar Declination (Sun's latitude at timestamp).
*   **$GHA$**: Greenwich Hour Angle (Sun's longitude at timestamp).

---

## 2. The Analytical Derivation

### Step A: Finding Latitude ($\phi$)
We begin with the fundamental equation of the celestial triangle:
$$\sin \delta = \sin \alpha \sin \phi + \cos \alpha \cos \phi \cos A$$

To solve for $\phi$, we transform this into a linear combination of sine and cosine:
1.  Let $a = \sin \alpha$
2.  Let $b = \cos \alpha \cos A$
3.  Let $c = \sin \delta$

The equation becomes $a \sin \phi + b \cos \phi = c$. We solve this using the $R\sin(\phi + \theta)$ identity:
$$R = \sqrt{a^2 + b^2}$$
$$\theta = \mathrm{atan2}(b, a)$$
$$\phi = \arcsin\left(\frac{c}{R}\right) - \theta$$

**Note on Uniqueness:** While the inverse sine and the square root in the derivation of $R$ can mathematically suggest two roots, only one latitude will satisfy the simultaneous requirement of the observed azimuth and the sun's declination within the bounds of a sphere.

### Step B: Finding Longitude ($\lambda$)
Once $\phi$ is determined, we find the **Local Hour Angle ($H$)**. This is the angular distance between the observer's meridian and the sun's meridian.

Using the components of the horizontal system:
1.  **$y$ (East-West component):** $-\sin A \cos \alpha$
2.  **$x$ (North-South component):** $\cos \alpha \sin \phi \cos A - \cos \phi \sin \alpha$

We use the four-quadrant inverse tangent to find $H$:
$$H = \mathrm{atan2}(-\sin A \cos \alpha, \cos \alpha \sin \phi \cos A - \cos \phi \sin \alpha)$$

Finally, translate the Local Hour Angle into Longitude:
$$\lambda = H - GHA$$

*If $\lambda$ falls outside the range $[-180^\circ, 180^\circ]$, normalize by adding or subtracting $360^\circ$.*

---

## 3. Geometric Clarification of Uniqueness

It is a common misconception in navigation algebra that two positions exist for one observation. This is debunked by the intersection of geometric loci:

1.  **The Circle of Equal Altitude:** An altitude $\alpha$ places you on a "Small Circle" centered at the Sun's Geographical Position (GP).
2.  **The Azimuth Curve:** An azimuth $A$ defines a specific path originating from the Sun's GP. 

On a sphere, a radial line (the azimuth) extending from a point (the GP) can only intersect a circle centered at that same point at **one unique location**. Any "second solution" appearing in the algebra is a mathematical artifact (a "ghost" point) where the sun would technically be on the opposite side of the Earth or the azimuth would be $180^\circ$ reversed.

---
