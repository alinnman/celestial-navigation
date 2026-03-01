# Analytical Solution: Deducing Latitude and Longitude from a Single Solar Observation

This document provides the verified mathematical framework to determine an observer's **Latitude ($\phi$)** and **Longitude ($\lambda$)** using a single timestamped observation of the Sun's **Azimuth ($A$)** and **Altitude ($\alpha$)**.

This is based on [this question](https://github.com/alinnman/celestial-navigation/discussions/43) in the discussion forum

## 1. Input Variables
To obtain a unique coordinate, the following four values are required:
*   **$A$**: Solar Azimuth (Degrees clockwise from North, $0^\circ$ to $360^\circ$).
*   **$\alpha$**: Solar Altitude (Degrees above the horizon).
*   **$\delta$**: Solar Declination (Sun's latitude at the UTC timestamp).
*   **$GHA$**: Greenwich Hour Angle (Sun's longitude relative to Greenwich at the UTC timestamp).

---

## 2. Mathematical Derivation

### Step A: Finding Latitude ($\phi$)
The relationship between the celestial equatorial system and the horizontal system is governed by the **Spherical Law of Cosines**:
$$\sin \delta = \sin \alpha \sin \phi + \cos \alpha \cos \phi \cos A$$

To solve for $\phi$ analytically, we treat this as a linear combination of sine and cosine ($a \sin \phi + b \cos \phi = c$):
1.  **$a = \sin \alpha$**
2.  **$b = \cos \alpha \cos A$**
3.  **$c = \sin \delta$**

Using the auxiliary angle identity:
$$R = \sqrt{a^2 + b^2}$$
$$\theta = \mathrm{atan2}(b, a)$$

The latitude is found by:
$$\phi = \arcsin\left(\frac{c}{R}\right) - \theta$$

Note: Mathematically, a second root exists at $\phi_2 = (\pi - \arcsin(c/R)) - \theta$. However, on a physical sphere, only one root will typically fall within the valid range of $[-90^\circ, 90^\circ]$ and remain consistent with the observed azimuth.

### Step B: Finding Longitude ($\lambda$)
Once $\phi$ is known, we find the **Local Hour Angle ($H$)**, which is the angular distance between the observer's meridian and the sun's meridian. We use the four-quadrant inverse tangent $\mathrm{atan2}(y, x)$ to ensure the correct East/West orientation:

1.  **$y$ (East-West component):** $-\sin A \cos \alpha$
2.  **$x$ (North-South component):** $\sin \alpha \cos \phi - \cos \alpha \sin \phi \cos A$

The Local Hour Angle is:
$$H = \mathrm{atan2}(y, x)$$

Finally, calculate the Longitude by referencing the Sun's position relative to Greenwich:
$$\lambda = H - GHA$$

If $\lambda$ falls outside the range $[-180^\circ, 180^\circ]$, normalize by adding or subtracting $360^\circ$.

---

## 3. Geometric Uniqueness
While algebraic formulas involving squares and inverse sines often suggest multiple solutions, the geometry of a sphere ensures a **unique** location for a specific $(A, \alpha, t)$ triplet:

*   **Altitude ($\alpha$)** defines a **Circle of Equal Altitude** centered at the Sun's Geographical Position (GP).
*   **Azimuth ($A$)** defines a **unique radial curve** originating from the Sun's GP toward the observer.
*   The intersection of a radial line and a circle centered at the origin occurs at exactly **one point**. Any secondary "mathematical" roots are artifacts where the Sun would be below the horizon or the azimuth would be reversed by $180^\circ$.

---

## 4. Implementation Notes
*   **Sign Conventions:** Azimuth must be $0^\circ$ to $360^\circ$ (North-Clockwise).
*   **Angular Units:** Ensure all trigonometric functions in code (like `sin`, `cos`, `atan2`) receive inputs in **radians**.
*   **Coordinate Range:** Latitude $(\phi)$ results in $[-90^\circ, 90^\circ]$ and Longitude $(\lambda)$ results in $[-180^\circ, 180^\circ]$.
