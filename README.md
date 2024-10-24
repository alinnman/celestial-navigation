<!---
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# celestial-navigation

## Table of contents

1. [Introduction](#introduction)
1. [Making Sights](#making-sights)
    1. [Atmospheric Refraction](#atmospheric-refraction)
    1. [Dip of Horizon](#dip-of-horizon)
    1. [Ignored Corrections](#ignored-corrections)
1. [Sight Reduction](#sight-reduction)
    1. [Using two sights](#using-two-sights)
    1. [Using three or more sights](#using-three-or-more-sights)
    1. [Running the chicago script](#run-chicago-script)
1. [Dead Reckoning](#dead-reckoning)
    1. [Running the sea script](#run-sea-script)
1. [A real-life example](#real-life)
1. [Terrestrial Navigation](#terrestrial)
1. [Sextant Calibration](#calibration)
1. [Chronometer Handling](#chronometer)

## 1. Introduction <a name="introduction"></a>

![US Navy training in celestial navigation](pics/us-navy.jpg "US Navy Training in Celestial Navigation")

This project contains a toolkit (written in Python) to be used for
[celestial navigation](https://en.wikipedia.org/wiki/Celestial_navigation)
together with some demos and documentation.
Sights (altitude measurements) have to be obtained using a sextant,
a nautical almanac and an accurate chronometer.
The toolkit takes care of the **sight reduction**
(conversion to estimated location on Earth),
a task that traditionally is performed with careful manual work using special
tables (sight reduction tables), pen, dividers and specialized plotting charts.
Using a calculator can speed up this manual task, and also reduce possible
(human) errors.
A **computer** can do it even quicker, and this toolkit will typically perform
a sight reduction in less than one millisecond.  
You can use the toolkit on a mobile phone without internet connection.
If you also have access to a solar powered battery (powerbank) you have a tool
useful while traveling in remote places or on the ocean.

* The toolkit supports **stationary** observations, i.e. when observations are
  made from a single position,
  using multiple sights where the position is determined from the intersection(s)
  of the small circles of equal altitude.
  For two sights you will get two possible coordinates.
  For three or more sights you will get one coordinate
  (calculated as a mean value).
* There is also support for **dead reckoning** observations,
  typically at sea on a moving ship. This also needs a working compass and a
  chip log or similar.
  See [section 4](#dead-reckoning) below for more information.
* As a bonus there is also support for **terrestial navigation**.
  See [Section 6](#terrestrial) below for more information.

For more information on installation and usage of the Python scripts see [here](INSTALL.md).

A short explanation of the logical steps and algorithms used in this toolkit can
be found [here](WORKFLOW.md).

Digital versions of the Nautical Almanac for [2024](NAtrad(A4)_2024.pdf)
and [2025](NAtrad(A4)_2025.pdf)
are included in this repository.

A more detailed description of celestial navigation can be found [here](https://www.waypointamsterdam.com/Handy_stuf/Short_Guide_To_Astro_navigation.pdf).<br>

A historical document, the Admiralty Navigational Manual (1938),
from His Majestys Stationary Office (UK) can be found [here](https://archive.org/details/dli.ernet.211556/mode/2up).

If you wonder why I wrote this in the first place, then see [this short explanation](WHY.md).

If you want to contribute to the project then see [this page](CONTRIBUTING.md).

## 2. Making sights <a name="making-sights"></a>

You create a sight with code like this (for the Sun). You specify data from your
sextant and chronometer. You also add tabular data from the
Nautical Almanac. This data is given from the current hour of the observation,
and the next hour. (You don't have to enter linear factors etc. from the almanac).

    a = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 5,\
              time_day             = 5,\
              time_hour            = 15, \
              time_minute          = 55, \
              time_second          = 18, \
              gha_time_0_degrees   = 45, \
              gha_time_0_minutes   = 50.4, \
              gha_time_1_degrees   = 60, \
              gha_time_1_minutes   = 50.4, \
              decl_time_0_degrees  = 16, \
              decl_time_0_minutes  = 30.6, \
              decl_time_1_degrees  = 16, \
              decl_time_1_minutes  = 31.3, \
              measured_alt_degrees = 55, \
              measured_alt_minutes = 8, \
              measured_alt_seconds = 0 \
              )

You can also see a complete example in [a python script](starfixdata.stat.1.py)
and also [a corresponding excel file](chicago.ods).
This sample is built using altitudes taken from a star atlas Stellarium
<https://en.wikipedia.org/wiki/Stellarium_(software)> from a point in central
Chicago on May 5th 2024.
In other words: No sextant readings were made and the accuracy is very good.
(Running this sample will give you an accuracy of just some 100 meters).

The data is picked from your chronometer (clock), sextant and the Nautical Almanac
in the following way. Arguments in *italics* are optional.

| Argument | Description                                  | Remark                                                         | Collected From |
| :-------------       | :-------------                               | :-------------                                                 | :------------- |
| object               | Name of celestial object.                     | Only mnemonic.                                                  | N/A |
| time_year            | Current year.                                 | In UTC.                                                         | Chronometer |
| time_month           | Current month (1-12).                               | In UTC.                                                         | Chronometer |
| time_day             | Current day of month (1-31).                        | In UTC.                                                         | Chronometer |
| time_hour            | Observation time - Hours (0-23).              | In UTC.                                                        | Chronometer |
| time_minute          | Observation time - Minutes (0-59).            | In UTC.                                                        | Chronometer |
| *time_second*        | Observation time - Seconds (0-59).            | In UTC. Default = 0.   | Chronometer |
| gha_time_0_degrees   | GHA degrees reading for this hour.            | For stars use GHA of Aries.                                    | Nautical Almanac |
| gha_time_0_minutes   | GHA minutes reading for this hour (0-60).           | Can be zero (use decimal degrees). For stars use GHA of Aries. | Nautical Almanac |
| gha_time_1_degrees   | GHA degrees reading for next hour.            | For stars use GHA of Aries.                                    | Nautical Almanac |
| gha_time_1_minutes   | GHA minutes reading for next hour (0-60).            | Can be zero (use decimal degrees). For stars use GHA of Aries. | Nautical Almanac |
| decl_time_0_degrees  | Declination degrees reading for this hour (-90 - 90).    |   |  Nautical Almanac |
| decl_time_0_minutes  | Declination minutes reading for this hour (0-60).   | Can be zero (use decimal degrees).                              | Nautical Almanac |  
| *decl_time_1_degrees*  | Declination degrees reading for next hour (-90 - 90). | Can be skipped for stars. Default = decl_time_0_degrees | Nautical Almanac |
| *decl_time_1_minutes*  | Declination minutes reading for next hour (0-60). | Can be skipped for stars. Can be zero (use decimal degrees). Default = decl_time_1_minutes | Nautical Almanac |
| *sha_diff_degrees*   | SHA of star vs Aries in degrees.              | Only use for stars. Otherwise skip. Default = 0. | Nautical Almanac |
| *sha_diff_minutes*  | SHA of star vs Aries in minutes (0-60). | Only use for stars. Otherwise skip. Can be zero (use decimal degrees). Default = 0. | Nautical Almanac |
| *semidiameter_correction* | Correction for limb measurements.  | Typically used for Moon or Sun. *SD* value, positive (lower limb) or negative (upper limb). Default = 0. | Nautical Almanac | 
| *horizontal_parallax* | Correction for horizontal parallax.  | Used for the Moon. *HP* value. Default = 0. | Nautical Almanac | 
| measured_alt_degrees | Altitude of object in degrees. (0-90).         |                                                                | Sextant |
| *measured_alt_minutes* | Altitude of object in minutes (0-60).         | Can be zero (use decimal degrees). Default = 0.                              | Sextant |
| *measured_alt_seconds* | Altitude of object in seconds (0-60).         | Can be zero (use decimal degrees/minutes). Default = 0.                      | Sextant |
| *artficial_horizon*    | Indicates if you use an artifical horizon. True or False. | Default = False.          | N/A |
| *observer_height*    | Height of observer above sea level or ground in meters (>= 0). | Only relevant for observations using natural horizon. Default = 0.          | Height Measurement |
| *sextant*            | An object defining a specific used sextant.        | See [this code sample](starfixdata.xtra.home.py) for details. Default = None.       | Sextant Calibration |
| *chronometer*            | An object defining a specific used chronometer.        | See [this code sample](starfixdata.xtra.home.py) for details. Default = None.       | Chronometer Calibration |
| *temperature*            | Measured temperature at observing point. (degrees celsius)        |  Default = 10    | Observations or meteorology information |
| *dt_dh* | Temperature gradient (degrees celsius / meter) | default = -0.01 | Observations or meteorology information |
| *pressure* | Measured pressure at observing point. (kPa) | Default = 101 | Observations or meteorology information | 
| *ho_obs* | Set to True if dip and refraction corrections should be omitted | Default = False | N/A |

### 2.i. Atmospheric refraction<a name="atmospheric-refraction"></a>

The measured altitude values (attributes measured_alt_degrees,
measured_alt_minutes and measure_alt_seconds) are corrected for atmospheric
refraction using [Bennett's empirical formula](https://en.wikipedia.org/wiki/Atmospheric_refraction#Calculating_refraction)
with adjustments for temperature and pressure.

$R = \cot \left( h_a + \frac{7.31}{h_a + 4.4} \right)\frac{P}{101}\frac{283}{273+T}$

where 

* $R$ is the refraction in arc minutes.
* $h_a$ is the measured angle.
* $P$ is pressure in millibars.
* $T$ is temperature in Celsius. 

### 2.ii. Dip of horizon<a name="dip-of-horizon"></a>

If you specify the *observer_height* parameter you will correct for the dip of
the horizon. This is useful for observations from a ship deck at sea, or from a
hill/mountain with flat surroundings.
The dip is calculated using this formula

$a_{\text{diff}}= \arccos{ \frac{R}{R+h}}$

where

* $a_{\text{diff}}$ is the calculated dip (in radians)
* $R = \frac{r}{1-k}$ (corrected radius of Earth for geodetic refraction)
* $h$ is the height of the observer (in meters).
* $r$ is the radius of the Earth (in meters).
* $k = 503\frac{P}{T^2}\left(0.0342+\frac{dT}{dh}\right)$ (refraction coefficient)
* $P$ is the pressure (in millibars)
* $T$ is the temperature (in Kelvins)
* $\frac{dT}{dh}$ is the temperature gradient

If you use an artificial horizon the dip is always zero,
and the *observer_height* parameter should be zero.

For more information about the formula above please refer to
[this article](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2010JD014067).

### 2.iii. Ignored Corrections<a name="ignored-corrections"></a>

Currently the tool does not aim for very high accuracy and more elaborate
corrections are eliminated.

* Refraction correction is simple (see above), but probably good enough for basic celestial navigation. 
* Earth oblateness is ignored.

Future implementations may contain more precise corrections though.
See [more about future plans](CONTRIBUTING.md).

## 3. Sight reduction<a name="sight-reduction"></a>

### 3.i. Using two sights<a name="using-two-sights"></a>

Using two star fixes a sight reduction can be done in the following way:

    from starfix import Sight, SightCollection, get_representation
 
    a = Sight (....Parameters....)
    b = Sight (....Parameters....)
    
    collection = SightCollection ([a, b])
    try:
        intersections, fitness, diag_output = collection.get_intersections ()
        print (get_representation(intersections,1))
    except ValueError as ve:
        print ("Cannot get perform a sight reduction. Bad sight data.")
        

The result will be a tuple of **two** coordinates (intersections of two circles 
of equal altitude). These intersections can be located far away from each other.
You will have to decide which one of them is the correct observation point,
based on previous knowledge of your location.

The intersections are calculated using an algorithm based on
[this article](https://math.stackexchange.com/questions/4510171/how-to-find-the-intersection-of-two-circles-on-a-sphere) <br/>
This is a short outline of the algorithm.

![Intersection of small circles.](pics/globe-intersect.png "Intersection of small circles.")

For both measurements take note of the measured altitude
(from your **sextant**), $f_1$ and $f_2$.

Using your **chronometer** (clock) register the corresponding times $t_1$ and $t_2$
for the two measurements

Define angles $\alpha$ and $\beta$ this way:
$\alpha = \frac{\pi}{2} - f_1$, $\beta = \frac{\pi}{2} - f_2$

From the Nautical Almanac, using the timestamps $t_1$ and $t_2$,
get the geographic position vectors (GP:s) $a$ and $b$.

Now we can define two circles of equal altitude, $A$ and $B$.

$A = \lbrace p \in \mathbb{R}^3 \mid p \cdot a = \cos \alpha \land \left|p\right| = 1 \rbrace$ <br/>
$B = \lbrace p \in \mathbb{R}^3 \mid p \cdot b = \cos \beta \land \left|p\right| = 1 \rbrace$

The circles relate to a *sight pair* $S_{p_{1,2}} = \{s_1, s_2\}$
which we will come back to later.

(From now on we assume all coordinates/vectors are located on the unity sphere,
i.e. $\lbrace p \in \mathbb{R}^3 \mid \left|p\right| = 1 \rbrace$,
i.e. the Earth is a three-dimensional sphere and its surface has "radius = 1")

We aim for finding the intersections $p_1$ and $p_2$ for the circles $A$ and $B$
and the point $q$ being the midpoint between $p_1$ and $p_2$.

Using the [Pythagorean Theorem for a Sphere](https://en.wikipedia.org/wiki/Spherical_law_of_cosines)
it is easy to see this:

$\cos aq\cdot \cos pq = \cos \alpha$ <br/>
$\cos bq\cdot \cos pq = \cos \beta$ <br/>

From which we derive this

$q \cdot (a \cos \beta - b \cos \alpha) = 0$

Applying two cross-products and a normalization we can get the value for $q$

$q = N \left( (a \times b) \times (a \cos \beta - b \cos \alpha) \right)$

where $N$ is normalization

$N(x) = \frac{x}{\left|x\right|}$

Now we can find the intersection points by rotating $q$ for an angle of $\rho$ 
along a rotation axis $r$. <br/>
$\rho$ and $r$ are calculated this way:

$r = \left(a \times b\right) \times q$ <br/>
$\rho = \arccos(p \cdot q) = \arccos\left(\frac{\cos \alpha}{a \cdot q}\right) = \arccos\left(\frac{\cos \beta}{b \cdot q}\right)$

The final rotation is accomplished using [Rodrigues/Gauss rotation formula](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula).

$p_{\mathrm{rot}} = q \cos \rho + \left( r \times q \right) \sin \rho + r \left(r \cdot q \right)\left(1 - \cos \rho \right)$

Apply the formula above for $\rho$ and $-\rho$ and you will get the two 
intersection points $p_1$ and $p_2$.
**One of these points matches your location**.

When performing the calculation above we also deduce the intersection angle for
the two small circles (**fitness**). This angle will be used later on when we
compare many different intersections. When the angle is small the error margin
will be rather high and this can be used to reduce the effects of intersections
with big uncertainty. An angle close to 90 degrees however indicates a rather
precise measurement and this should be prioritized.

This is the algorithm for calculating the fitness:

$d_1 = N((p_1 - a) \times a)$ <br/>
$d_2 = N((p_1 - b) \times b)$

From this we calculate the fitness factor $\phi$:

$\phi = |d_1 \times d_2|$  ;  $0<=\phi<=1$


Note: The sight reduction algorithm described in this section will only work if at least one of the circles is a small circle.
It cannot be used for calculating intersections of two great circles.

Note: I have chosen to use an algorithm based on 3D cartesian vectors.
Standard literature on sight reduction typically uses 2D spherical coordinates,
such as [Longhand haversine sight reduction](https://en.wikipedia.org/wiki/Sight_reduction#Longhand_haversine_sight_reduction).
Such calculations in 2D are easier to carry out by hand but results in more
complex computer software. The 3D/cartesian approach is more structurally
simple and easier to convert to well-functioning software.

### 3.ii. Using three or more sights<a name="using-three-or-more-sights"></a>

Using three (or more) sights a sight reduction can be done in the following way

    from starfix import Sight, SightCollection, getRepresentation
 
    a = Sight (....Parameters....)
    b = Sight (....Parameters....)
    c = Sight (....Parameters....)
    
    collection = SightCollection ([a, b, c]) # Add more sights if needed
    try:
        intersections, fitness, diag_output = collection.getIntersections ()
        print (getRepresentation(intersections,1))
    except ValueError as ve:
        print ("Cannot get perform a sight reduction. Bad sight data.")

A *sight* is defined as a collection of data as described in the section 1 above,
i.e. recorded data for a celestial object for a specific time.

A collection contains of a set of sights (star fixes) $S$

$S_{\mathrm{sights}} = \lbrace s_1, s_2, \dots s_n  \rbrace $

Now set up a set of sight pairs

$S_p = \lbrace {S_p}_{i,j} | i<=n \land j<=n \land j>i+1 \rbrace$

It is easy to see that the number of sight pairs (the cardinality) can be 
calculated like this

$\left|S_p\right| = \frac{n^2 + n}{2} $

For each sight pair we now collect the two corresponding intersection points
($L$ = left, $R$ = right) using the algorithm described in 2.1 above.

$S_{p,i,j} \to \lbrace I_{p,i,j,L},I_{p,i,j,R} \rbrace$

This will result in a set of intersection points

$I_p = \lbrace I_{p,i,j,O} | O \in \{L,R \} \land i<=n \land j<=n \land j>i+1 \rbrace$

The cardinality can easily be shown as

$\left|I_p\right| = n^2 + n $

For each pair of intersection points we calculate the distance.
The distance is easily calculated using this formula.

$d\left(x,y\right) = \arccos (x \cdot y) $

This will give us the following set

$D = \lbrace d\left(I_k,I_l\right) | k < \left|I\right| \land l < \left|I\right| \land k <> l \rbrace$

The cardinality of $D$ can be calculated

$\left|D\right| = {\left|I\right|}^2 - {\left|I\right|} = n^4 + 2n^3 - n$

We now need to eliminate all false intersections and only choose those close 
to the probable location of the observer.

The final part of the algorithm sorts the set $D$ to extract a maximum of $\frac{n^2-n}{2}$
intersection points, and also applying a maximal allowed distance limit
(which defaults to 100 km). The **fitness** value (see above) is used for
giving priority (weighting) for intersections with a larger angle.

The final result will be a **single** mean value of the extracted intersection points.

### 3.iii. Running the starfixdata.chicago script<a name="run-chicago-script"></a>

This picture shows the small circles defined in the
[starfixdata.stat.1.py](starfixdata.stat.1.py) sample
![Locating from Chicago](pics/chicago-intersection-1.png "Locating from Chicago")

When we move in closer we can clearly see a precise intersection.
![Locating from Chicago (detail)](pics/chicago-intersection-2.png "Locating from Chicago (detail)")

*Note: The mapping software used in the images above is not precise, and the
actual intersections are even "tighter" than shown above.*

The output of the script will be like this:
First we show the two intersection points from two small circles. The second one
is within Chicago.

    ((N 7°,40.8′;W 94°,14.0′);(N 41°,51.2′;W 87°,38.6′))

Then we add another small circle and show the calculated mean value of the intersections

    (N 41°,51.3′;W 87°,38.6′)

There is also another similar test script in the [starfixdata.stat.2.py](starfixdata.stat.2.py)
sample where the Moon is used. **Horizontal parallax** is applied to the Moon
using the *HP* field from the Nautical Almanac.
The Moon is typically the only celestial object where horizontal parallax
needs to be considered. For other planets and the Sun the correction will almost
always be obscured by sextant reading errors.

You may also use the supplied Jupyter Notebook scripts
[notebook.stat.1.ipynb](notebook.stat.1.ipynb) and [notebook.stat.2.ipynb](notebook.stat.2.ipynb).

## 4. Dead Reckoning<a name="dead-reckoning"></a>

When sailing (or moving on the ground) you can use this technique to support
dead reckoning where repeated sights (typically of the Sun) will give extra
accuracy. You do this by defining a trip segment like this.

    from starfix import SightTrip, Sight, LatLon
    
    # We are sailing from point s1 to point s2, in the Baltic Sea.  
    # We have a rough estimate of an initial position of 59N;18E to start with
    # This estimate is used for selecting the correct intersection point on Earth.
    s1LatLon = LatLon (59, 18)

    # We define two star fixes  
    s1 = Sight (......) # This is your sight at the start of this trip segment. 
    s2 = Sight (......) # This is your sight at the end of this trip segment.

See above for how to create a sight object

    # We reach s2 by applying about 175 degrees for 1 hour
    # (time between taking of sights) with a speed of 20 knots. 
    C_COURSE = 175
    SPEED = 20    
    st = SightTrip (sight_start = s1, sight_end = s2,\
                    estimated_starting_point        = s1LatLon,\
                    course_degrees                  = C_COURSE,\
                    speed_knots                     = SPEED)

Now you can calculate the coordinates for this trip.

    intersections, fitness, diag_output = st.get_intersections ()
    print ("Starting point = " + str(get_representation(intersections[0],1)))
    print ("End point = " + str(get_representation(intersections[1],1)))

The algorithm is a calculation based on distance calculations on segments of the
small circles related to $s_1$ and $s_2$.

The two small circles define a *sight pair* $S_p$ but the two sights are taken
at different times. There are two intersection points $\lbrace p_1,p_2 \rbrace$.
We select the intersection $p_i$ point which is closest to the estimated
starting point $p_e$ by finding the minimum value of $\arccos (p_n \cdot p_e)$

We now define a function on a rotation angle $\rho$ which we will apply on the circle $s_1$

$K(\rho) = \arccos ( (r(s_1,\rho) + t(\phi,\tau))\cdot p_{\text{GPs2}} ) - (\frac{\pi}{2} - \alpha_{s2})$

where<br>

* $r$ is a rotation function (based on Rodrigues formula, see above)
* $t$ is a straight movement function based on approximate course $\phi$
  with distance $\tau$.
* $p_{\text{GPs2}}$ is the vector of the *geographic position* of sight $s_2$
* $\alpha_{s2}$ is the altitude measured for $s_2$ (see above for calculation)

The solution of the equation $K(\rho) = 0$ is computed using [Newton's method](https://en.wikipedia.org/wiki/Newton%27s_method).

The supplied script sample [starfixdata.sea.py](starfixdata.sea.py) contains
a demo for a short trip at sea (in the Baltic Sea).

This is a picture of the small circles generated by the sample.
The larger circle corresponds to the first observation with a lower Sun altitude.
The smaller circle is the final observation with a higher Sun altitude.

![Sailing in the Baltic Sea](pics/baltic-intersection-1.png "Sailing in the Baltic Sea")

When we move in closer we can clearly see the intersection $p_i$.

![Sailing in the Baltic Sea (closeup)](pics/baltic-intersection-2.png "Sailing in the Baltic Sea (closeup)")

And the course (with our positions) can easily be found using a paralellogram
adjustment where we "squeeze in" a route of 20 NM, course 175 degrees, starting
at the first small circle and ending at the final circle. The classical method
of doing this is of course using a chart and proper plotting equipment and
assume linearity of the circle segments.

![Sailing in the Baltic Sea (closeup)](pics/baltic-intersection-2-edit.png "Sailing in the Baltic Sea (closeup)")

### 4.i. Running the starfixdata.sea script<a name="run-sea-script"></a>

The script outputs the estimated starting and ending points for our trip segment
(see the red arrow in the map above)

    Starting point = (N 58°,46.1′;E 18°,0.1′)
    End point = (N 58°,26.2′;E 18°,3.5′)

In addition we get some diagnostic information.
First the radius and GP coordinate of the small circle of the first observation.

    S1 radius = 6581.3
    S1 GP     = 23.4367,86.7554

And for the final observation.

    S2 radius = 5722.4
    S2 GP     = 23.4367,71.7571

If you want to plot the trip segment in Google Maps (GM)
you have the coordinates here.

    Starting point GM = 58.7684,18.0023
    Ending   point GM = 58.4364,18.0583

You may also use the supplied Jupyter Notebook script
[notebook.sea.ipynb](notebook.sea.ipynb).

## 5. A real-life example<a name="real-life"></a>

You can also see a real-life measurement I recently made using a simple plastic
sextant (Davis Mark III), a standard watch and an artifical horizon.

![Simple celestial navigation gear](pics/celnav-gear.jpg "Simple celestial navigation gear")

The sample can be found [here](starfixdata.xtra.home.py)
The resulting position is just 1.45 nautical miles away from my real position,
which I consider being an excellent result given the simple equipment and my
modest level of training.
But there are some question marks about this accuracy, and I will have to make
more sights since I need to get more training.

## 6. Terrestrial Navigation <a name="terrestrial"></a>

A sextant can be used for terrestrial navigation too,
if you orient it horizontally. Typically you take sights of lighthouses when
performing a landfall towards a coast.
[This sample](terrestrial.py) shows an example of this.
The underlying maths are quite similar to sight reduction of star fixes.
You need to find the intersection of two
circles representing equal angle to two terrestrial points.

The following picture shows how the sample results in two circles of equal angle.
The three small circles are centered on three lighthouses and you have measured
the observed angle between them from your observation point with a sextant.
The red arrow points towards the calculated correct position (intersection).

![Navigation towards three lighthouses](pics/lighthouses.png "Terrestrial Navigation")

You may also use the supplied Jupyter Notebook script
[notebook.terrestrial.ipynb](notebook.terrestrial.ipynb).

## 7. Sextant Calibration <a name="calibration"></a>

There are many technical aspects of handling and calibrating a sextant and we
will not mention all these things here, with one exception.
A sextant may show a **gradation error** which can cause errors for larger
measured angles. The little plastic sextant I have used (a Davis Mark III) was
suspected by me,
and I decided to measure it by taking a terrestrial angle fix and compare it to
the data from my map. And yes, there was an error of about 2 minutes / 10 degrees.
For the details see [this sample](starfixdata.xtra.home.py) where a measurement of a
local view is used as input to a calibration parameter of the used sextant.  

## 8. Chronometer Handling <a name="chronometer"></a>

Your chronometer may have a **drift** to take care of, typically if it is mechanical
or digital with no auto-setting. 
The toolkit contains a Chronometer class which can be used to handle this and
you will find an example of handling this in [this sample](starfixdata.xtra.home.py)