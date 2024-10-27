''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

'''

from time import time
from starfix import Sight, SightCollection, get_representation, get_google_map_string

starttime = time ()

# Our starfix data

a = Sight (   object_name          = "Sun", \
              set_time             = "2024-05-05 15:55:18+00:00", \
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
              measured_alt_seconds = 1.8 \
              )

b = Sight (   object_name          = "Sun", \
              set_time             = "2024-05-05 23:01:19+00:00", \
              gha_time_0_degrees   = 165, \
              gha_time_0_minutes   = 50.8, \
              gha_time_1_degrees   = 180, \
              gha_time_1_minutes   = 50.8, \
              decl_time_0_degrees  = 16, \
              decl_time_0_minutes  = 36.2, \
              decl_time_1_degrees  = 16, \
              decl_time_1_minutes  = 36.9, \
              measured_alt_degrees = 19, \
              measured_alt_minutes = 28, \
              measured_alt_seconds = 18 \
              )

c = Sight (   object_name          = "Vega", \
              set_time             = "2024-05-06 04:04:13+00:00", \
              gha_time_0_degrees   = 284, \
              gha_time_0_minutes   = 30.4, \
              gha_time_1_degrees   = 299, \
              gha_time_1_minutes   = 32.9, \
              decl_time_0_degrees  = 38, \
              decl_time_0_minutes  = 48.1, \
              measured_alt_degrees = 30, \
              measured_alt_minutes = 16, \
              measured_alt_seconds = 24.6, \
              sha_diff_degrees     = 80, \
              sha_diff_minutes     = 33.4 \
              )

print ("Two daytime observations of the sun")
collection = SightCollection ([a, b])
try:
    intersections, fitness, diag_output = collection.get_intersections ()
except ValueError as ve:
    print ("Cannot get perform a sight reduction. Bad sight data.")
    exit ()
print (get_representation(intersections,1))
print ("-----------------------------------")
print ("We add an additional night time observation of Vega")
collection = SightCollection ([a, b, c])
intersections, fitness, diag_output = collection.get_intersections ()
endtime = time ()
takenMs = round((endtime-starttime)*1000,3)
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
