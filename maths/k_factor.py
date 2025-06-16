''' A toolkit for celestial navigation, in particular sight reductions 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    This is a little script calculating the k factor and the radius of the Earth
    for a series of dip observations.
'''

from math import sqrt
from decimal import Decimal

# Data retreived from https://youtu.be/6viR_GJ8998?si=DYb5AwY-2OZzyKKc
vals = [[5, 0.0712],
[20, 0.1442],
[36, 0.1817],
[43, 0.2306],
[59, 0.2372],
[72, 0.2712],
[97, 0.2995],
[127, 0.3406],
[184, 0.4018]]

def calculate ():
    ''' Perform the simple mean value calculation and print the result '''
    accum_k = 0
    for v in vals:
        the_item = (v[1]/sqrt(v[0]))*60
        accum_k += the_item
    mean_k = accum_k / len(vals)
    print ("The k coefficient is " + str(round(mean_k,2)))

    earth_radius = (2.364 * 10**7) / mean_k**2
    print ("The calculated radius of the Earth is " + f"{Decimal(str(earth_radius)):.3E}" + " m.")

calculate ()
