# Why an off-axis circle projects to an ellipse

This note gives the mathematical foundation for a fact used repeatedly in
star-trail arguments: viewing a circle from a direction not aligned with its
central axis produces an image that is an ellipse.

The short version: projecting the circle's plane onto the image plane is a
*linear* map (for a distant object, i.e. parallel rays) or a *projective* map
(for a nearby object, i.e. perspective). Linear maps carry circles to ellipses.
Projective maps carry circles to conics. Both cases are worked out below,
because they give slightly different guarantees and the difference matters if
an opponent tries to nitpick.

## 1. Parallel projection (distant object, the exact-ellipse case)

Write the circle of radius $r$ centred at $c$, lying in a plane spanned by
orthonormal vectors $u$ and $v$:

$$C = \lbrace\, c + r\cos t\,u + r\sin t\,v \;:\; t \in [0,2\pi) \,\rbrace$$

Orthographic projection $\pi : \mathbb{R}^3 \to \mathbb{R}^2$ (drop the component
along the viewing direction) is linear, so it distributes over the
parametrisation. Set $\mathbf{a} = \pi(u)$, $\mathbf{b} = \pi(v)$,
$\mathbf{c}_0 = \pi(c)$:

$$\pi(C) = \lbrace\, \mathbf{c}_0 + r\cos t\,\mathbf{a} + r\sin t\,\mathbf{b} \,\rbrace$$

Let $M = [\,\mathbf{a}\ \ \mathbf{b}\,]$ be the matrix with those columns. A point
of the image is $\mathbf{x} = \mathbf{c}_0 + M\mathbf{w}$ with
$\mathbf{w} = r(\cos t, \sin t)^\top$, so $\lvert \mathbf{w}\rvert = r$.

If $\mathbf{a}$ and $\mathbf{b}$ are linearly independent, $M$ is invertible.
Then $\mathbf{w} = M^{-1}(\mathbf{x} - \mathbf{c}_0)$, and the constraint
$\lvert \mathbf{w}\rvert^2 = r^2$ becomes

$$(\mathbf{x} - \mathbf{c}_0)^\top\, Q\, (\mathbf{x} - \mathbf{c}_0) = r^2,
\qquad Q = (M^{-1})^\top M^{-1} = (M M^\top)^{-1}$$

$Q$ is symmetric positive-definite whenever $M$ is invertible. A level set of an
SPD quadratic form is by definition an ellipse, with principal axes the
eigenvectors of $Q$ and semi-axis lengths $r/\sqrt{\lambda_i}$. That is the
whole proof.

### The foreshortening formula

To recover the familiar foreshortening, tilt the circle's plane by an angle
$\theta$ about an axis lying in the image plane. Then $u$ stays in the image
plane, so $\pi(u) = (1,0)$, and $v$ tips out of it, so $\pi(v) = (0,\cos\theta)$.
Here $M = \mathrm{diag}(1, \cos\theta)$ and

$$\frac{X^2}{r^2} + \frac{Y^2}{(r\cos\theta)^2} = 1$$

This is an ellipse with semi-axes $r$ and $r\cos\theta$, and eccentricity

$$e = \sin\theta$$

The diameter along the tilt axis projects at full length $2r$. The
perpendicular diameter foreshortens to $2r\cos\theta$.

## 2. Perspective projection (nearby object, the general case)

Put the eye at the origin $O$. The circle $C$ lies in some plane not passing
through $O$. Each point of $C$ is seen along a ray
$\lbrace s\,p : s > 0,\ p \in C\rbrace$, and the union of these rays is a
**cone** $K$ with apex $O$. The image on the sensor is $K \cap \Pi$, where
$\Pi$ is the image plane (not through $O$).

The cone $K$ is a quadric surface. The circle satisfies a plane equation
$n \cdot x = c$ and a sphere equation $\lvert x - m\rvert^2 = \rho^2$. Along a
ray write $x = s\,p$. The plane fixes $s = c / (n \cdot p)$. Substituting into
the sphere equation and clearing the denominator gives a homogeneous
degree-two equation in $p$, which is exactly the equation of a quadric cone.

The classical theorem finishes it: every plane section of a quadric cone is a
conic, i.e. an ellipse, a parabola, or a hyperbola. So a perspective image of a
circle is in general a conic. It is specifically an ellipse when $\Pi$ meets
every generator of the cone on the same side of the apex. Equivalently, when the
whole circle lies in front of the observer and does not cross the plane through
the eye parallel to the image plane (the vanishing plane).

That condition holds for any normal act of looking at a circle, so the everyday
claim is true. Stated with full generality, though, the image is a conic, not
always an ellipse. That distinction is worth keeping in reserve, since it is the
kind of precision a bad-faith opponent will probe. For the ellipse case,
Dandelin's spheres give the two foci constructively.

## 3. The two extremes are the same theorem

The relation $e = \sin\theta$ absorbs both edge cases without special pleading.

- On-axis viewing is $\theta = 0$, giving $e = 0$: a circle, which is just an
  ellipse with equal axes.
- Perfectly edge-on viewing is $\theta = 90^\circ$, giving $e \to 1$: the minor
  axis vanishes and the ellipse degenerates to a line segment.

Circle, ellipse, and flat line are not three separate phenomena. They are one
continuous family indexed by the tilt.

## 4. Application to star trails

For star trails the perspective/cone argument is the operative one. A star
sweeps a genuine circle of directions about the celestial pole. The pinhole
optics turn that circle of directions into a cone. The sensor slices the cone
into a conic.

The load-bearing point against a flat-plane "perspective illusion" account is
not the shape of any single arc. It is the global structure: one common axis,
concentric nested curves, a uniform angular rate, and the whole family a rigid
section of a single cone. A square-root law cannot come out of linear
perspective, and neither can a coherent single-axis rotation field.
