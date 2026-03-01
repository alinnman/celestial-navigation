# Analytical Solution: Deducing Lat/Lon from Solar Position

**NOTE: This is just a draft. It hasn't been verified**

This document provides the mathematical framework to determine an observer's **Latitude ($\phi$)** and **Longitude ($\lambda$)** using the Sun's **Azimuth ($A$)**, **Altitude ($\alpha$)**, and a **Timestamp** (to determine the Sun's Geographical Position).

## 1. Known Variables
From your observation and the nautical almanac (at a specific UTC timestamp), we have:
*   **$A$**: Solar Azimuth (Degrees from North).
*   **$\alpha$**: Solar Altitude (Degrees above the horizon).
*   **$\delta$**: Solar Declination (Sun's latitude).
*   **$GHA$**: Greenwich Hour Angle (Sun's longitude relative to Greenwich).

---

## 2. Mathematical Derivation

### Step A: Finding Latitude ($\phi$)
Using the Spherical Law of Cosines for the zenith distance, we relate the coordinates:
$$\sin \delta = \sin \alpha \sin \phi + \cos \alpha \cos \phi \cos A$$

To solve for $\phi$ analytically, we treat this as a linear combination of sine and cosine ($a \sin \phi + b \cos \phi = c$):
1.  Let $a = \sin \alpha$
2.  Let $b = \cos \alpha \cos A$
3.  Let $c = \sin \delta$

The solution is:
$$\phi = \mathrm{atan2}(a, b) \pm \arccos\left(\frac{c}{\sqrt{a^2 + b^2}}\right)$$

### Step B: Finding Longitude ($\lambda$)
Once $\phi$ is known, we find the **Local Hour Angle ($H$)**. We use the relationship between the horizontal and equatorial systems:
$$\sin H = \frac{-\sin A \cos \alpha}{\cos \delta}$$
$$\cos H = \frac{\sin \alpha - \sin \phi \sin \delta}{\cos \phi \cos \delta}$$

Using $\mathrm{atan2}(\sin H, \cos H)$ provides the full-circle value of $H$. Finally:
$$\lambda = H - GHA$$

---

## 3. Notes on Ambiguity
There are mathematically two points on Earth where the sun appears at the exact same altitude and azimuth at any given moment. 
*   **Hemisphere Check:** One solution is usually in the "wrong" hemisphere. If you know your approximate location, you can discard the incorrect result.
*   **Convergence:** If the sun is near the local meridian (Solar Noon), the two potential solutions converge into a single point.
*   **Normalization:** The resulting longitude should be normalized to the range $[-180^\circ, 180^\circ]$ to follow standard GPS conventions.
