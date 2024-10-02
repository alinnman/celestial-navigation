''' This is a sample for celestial navigation for a stationary observer 
    (C) August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

'''

from time import time
from starfix import Sight, SightCollection, get_representation, get_google_map_string


starttime = time ()

# Our starfix data

year = 2024
month = 10
day = 1
hour = 17
minute = 13
second = 0

a = Sight (   object_name          = "Sabik", \
              time_year            = year,\
              time_month           = month,\
              time_day             = day,\
              time_hour            = hour, \
              time_minute          = minute, \
              time_second          = second, \
              gha_time_0_degrees   = 265, \
              gha_time_0_minutes   = 55.1, \
              gha_time_1_degrees   = 280, \
              gha_time_1_minutes   = 57.5, \
              decl_time_0_degrees  = -15, \
              decl_time_0_minutes  = 45.3, \
              sha_diff_degrees     = 102, \
              sha_diff_minutes     = 3.2, \
              measured_alt_degrees = 57, \
              measured_alt_minutes = 40.2, \
              )

b = Sight (   object_name          = "Venus", \
              time_year            = year,\
              time_month           = month,\
              time_day             = day,\
              time_hour            = hour, \
              time_minute          = minute, \
              time_second          = second, \
              gha_time_0_degrees   = 47, \
              gha_time_0_minutes   = 57.8, \
              gha_time_1_degrees   = 62, \
              gha_time_1_minutes   = 57.3, \
              decl_time_0_degrees  = -15, \
              decl_time_0_minutes  = 14.8, \
              decl_time_1_degrees  = -15, \
              decl_time_1_minutes  = 15.9, \
              measured_alt_degrees = 25, \
              measured_alt_minutes = 13.1, \
              )

c = Sight (   object_name          = "Saturn", \
              time_year            = year,\
              time_month           = month,\
              time_day             = day,\
              time_hour            = hour, \
              time_minute          = minute, \
              time_second          = second, \
              gha_time_0_degrees   = 279, \
              gha_time_0_minutes   = 30.9, \
              gha_time_1_degrees   = 294, \
              gha_time_1_minutes   = 33.5, \
              decl_time_0_degrees  = -8, \
              decl_time_0_minutes  = 11.8, \
              decl_time_1_degrees  = -8, \
              decl_time_1_minutes  = 11.9, \
              measured_alt_degrees = 30, \
              measured_alt_minutes = 24.7, \
              )

collection = SightCollection ([a, b, c])
intersections = collection.get_intersections ()
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
