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
              index_error_minutes  = 0,\
              semi_diameter_correction = 15.7
              )

#collection = SightCollection ([c, f])
collection = SightCollection ([a, b, c, d, e])

intersections = collection.getIntersections (estimatedPosition = LatLon(59,19))
#intersections = collection.getIntersections ()
print (getRepresentation(intersections,1))
print ("GM = " + getGoogleMapString(intersections,4))

#Diagnostics for map rendering etc. 
print ("Some useful data follows") 

#print ("A radius = " + str(round(a.getRadius (),1)))
#print ("A GP     = " + getGoogleMapString(a.GP,4))

#print ("B radius = " + str(round(b.getRadius (),1)))
#print ("B GP     = " + getGoogleMapString(b.GP,4))

print ("C radius = " + str(round(c.getRadius (),1)))
print ("C GP     = " + getGoogleMapString(c.GP,4))

#print ("D radius = " + str(round(c.getRadius (),1)))
#print ("D GP     = " + getGoogleMapString(c.GP,4))

#print ("E radius = " + str(round(e.getRadius (),1)))
#print ("E GP     = " + getGoogleMapString(e.GP,4))

print ("F radius = " + str(round(f.getRadius (),1)))
print ("F GP     = " + getGoogleMapString(f.GP,4))

print ("-----------------------------------")
 