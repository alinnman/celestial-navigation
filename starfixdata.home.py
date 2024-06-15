from starfix import Sight, SightCollection, SightTrip, LatLon,getRepresentation, getGoogleMapString, distanceBetweenPoints, EARTH_CIRCUMFERENCE


# This is observations from actual sextant readings. 
# I used a simple plastic sextant (Davis Mk III) and an artificial horizon. 
# THIS IS JUST TEST DATA. 
     
a = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 8,\
              time_hour            = 13, \
              time_minute          = 56, \
              time_second          = 6, \
              gha_time_0_degrees   = 15, \
              gha_time_0_minutes   = 12.3, \
              gha_time_1_degrees   = 30, \
              gha_time_1_minutes   = 12.2, \
              decl_time_0_degrees  = 22, \
              decl_time_0_minutes  = 55.0, \
              decl_time_1_degrees  = 22, \
              decl_time_1_minutes  = 55.2, \
              measured_alt_degrees = 81, \
              measured_alt_minutes = 51, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True, \
              index_error_minutes  = 0
              )

b = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 9,\
              time_hour            = 6, \
              time_minute          = 57, \
              time_second          = 0, \
              gha_time_0_degrees   = 270, \
              gha_time_0_minutes   = 10.2, \
              gha_time_1_degrees   = 285, \
              gha_time_1_minutes   = 10.0, \
              decl_time_0_degrees  = 22, \
              decl_time_0_minutes  = 58.5, \
              decl_time_1_degrees  = 22, \
              decl_time_1_minutes  = 58.7, \
              measured_alt_degrees = 72, \
              measured_alt_minutes = 9, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True,\
              index_error_minutes  = 0
              )
              
c = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 13,\
              time_hour            = 15, \
              time_minute          = 3, \
              time_second          = 41, \
              gha_time_0_degrees   = 44, \
              gha_time_0_minutes   = 56.6, \
              gha_time_1_degrees   = 59, \
              gha_time_1_minutes   = 56.5, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 15.5, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 15.6, \
              measured_alt_degrees = 66, \
              measured_alt_minutes = 15, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True,\
              index_error_minutes  = 0
              )

d = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 14,\
              time_hour            = 6, \
              time_minute          = 14, \
              time_second          = 40, \
              gha_time_0_degrees   = 269, \
              gha_time_0_minutes   = 54.7, \
              gha_time_1_degrees   = 284, \
              gha_time_1_minutes   = 54.5, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 17.3, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 17.4, \
              measured_alt_degrees = 61, \
              measured_alt_minutes = 56, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True,\
              index_error_minutes  = 0
              )

e = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 14,\
              time_hour            = 6, \
              time_minute          = 5, \
              time_second          = 9, \
              gha_time_0_degrees   = 269, \
              gha_time_0_minutes   = 54.7, \
              gha_time_1_degrees   = 284, \
              gha_time_1_minutes   = 54.5, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 17.3, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 17.4, \
              measured_alt_degrees = 59, \
              measured_alt_minutes = 25, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True,\
              index_error_minutes  = 0
              )

f = Sight (   object_name          = "Sun", \
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
              index_error_minutes  = 6,\
              semi_diameter_correction = 15.7
              )

g = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 15,\
              time_hour            = 13, \
              time_minute          = 2, \
              time_second          = 34, \
              gha_time_0_degrees   = 14, \
              gha_time_0_minutes   = 50.5, \
              gha_time_1_degrees   = 29, \
              gha_time_1_minutes   = 50.4, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 20.4, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 20.5, \
              measured_alt_degrees = 94, \
              measured_alt_minutes = 13, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True,\
              index_error_minutes  = 6
              )

h = Sight (   object_name          = "Sun", \
              time_year            = 2024,\
              time_month           = 6,\
              time_day             = 15,\
              time_hour            = 14, \
              time_minute          = 31, \
              time_second          = 35, \
              gha_time_0_degrees   = 29, \
              gha_time_0_minutes   = 50.4, \
              gha_time_1_degrees   = 44, \
              gha_time_1_minutes   = 50.2, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 20.5, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 20.6, \
              measured_alt_degrees = 74, \
              measured_alt_minutes = 29, \
              measured_alt_seconds = 0, \
              artificial_horizon   = True,\
              index_error_minutes  = 6
              )

i = Sight (   object_name          = "Sun", \
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
              index_error_minutes  = 6
              )

collection = SightCollection ([f, g, h, i])
#collection = SightCollection ([a, b, c, d, e, f, g])

home = LatLon (59.318659676810654, 18.04959717835501)

intersections = collection.getIntersections (estimatedPosition = LatLon(59,19))
#intersections = collection.getIntersections ()
print (getRepresentation(intersections,1))
print ("GM = " + getGoogleMapString(intersections,4))
print ("Intersection distance from home = " + str(distanceBetweenPoints(intersections, home)))

#Diagnostics for map rendering etc. 
print ("Some useful data follows") 

print ("A radius = " + str(round(a.getRadius (),1)))
print ("A GP     = " + getGoogleMapString(a.GP,4))
print ("Diff     = " + str(a.getDistanceFrom (home)))
print ("--")

print ("B radius = " + str(round(b.getRadius (),1)))
print ("B GP     = " + getGoogleMapString(b.GP,4))
print ("Diff     = " + str(b.getDistanceFrom (home)))
print ("--")

print ("C radius = " + str(round(c.getRadius (),1)))
print ("C GP     = " + getGoogleMapString(c.GP,4))
print ("Diff     = " + str(c.getDistanceFrom (home)))
print ("--")

print ("D radius = " + str(round(d.getRadius (),1)))
print ("D GP     = " + getGoogleMapString(d.GP,4))
print ("Diff     = " + str(d.getDistanceFrom (home)))
print ("--")

print ("E radius = " + str(round(e.getRadius (),1)))
print ("E GP     = " + getGoogleMapString(e.GP,4))
print ("Diff     = " + str(e.getDistanceFrom (home)))
print ("--")


print ("F radius = " + str(round(f.getRadius (),1)))
print ("F GP     = " + getGoogleMapString(f.GP,4))
print ("Diff     = " + str(f.getDistanceFrom (home)))
print ("--")

print ("G radius = " + str(round(g.getRadius (),1)))
print ("G GP     = " + getGoogleMapString(g.GP,4))
print ("Diff     = " + str(g.getDistanceFrom (home)))
print ("--")

print ("H radius = " + str(round(h.getRadius (),1)))
print ("H GP     = " + getGoogleMapString(h.GP,4))
print ("Diff     = " + str(h.getDistanceFrom (home)))
print ("--")

print ("I radius = " + str(round(i.getRadius (),1)))
print ("I GP     = " + getGoogleMapString(i.GP,4))
print ("Diff     = " + str(i.getDistanceFrom (home)))
print ("--")
print ("-----------------------------------")
 
'''
Intersection map: 
https://www.mapdevelopers.com/draw-circle-tool.php?circles=%5B%5B5460600%2C22.9198%2C-29.2284%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B6000400%2C22.9755725%2C75.5820142%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B6328800%2C23.2584%2C-45.8641%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B6569100%2C23.2852084%2C86.4208598%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B6709200%2C23.3216284%2C88.859911%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%2C%5B6807200%2C23.3013225%2C90.641288%2C%22%23AAAAAA%22%2C%22%23000000%22%2C0.4%5D%5D
'''