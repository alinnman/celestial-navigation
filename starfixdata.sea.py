''' Simple sample representing a trip at sea where celestial navigation is supporting
    celestial navigation
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)    
    
'''

from time import time
from starfix import Sight, SightTrip, get_representation, get_google_map_string, LatLon

starttime = time ()

# We are sailing from point s1 to point s2, in the Baltic Sea.
# We are sailing from point s1 to point s2, in the Baltic Sea.
# We have a rough estimate of an initial position of 59N;18E to start with
# This estimate is used for selecting the correct intersection point on Earth.
s1LatLon = LatLon (59, 18)

#This is the star fix for s1, the starting point

s1 = Sight (  object_name          = "Sun", \
              time_year            = 2024, \
              time_month           = 6, \
              time_day             = 20, \
              time_hour            = 6, \
              time_minute          = 14, \
              time_second          = 38, \
              gha_time_0_degrees   = 269, \
              gha_time_0_minutes   = 35.2, \
              gha_time_1_degrees   = 284 , \
              gha_time_1_minutes   = 35.1, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 26.2, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 26.2, \
              measured_alt_degrees = 30, \
              measured_alt_minutes = 51, \
              measured_alt_seconds = 27.1 \
              )


# Point s2 is located roughly 20 nautical miles out in the sea.

# We take a sight here and get this.

s2 = Sight (  object_name          = "Sun", \
              time_year            = 2024, \
              time_month           = 6, \
              time_day             = 20, \
              time_hour            = 7, \
              time_minute          = 14, \
              time_second          = 38, \
              gha_time_0_degrees   = 284, \
              gha_time_0_minutes   = 35.1, \
              gha_time_1_degrees   = 299 , \
              gha_time_1_minutes   = 35.0, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 26.2, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 26.2, \
              measured_alt_degrees = 38, \
              measured_alt_minutes = 34, \
              measured_alt_seconds = 21.6 \
              )

# We reach s2 by applying about 175 degrees for 1 hour with a speed of 20 knots.
C_COURSE = 175
SPEED = 20
st = SightTrip (sight_start               = s1,\
                 sight_end                = s2,\
                 estimated_starting_point = s1LatLon,\
                 course_degrees           = C_COURSE,\
                 speed_knots              = SPEED)
intersections, fitness = st.get_intersections ()
print ("MD = " + st.get_map_developers_string ())
print ("Starting point = " + str(get_representation(intersections[1],1)))
print ("End point = " + str(get_representation(intersections[0],1)))


# Diagnostics for map rendering etc.

print ("S1 radius = " + str(round(s1.get_radius (),1)))
print ("S1 GP     = " + get_google_map_string(s1.gp,4))

print ("S2 radius = " + str(round(s2.get_radius (),1)))
print ("S2 GP     = " + get_google_map_string(s2.gp,4))

print ("Starting point GM = " + get_google_map_string (intersections[1],4))
print ("Ending   point GM = " + get_google_map_string (intersections[0],4))

endtime = time ()

takenMs = round((endtime-starttime)*1000,2)

print ("Time taken = " +str(takenMs)+" ms")
