# Proof 1: Celestial Navigation: Mathematical Proof of Earth's Sphericity and Practical Algorithm

## Introduction

Celestial navigation provides both practical positioning methods and fundamental geometric proof of Earth's spherical nature. This document presents both the theoretical proof that Earth must be spherical based on observational data, and the practical vector-algebraic algorithm which can be used in modern celestial navigation software (such as [this toolkit](../README.md)).

## Part I: Theoretical Proof of Earth's Sphericity

### Problem Statement

Given the observational formula for celestial object altitude:
$$a = 90 - \frac{d}{111.1}$$

Where:
- $a$ = altitude of celestial object (degrees)
- $d$ = distance from observer to GP (km)  
- $GP$ = geographical position (point where object is at zenith)

**Theorem:** This relationship can only occur on a spherical Earth with very distant celestial objects.

### Mathematical Proof

**Step 1: Universal Constraint**

For ANY point on Earth's surface at distance $d$ from the GP of a celestial object, the altitude follows:
$$a = 90 - \frac{d}{111.1}$$

This must hold for ALL observers at ALL possible distances $d$ from any GP.

**Step 2: Geometric Interpretation**

The altitude $a$ represents the angle between the local horizontal plane and the line to the celestial object. For distant objects, this equals the angle between:
- The local normal to Earth's surface (zenith direction)
- The direction from GP to observer (projected from Earth's center)

**Step 3: Surface Curvature Constraint**

For the linear relationship to hold universally, consider observers at distances $d_1$ and $d_2$ from a GP. The difference in altitude angles must equal:
$$\Delta a = \frac{d_2 - d_1}{111.1}$$

This means the **angular separation** between any two points, as measured from Earth's center, must be exactly proportional to their surface distance with constant $111.1$ km/degree.

**Step 4: Uniqueness of Spherical Geometry**

This constant ratio between arc length and central angle $(s = r\theta)$ is the **defining property** of a sphere with radius $r$.

For ANY other surface:
- **Ellipsoid**: The ratio $\frac{s}{\theta}$ varies with position
- **Flat surface**: No central angle exists; relationships are trigonometric, not linear
- **Any irregular surface**: Ratio varies with position and direction

**Step 5: Mathematical Derivation**

On a sphere of radius $R$:
$$s = R \times \frac{\pi}{180} \times \theta_{\text{degrees}}$$

For our formula $a = 90 - \frac{d}{111.1}$ to match $a = 90 - \theta$:
$$\frac{180}{\pi R} = \frac{1}{111.1}$$

Therefore: 
$$R = \frac{180 \times 111.1}{\pi} \approx 6371 \text{ km}$$

**Conclusion:** The linear relationship can **ONLY** occur on a perfect sphere of radius ≈ 6371 km.

## Part II: Practical Sight Reduction Algorithm

*The following describes the vector-algebraic algorithm used in modern celestial navigation software (such as [this toolkit](../README.md)) to determine position from celestial observations.*

### Workflow Overview

The sight reduction process converts sextant measurements into precise geographic position through the following steps:

*The following description can also be found [here](../WORKFLOW.md)*

### Step 1: Make Celestial Observations

Using a **sextant**, measure the altitude to two celestial objects:
- Record measured altitudes: $f_1$ and $f_2$
- Define angles: $\alpha = \frac{\pi}{2} - f_1$, $\beta = \frac{\pi}{2} - f_2$
- Using a **chronometer**, register corresponding times: $t_1$ and $t_2$

### Step 2: Determine Geographic Positions (GP)

From the **Nautical Almanac**, obtain GP coordinates for times $t_1$ and $t_2$:
- Perform linear interpolation for precise timing
- Convert from spherical to Cartesian coordinates
- Apply corrections for atmospheric refraction and horizon dip
- Result: Position vectors $\mathbf{a}$ and $\mathbf{b}$ representing the GPs

### Step 3: Vector-Algebraic Sight Reduction

**Define Circles of Equal Altitude:**

Two circles $A$ and $B$ define the circles of equal altitude:

$$A = \lbrace \mathbf{p} \in \mathbb{R}^3 \mid \mathbf{p} \cdot \mathbf{a} = \cos \alpha \land |\mathbf{p}| = 1\rbrace $$

$$B = \lbrace \mathbf{p} \in \mathbb{R}^3 \mid \mathbf{p} \cdot \mathbf{b} = \cos \beta \land |\mathbf{p}| = 1\rbrace $$

**Calculate Intersection Midpoint:**
$$\mathbf{q} = N((\mathbf{a} \times \mathbf{b}) \times (\mathbf{a} \cos \beta - \mathbf{b} \cos \alpha))$$

where<br>$N(\mathbf{x}) = \frac{\mathbf{x}}{|\mathbf{x}|}$

**Calculate Rotation Parameters:**

Calculate the midpoint $q$ between intersections of $A$ and $B$.

$$q = N((a \times b) \times (a \cos \beta - b \cos \alpha))$$

$$\mathbf{r} = (\mathbf{a} \times \mathbf{b}) \times \mathbf{q}$$

$$\rho = \arccos\left(\frac{\cos \alpha}{\mathbf{a} \cdot \mathbf{q}}\right)$$

**Apply [Rodrigues' Rotation Formula](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula):**
$$\mathbf{p}_{\text{rot}} = \mathbf{q} \cos \rho + (\mathbf{r} \times \mathbf{q}) \sin \rho + \mathbf{r}(\mathbf{r} \cdot \mathbf{q})(1 - \cos \rho)$$

**Final Result:**
Apply the formula for both $+\rho$ and $-\rho$ to get two intersection points $\mathbf{p}_1$ and $\mathbf{p}_2$. Convert back to spherical coordinates - one represents your physical location.

**Note:**
The result we get above is a pure **spherical** sight reduction, performed on the unit sphere. In reality the Earth is an oblate spheroid, and you also need to enter corrections
for atmospheric refraction and horizon dip. These are added as (smaller) coorections in a real-world implementation. 

## Part III: Mathematical Connection

### Why the Algorithm Requires a Spherical Earth

The vector-algebraic sight reduction algorithm **fundamentally depends** on Earth's sphericity:

1. **Circle of Equal Altitude**: The equation $\mathbf{p} \cdot \mathbf{a} = \cos \alpha$ defines a perfect circle on a sphere. On any other surface, these would not be circles.

2. **Constant Relationship**: The algorithm assumes the linear relationship $\alpha = \frac{\pi}{2} - f$ holds universally - which our proof shows only occurs on a sphere.

3. **Vector Operations**: The cross products and dot products work precisely because we're operating on a unit sphere where all positions satisfy $|\mathbf{p}| = 1$.

4. **Intersection Geometry**: Two circles on a sphere intersect at exactly two points. This elegant geometric property breaks down on other surfaces.

### Historical Validation

Traditional celestial navigation used **sight reduction tables** rather than vector algebra, but relied on the same spherical trigonometry principles. The constant 111.1 km/degree appears in all navigation systems because:

- Ancient Greek measurements (Eratosthenes, ~200 BC)
- Islamic astronomical observations (Al-Ma'mun, 9th century)  
- Modern satellite geodesy

All confirm the same fundamental relationship that proves Earth's sphericity.

## Implementation Notes

*For software development and practical work:*

- **Atmospheric Corrections**: Apply refraction and dip corrections before sight reduction
- **Interpolation**: Use linear interpolation for almanac data between tabulated hours
- **Coordinate Conversion**: Ensure proper conversion between spherical (latitude/longitude) and Cartesian (x,y,z) coordinates
- **Precision**: Modern GPS requires meter-level accuracy, but celestial navigation will only reach about 1 nautical miles accuracy, due to the simple mechanical devices (sextant and clock). This requires careful manual work. 

The algorithm's success in providing accurate positioning for centuries demonstrates that Earth must indeed be spherical, as any other geometry would cause systematic errors that would accumulate and render the method useless.

---

## Supporting Academic Sources

### Fundamental Mathematical and Geometric Sources

**Classical Texts:**
- Todhunter, Isaac. "Spherical Trigonometry for the Use of Colleges and Schools" (19th century)
- "Heavenly Mathematics: The Forgotten Art of Spherical Trigonometry" (Princeton University Press)

**Mathematical Foundations:**
- Wikipedia: "Spherical trigonometry"  
  https://en.wikipedia.org/wiki/Spherical_trigonometry
- Wikipedia: "Geodesic"  
  https://en.wikipedia.org/wiki/Geodesic
- Wikipedia: "Differential geometry"  
  https://en.wikipedia.org/wiki/Differential_geometry

### Celestial Navigation and Applied Mathematics

**Navigation Theory:**
- Academia.edu: "Mathematics for Celestial Navigation"  
  https://www.academia.edu/35773055/Mathematics_for_Celestial_Navigation
- Astro Navigation Demystified: "Spherical Trigonometry Introduction"  
  https://astronavigationdemystified.com/spherical-trigonometry-introduction/
- Wikipedia: "Navigational triangle"  
  https://en.wikipedia.org/wiki/Navigational_triangle

**Historical Context:**
- Physics Today: "Trigonometry for the heavens" (2017)  
  https://pubs.aip.org/physicstoday/article/70/12/70/904108/Trigonometry-for-the-heavensThe-stars-and-planets

### Geodesy and Earth Sciences

**Earth Shape and Measurement:**
- Wikipedia: "Geodesy"  
  https://en.wikipedia.org/wiki/Geodesy
- Wikipedia: "Figure of the Earth"  
  https://en.wikipedia.org/wiki/Figure_of_the_Earth
- NOAA National Ocean Service: "The Figure of the Earth"  
  https://oceanservice.noaa.gov/education/tutorial_geodesy/geo03_figure.html

### Key Supporting Facts

1. Historical measurements confirm "111.3 km per degree and 40,068 km circumference"
2. The cosine rule is "the fundamental identity of spherical trigonometry"
3. For a sphere, "geodesics are great circles" enabling precise navigation calculations
4. Vector algebra provides exact solutions that validate spherical Earth geometry
