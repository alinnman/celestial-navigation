from starfix import Sight, SightTrip, getRepresentation, getGoogleMapString


# We are sailing from point s1 to point s2, in the Baltic Sea.  
# Point s1 is located near the coast and we get this coordinate using approximate land-based navigation (or from a previous sight)

s1LonLat = (18, 59)

#This is the star fix for s1, the starting point

s1 = Sight (  object_name          = "Sun", \
              time_year            = 2024, \
              time_month           = 6, \
              time_day             = 20, \
              time_hour            = 6, \
              time_minute          = 14, \
              time_second          = 38, \
              gha_time_0_degrees   = 269, \
              gha_time_0_minutes   = 35.2, \
              gha_time_1_degrees   = 284 , \
              gha_time_1_minutes   = 35.1, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 26.2, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 26.2, \
              measured_alt_degrees = 30, \
              measured_alt_minutes = 51, \
              measured_alt_seconds = 27.1 \
              )
   

# Point s2 is located roughly 20 nautical miles out in the sea. 

# We take a sight here and get this. 
          
s2 = Sight (  object_name          = "Sun", \
              time_year            = 2024, \
              time_month           = 6, \
              time_day             = 20, \
              time_hour            = 7, \
              time_minute          = 14, \
              time_second          = 38, \
              gha_time_0_degrees   = 284, \
              gha_time_0_minutes   = 35.1, \
              gha_time_1_degrees   = 299 , \
              gha_time_1_minutes   = 35.0, \
              decl_time_0_degrees  = 23, \
              decl_time_0_minutes  = 26.2, \
              decl_time_1_degrees  = 23, \
              decl_time_1_minutes  = 26.2, \
              measured_alt_degrees = 38, \
              measured_alt_minutes = 34, \
              measured_alt_seconds = 21.6 \
              )

# We reach s2 by applying about 175 degrees for 1 hour with a speed of 20 knots. 
cCourse = 175
speed = 20
st = SightTrip (sightStart = s1,\
                 sightEnd = s2,\
                 estimatedStartingPointLAT = s1LonLat[1],\
                 estimatedStartPointLON    = s1LonLat[0],\
                 courseDegrees             = cCourse,\
                 speedKnots                = speed)
intersections = st.getIntersections ()
print ("Starting point = " + str(getRepresentation(intersections[1],1)))
print ("End point = " + str(getRepresentation(intersections[0],1)))


# Diagnostics for map rendering etc. 

print ("S1 radius = " + str(round(s1.getRadius (),1)))
print ("S1 GP     = " + getGoogleMapString(s1.GP,4))

print ("S2 radius = " + str(round(s2.getRadius (),1)))
print ("S2 GP     = " + getGoogleMapString(s2.GP,4))

print ("Starting point GM = " + getGoogleMapString (intersections[1],4))
print ("Ending   point GM = " + getGoogleMapString (intersections[0],4))



 