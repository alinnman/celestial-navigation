''' This is a sample for celestial navigation for a stationary observer 
    (C) August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

'''

from time import time
from starfix import Sight, SightCollection, get_representation, get_google_map_string


starttime = time ()

# Our starfix data

year = 2024
month = 9
day = 17
hour = 23
minute = 36
second = 13

a = Sight (   object_name          = "Capella", \
              time_year            = year,\
              time_month           = month,\
              time_day             = day,\
              time_hour            = hour, \
              time_minute          = minute, \
              time_second          = second, \
              gha_time_0_degrees   = 342, \
              gha_time_0_minutes   = 21.9, \
              gha_time_1_degrees   = 357, \
              gha_time_1_minutes   = 24.4, \
              decl_time_0_degrees  = 46, \
              decl_time_0_minutes  = 1.2, \
              sha_diff_degrees     = 280, \
              sha_diff_minutes     = 22.3, \
              measured_alt_degrees = 33, \
              measured_alt_minutes = 9, \
              measured_alt_seconds = 34 \
              )

b = Sight (   object_name          = "Moon", \
              time_year            = year,\
              time_month           = month,\
              time_day             = day,\
              time_hour            = hour, \
              time_minute          = minute+5, \
              time_second          = second, \
              gha_time_0_degrees   = 347, \
              gha_time_0_minutes   = 55.7, \
              gha_time_1_degrees   = 2, \
              gha_time_1_minutes   = 24.6, \
              decl_time_0_degrees  = -3, \
              decl_time_0_minutes  = 43.5, \
              decl_time_1_degrees  = -3, \
              decl_time_1_minutes  = 25.3, \
              horizontal_parallax  = 61.2, \
              measured_alt_degrees = 48, \
              measured_alt_minutes = 22, \
              measured_alt_seconds = 5.2 \
              )

c = Sight (   object_name          = "Vega", \
              time_year            = year,\
              time_month           = month,\
              time_day             = day,\
              time_hour            = hour, \
              time_minute          = minute+10, \
              time_second          = second, \
              gha_time_0_degrees   = 342, \
              gha_time_0_minutes   = 21.9, \
              gha_time_1_degrees   = 357, \
              gha_time_1_minutes   = 24.4, \
              decl_time_0_degrees  = 38, \
              decl_time_0_minutes  = 48.6, \
              sha_diff_degrees     = 80, \
              sha_diff_minutes     = 33.3, \
              measured_alt_degrees = 25, \
              measured_alt_minutes = 39, \
              measured_alt_seconds = 4, \
              )

collection = SightCollection ([a,b,c])
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
