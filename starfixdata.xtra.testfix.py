''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

    Test sample from sextant exercise. This used a Ho observation so I added
    support for this in the code (eliminating refraction and dip calculations)
'''

from time import time
from starfix import Sight, SightCollection, get_representation, get_google_map_string


starttime = time ()

# Our starfix data

YEAR = 2024
MONTH = 10
DAY = 1
HOUR = 17
MINUTE = 13
SECOND = 0

TEMPERATURE = 18

a = Sight (   object_name          = "Sabik", \
              time_year            = YEAR,\
              time_month           = MONTH,\
              time_day             = DAY,\
              time_hour            = HOUR, \
              time_minute          = MINUTE, \
              time_second          = SECOND, \
              gha_time_0_degrees   = 265, \
              gha_time_0_minutes   = 55.1, \
              gha_time_1_degrees   = 280, \
              gha_time_1_minutes   = 57.5, \
              decl_time_0_degrees  = -15, \
              decl_time_0_minutes  = 45.3, \
              sha_diff_degrees     = 102, \
              sha_diff_minutes     = 3.2, \
              measured_alt_degrees = 57, \
              #measured_alt_minutes = 40.2, \
              measured_alt_minutes = 36.8, \
              observer_height      = 2.5, \
              temperature          = TEMPERATURE, \
              ho_obs               = True \
              )

b = Sight (   object_name          = "Venus", \
              time_year            = YEAR,\
              time_month           = MONTH,\
              time_day             = DAY,\
              time_hour            = HOUR, \
              time_minute          = MINUTE, \
              time_second          = SECOND, \
              gha_time_0_degrees   = 47, \
              gha_time_0_minutes   = 57.8, \
              gha_time_1_degrees   = 62, \
              gha_time_1_minutes   = 57.3, \
              decl_time_0_degrees  = -15, \
              decl_time_0_minutes  = 14.8, \
              decl_time_1_degrees  = -15, \
              decl_time_1_minutes  = 15.9, \
              measured_alt_degrees = 25, \
              #measured_alt_minutes = 13.1, \
              measured_alt_minutes = 8.4, \
              observer_height      = 2.5, \
              temperature          = TEMPERATURE, \
              ho_obs               = True \
              )

c = Sight (   object_name          = "Saturn", \
              time_year            = YEAR,\
              time_month           = MONTH,\
              time_day             = DAY,\
              time_hour            = HOUR, \
              time_minute          = MINUTE, \
              time_second          = SECOND, \
              gha_time_0_degrees   = 279, \
              gha_time_0_minutes   = 30.9, \
              gha_time_1_degrees   = 294, \
              gha_time_1_minutes   = 33.5, \
              decl_time_0_degrees  = -8, \
              decl_time_0_minutes  = 11.8, \
              decl_time_1_degrees  = -8, \
              decl_time_1_minutes  = 11.8, \
              measured_alt_degrees = 30, \
              #measured_alt_minutes = 24.7, \
              measured_alt_minutes = 20.2, \
              observer_height      = 2.5, \
              temperature          = TEMPERATURE, \
              ho_obs               = True \
              )


collection = SightCollection ([a, b])
intersections, fitness = collection.get_intersections (limit = 100)
print ("GM = " + get_google_map_string(intersections,4))
collection = SightCollection ([a, c])
intersections, fitness = collection.get_intersections (limit = 100)
print ("GM = " + get_google_map_string(intersections,4))
collection = SightCollection ([b, c])
intersections, fitness = collection.get_intersections (limit = 100)
print ("GM = " + get_google_map_string(intersections,4))

collection = SightCollection ([a, b, c])
intersections, fitness = collection.get_intersections (limit = 100)
endtime = time ()
takenMs = round((endtime-starttime)*1000,2)
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

print ("Time taken = " +str(takenMs)+" ms")
