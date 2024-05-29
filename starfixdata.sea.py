from starfix import Sight, SightCollection, SightTrip, getRepresentation, compassCourse, distanceBetweenPoints, KMtoNM, NMtoKM, EARTH_CIRCUMFERENCE


# We are sailing from point s1 to point s2, in the Baltic Sea.  
# Point s1 is located near the coast and we get this coordinate using land-based navigation. 

s1LonLat = (18.003624, 58.770335)

'''
This is the star fix for s1 but we don't use our sexant here, it is not needed. 

s1 = Sight (date                 = "2024-06-20", \
              object_name          = "Sun", \
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
'''    

# Point s2 is located roughly 20 nautical miles out in the sea. 

# We take a sight here and get this. 
          
s2 = Sight (date                 = "2024-06-20", \
              object_name          = "Sun", \
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
              
              
# ========== FIRST WE USE REALISTIC ("sloppy") DATA, NOT KNOWING THE LOCATION OF s2    

# We reach s2 by applying about 175 degrees for 1 hour with a speed of 20 knots. 
cCourse = 173 # Well. Nobody is perfect. 
timeInHours = 1
speed = 19
st = SightTrip (s2, s1LonLat[1], s1LonLat[0], cCourse, speed, timeInHours)
intersections = st.getIntersections ()
print (getRepresentation(intersections,1))

# ========== NOW WE REPEAT THIS WITH KNOWLEDGE OF THE EXACT COORDINATE OF s2              
   
s2LonLat = (18.05615, 58.43139)  # TRUE POINT

# Do a final check on slightly incorrect (realistic) data
checkDistance = distanceBetweenPoints (intersections [0], s2LonLat)
print ("Checked distance to true point (realistic) = " + str(round(KMtoNM(checkDistance),1)) + " nautical miles. This should be an acceptable value. ") 
   
# We reach s2 by applying the exact distances and courses. This not realistic. 
cCourse = compassCourse (s1LonLat[1], s1LonLat[0], s2LonLat[1], s2LonLat[0])

distance = distanceBetweenPoints (s1LonLat, s2LonLat)
distanceInNM = (distance / EARTH_CIRCUMFERENCE)*360*60
speed = distanceInNM

# Now calculate the trip
timeInHours = 1
st = SightTrip (s2, s1LonLat[1], s1LonLat[0], cCourse, speed, timeInHours) # REAL DATA
intersections = st.getIntersections ()
print (getRepresentation(intersections,1))

# Do a final check on perfect data. 
checkDistance = distanceBetweenPoints (intersections [0], s2LonLat)
print ("Checked distance to true point (exact) = " + str(round(KMtoNM(checkDistance),1)) + " nautical miles. This should be a *small* value. Accuracy is limited to precision in the Nautical Almanac")

