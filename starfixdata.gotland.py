''' This is a sample for celestial navigation for a stationary observer 
    (C) August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

'''

from time import time
from starfix import Sight, SightCollection, get_representation, get_google_map_string


starttime = time ()

# Our starfix data

a = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 29,\
              time_hour            = 8, \
              time_minute          = 21, \
              time_second          = 0, \
              gha_time_0_degrees   = 299, \
              gha_time_0_minutes   = 6.6, \
              gha_time_1_degrees   = 314, \
              gha_time_1_minutes   = 6.5, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 11.6, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 11.4, \
              measured_alt_degrees = 46, \
              measured_alt_minutes = 23, \
              )

b = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 29,\
              time_hour            = 12, \
              time_minute          = 51, \
              time_second          = 0, \
              gha_time_0_degrees   = 359, \
              gha_time_0_minutes   = 6.1, \
              gha_time_1_degrees   = 14, \
              gha_time_1_minutes   = 6.6, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 11.1, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 10.8, \
              measured_alt_degrees = 49, \
              measured_alt_minutes = 18, \
              )

c = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 29,\
              time_hour            = 15, \
              time_minute          = 36, \
              time_second          = 0, \
              gha_time_0_degrees   = 44, \
              gha_time_0_minutes   = 5.7, \
              gha_time_1_degrees   = 59, \
              gha_time_1_minutes   = 5.6, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 10.5, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 10.4, \
              measured_alt_degrees = 29, \
              measured_alt_minutes = 20, \
              )


collection = SightCollection ([a, b, c])
intersections, fitness = collection.get_intersections ()
print (get_representation(intersections,1))
print ("MD = " + collection.get_map_developers_string())
print ("GM = " + get_google_map_string(intersections,4))

#Diagnostics for map rendering etc.
print ("Some useful data follows")
print ("A radius = " + str(round(a.get_radius (),1)))
print ("A GP     = " + get_google_map_string(a.gp,4))

print ("B radius = " + str(round(b.get_radius (),1)))
print ("B GP     = " + get_google_map_string(b.gp,4))

print ("C radius = " + str(round(c.get_radius (),1)))
print ("C GP     = " + get_google_map_string(c.gp,4))

endtime = time ()

takenMs = round((endtime-starttime)*1000,2)

print ("Time taken = " +str(takenMs)+" ms")
