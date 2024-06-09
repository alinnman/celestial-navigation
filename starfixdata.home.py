from starfix import Sight, SightCollection, SightTrip, LatLon,getRepresentation, getGoogleMapString, distanceBetweenPoints, EARTH_CIRCUMFERENCE


# This is an observation from an actual sextant reading. 
# I used a simple plastic sextant (Davis Mk III) and an artificial horizon. 
# I also measured the index error approximately, since the sextant is hard to adjust very well. 
# The reading is accurate to 1.5 nautical miles which is very good..
        
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
              index_error_minutes  = 8
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
              index_error_minutes  = 8
              )
      
print ("Two daytime observations of the sun")
collection = SightCollection ([a, b])
intersections = collection.getIntersections (estimatedPosition = LatLon(59,19))
print (getRepresentation(intersections,1))
print ("GM = " + getGoogleMapString(intersections,4))

#Diagnostics for map rendering etc. 
print ("Some useful data follows") 
print ("A radius = " + str(round(a.getRadius (),1)))
print ("A GP     = " + getGoogleMapString(a.GP,4))

print ("B radius = " + str(round(b.getRadius (),1)))
print ("B GP     = " + getGoogleMapString(b.GP,4))

print ("-----------------------------------")
 