''' This is a sample for celestial navigation for a stationary observer 
    Sample taken from FB discussion with Nigel Coey. 
    Data is approximate star fixes from Macquarie Island
    (C) August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)
    
Output: 
MEAN VALUE COORDINATE from multi-point sight data.
Location = (S 56°,50.2′;E 154°,27.0′)
Google Map coordinate = -56.84,154.45
https://www.mapdevelopers.com/draw-circle-tool.php?circles=%5B%5B5563507%2C-63.2367%2C39.3583%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B7790847%2C-52.7017%2C-51.5033%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B4450597%2C-57.1067%2C-122.9567%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%5D

Some useful data follows (Small circles of equal altitude). For plotting in map software etc.
A celestial body = Acrux
A radius = 5563.5
A GP     = -63.2367,39.3583

B celestial body = Canopus
B radius = 7790.8
B GP     = -52.7017,-51.5033

C celestial body = Achernar
C radius = 4450.6
C GP     = -57.1067,-122.9567

Map output: 
https://www.mapdevelopers.com/draw-circle-tool.php?circles=%5B%5B5563500%2C-62.7633%2C39.3583%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B7790800%2C-51.2983%2C-51.5033%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B4450600%2C-56.8933%2C-122.9567%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%5D 
'''

from time import time
from starfix import Sight, SightCollection, get_representation, get_google_map_string


starttime = time ()

# Our starfix data
HOUR = 11
MINUTE = 10

a = Sight (   object_name          = "Acrux", \
              time_year            = 2024,\
              time_month           = 8,\
              time_day             = 31,\

              time_hour            = HOUR, \
              time_minute          = MINUTE, \
              gha_time_0_degrees   = 145, \
              gha_time_0_minutes   = 7, \
              gha_time_1_degrees   = 160, \
              gha_time_1_minutes   = 9.4, \
              decl_time_0_degrees  = -63, \
              decl_time_0_minutes  = 14.2, \
              measured_alt_degrees = 40, \
              sha_diff_degrees     = 173, \
              sha_diff_minutes     = 1.1 \
              )

b = Sight (   object_name          = "Canopus", \
              time_year            = 2024,\
              time_month           = 8,\
              time_day             = 31,\
              time_hour            = HOUR, \
              time_minute          = MINUTE, \
              gha_time_0_degrees   = 145, \
              gha_time_0_minutes   = 7, \
              gha_time_1_degrees   = 160, \
              gha_time_1_minutes   = 9.4, \
              decl_time_0_degrees  = -52, \
              decl_time_0_minutes  = 42.1, \
              measured_alt_degrees = 20, \
              sha_diff_degrees     = 263, \
              sha_diff_minutes     = 52.8 \
              )

c = Sight (   object_name          = "Achernar", \
              time_year            = 2024,\
              time_month           = 8,\
              time_day             = 31,\
              time_hour            = HOUR, \
              time_minute          = MINUTE, \
              gha_time_0_degrees   = 145, \
              gha_time_0_minutes   = 7, \
              gha_time_1_degrees   = 160, \
              gha_time_1_minutes   = 9.4, \
              decl_time_0_degrees  = -57, \
              decl_time_0_minutes  = 6.4, \
              measured_alt_degrees = 50, \
              sha_diff_degrees     = 335, \
              sha_diff_minutes     = 20 \
              )


collection = SightCollection ([a, b, c])
intersections = collection.get_intersections (limit=500)
print ("Location = " + get_representation(intersections,1))
print ("GM = " + get_google_map_string (intersections,2))
print ("MD = " + collection.get_map_developers_string())

#Diagnostics for map rendering etc.
print ("")
print ("Some useful data follows (Small circles of equal altitude). \
       For plotting in map software etc.")
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
