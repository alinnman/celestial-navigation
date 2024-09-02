''' This is a sample for celestial navigation for a stationary observer 
    Sample taken from FB discussion with Nigel Coey. 
    Data is approximate star fixes from Macquarie Island
'''

from time import time
from starfix import Sight, SightCollection, get_representation, get_google_map_string


starttime = time ()

# Our starfix data
hour = 11
minute = 10

a = Sight (   object_name          = "Acrux", \
              time_year            = 2024,\
              time_month           = 8,\
              time_day             = 31,\

              time_hour            = hour, \
              time_minute          = minute, \
              time_second          = 0, \
              gha_time_0_degrees   = 145, \
              gha_time_0_minutes   = 7, \
              gha_time_1_degrees   = 160, \
              gha_time_1_minutes   = 9.4, \
              decl_time_0_degrees  = -63, \
              decl_time_0_minutes  = 14.2, \
              measured_alt_degrees = 40, \
              measured_alt_minutes = 0, \
              measured_alt_seconds = 0, \
              sha_diff_degrees     = 173, \
              sha_diff_minutes     = 1.1 \
              )

b = Sight (   object_name          = "Canopus", \
              time_year            = 2024,\
              time_month           = 8,\
              time_day             = 31,\
              time_hour            = hour, \
              time_minute          = minute, \
              time_second          = 0, \
              gha_time_0_degrees   = 145, \
              gha_time_0_minutes   = 7, \
              gha_time_1_degrees   = 160, \
              gha_time_1_minutes   = 9.4, \
              decl_time_0_degrees  = -52, \
              decl_time_0_minutes  = 42.1, \
              measured_alt_degrees = 20, \
              measured_alt_minutes = 0, \
              measured_alt_seconds = 0, \
              sha_diff_degrees     = 263, \
              sha_diff_minutes     = 52.8 \
              )

c = Sight (   object_name          = "Achernar", \
              time_year            = 2024,\
              time_month           = 8,\
              time_day             = 31,\
              time_hour            = hour, \
              time_minute          = minute, \
              time_second          = 0, \
              gha_time_0_degrees   = 145, \
              gha_time_0_minutes   = 7, \
              gha_time_1_degrees   = 160, \
              gha_time_1_minutes   = 9.4, \
              decl_time_0_degrees  = -57, \
              decl_time_0_minutes  = 6.4, \
              measured_alt_degrees = 50, \
              measured_alt_minutes = 0, \
              measured_alt_seconds = 0, \
              sha_diff_degrees     = 335, \
              sha_diff_minutes     = 20 \
              )


collection = SightCollection ([a, b, c])
intersections = collection.get_intersections (limit=500)
print ("Location = " + get_representation(intersections,1))
print ("Google Map coordinate = " + get_google_map_string (intersections,2))

#Diagnostics for map rendering etc.
print ("")
print ("Some useful data follows (Small circles of equal altitude). For plotting in map software etc.")
print ("A celestial body = " + a.object_name)
print ("A radius = " + str(round(a.get_radius (),1)))
print ("A GP     = " + get_google_map_string(a.gp,4))
print ("")
print ("B celestial body = " + b.object_name)
print ("B radius = " + str(round(b.get_radius (),1)))
print ("B GP     = " + get_google_map_string(b.gp,4))
print ("")
print ("C celestial body = " + c.object_name)
print ("C radius = " + str(round(c.get_radius (),1)))
print ("C GP     = " + get_google_map_string(c.gp,4))

endtime = time ()

takenMs = round((endtime-starttime)*1000,2)

print ("Time taken = " +str(takenMs)+" ms")
