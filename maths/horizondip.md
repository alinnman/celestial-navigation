<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Some notes on horizon dip (Al-Biruni)

See [this document](sphere-proof.2.md) where we construct reasoning and proof used here. 

From this we can easily get the radius of the Earth ($R$) given the
coefficient ($k$) just like [Al-Biruni did in 1017 AD](https://en.wikipedia.org/wiki/Al-Biruni#Geography_and_geodesy)

Note that Al-Biruni's calculation was made without knowledge of refraction
and also with measurements with partially unkown units of measurement
(in today's units). He also used a rather primitive level device.
He didn't get a very exact result for the radius $R$.
His primary finding was the **method** he used,
and the discovery of the dip of the horizon, allowing for anyone after
him to repeat the experiment.

Insert different values and we get:

$R \approx \frac {2.364 \times 10^7}{1.75^2} = 7.72 \times 10^6$
(which is larger than the real value)

$R \approx \frac {2.364 \times 10^7}{1.93^2} = 6.35 \times 10^6$
(close to the real value)

In the picture below we see a series of actual dip measurements.
For details see [this video](https://youtu.be/6viR_GJ8998?si=JCDL66ikg9gqIYtu). You can clearly see the square root relation here.

![Theodolite measurments](../pics/theodilite-measurements.png)

If you run [this script](k_factor.py) you will see that the actual $k$ factor
for this test was **$1.88$** which indicates less refraction than the "default"
value of $1.75$. Nevertheless; refraction is difficult and will always create
uncertainties in measurements like this. The overall effect of the horizon dip
and its dependence of increasing elevation is however **very obvious**.

If the theodolite measurements in the YouTube video were used as direct
data for Earth radius calculation we would get:

$R \approx \frac {2.364 \times 10^7}{1.88^2} = 6.659 \times 10^6$<br>
which is only about 4 percent larger than the real value.
