''' This is a real-world sample. Very basic sextant used '''

from starfix import Sight, SightCollection, LatLon, Sextant,\
                    get_decimal_degrees_from_tuple,\
                    get_representation, \
                    get_google_map_string, distance_between_points
from calibration import calibrationRealValue, calibrationMeasuredValue


# This is observations from actual sextant readings.
# I used a simple plastic sextant (Davis Mk III) and an artificial horizon.

# Defining the Sextant object, using the calculated gradation error as parameter.
mySextant = Sextant (get_decimal_degrees_from_tuple (calibrationMeasuredValue) / \
                     get_decimal_degrees_from_tuple (calibrationRealValue))

S1 = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 14,\
              time_hour            = 5, \
              time_minute          = 57, \
              time_second          = 50, \
              gha_time_0_degrees   = 254, \
              gha_time_0_minutes   = 54.8, \
              gha_time_1_degrees   = 269, \
              gha_time_1_minutes   = 54.7, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 17.1, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 17.3, \
              measured_alt_degrees = 57, \
              measured_alt_minutes = 8, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True,\
              index_error_minutes  = 0,\
              semi_diameter_correction = 15.7,\
              sextant = mySextant
              )

S2 = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 15,\
              time_hour            = 14, \
              time_minute          = 49, \
              time_second          = 7, \
              gha_time_0_degrees   = 29, \
              gha_time_0_minutes   = 50.4, \
              gha_time_1_degrees   = 44, \
              gha_time_1_minutes   = 50.2, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 20.5, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 20.6, \
              measured_alt_degrees = 70, \
              measured_alt_minutes = 17, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True,\
              index_error_minutes  = 0,\
              sextant = mySextant
              )

collection = SightCollection ([S1, S2])

# This is the exact position of my observation location
home = LatLon (59.318659676810654, 18.04959717835501)

intersections = collection.get_intersections (estimated_position = LatLon(59,19))
print (get_representation(intersections,1))
print ("MD = " + collection.get_map_developers_string())
print ("GM = " + get_google_map_string(intersections,4))
print ("Intersection distance from home = " + str(distance_between_points(intersections, home)))

#Diagnostics for map rendering etc.
print ("Some useful data follows")

print ("S1 radius = " + str(round(S1.get_radius (),1)))
print ("S1 GP     = " + get_google_map_string(S1.gp,4))
print ("Diff     = " + str(S1.get_distance_from (home)))
print ("--")

print ("S2 radius = " + str(round(S2.get_radius (),1)))
print ("S2 GP     = " + get_google_map_string(S2.gp,4))
print ("Diff     = " + str(S2.get_distance_from (home)))
print ("--")
print ("-----------------------------------")
 