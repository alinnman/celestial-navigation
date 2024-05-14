from starfix import starFix, starFixCollection, getRepresentation

# Our starfix data
        
a = starFix (date                 = "2024-05-05", \
              object_name          = "Sun", \
              time_hour            = 15, \
              time_minute          = 55, \
              time_second          = 18, \
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

b = starFix (date                 = "2024-05-05", \
              object_name          = "Sun", \
              time_hour            = 23, \
              time_minute          = 1, \
              time_second          = 19, \
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

c = starFix (date                 = "2024-05-06", \
              object_name          = "Vega", \
              time_hour            = 4, \
              time_minute          = 4, \
              time_second          = 13, \
              gha_time_0_degrees   = 284, \
              gha_time_0_minutes   = 30.4, \
              gha_time_1_degrees   = 299, \
              gha_time_1_minutes   = 32.9, \
              decl_time_0_degrees  = 38, \
              decl_time_0_minutes  = 48.1, \
              decl_time_1_degrees  = 38, \
              decl_time_1_minutes  = 48.1, \
              measured_alt_degrees = 30, \
              measured_alt_minutes = 16, \
              measured_alt_seconds = 24.6, \
              sha_diff_degrees     = 80, \
              sha_diff_minutes     = 33.4 \
              )
              



collection = starFixCollection ([a, b])
intersections = collection.getIntersections ()
#print (intersections)
print (getRepresentation(intersections,1))

collection = starFixCollection ([a, b, c])
intersections = collection.getIntersections ()
#print (intersections)
print (getRepresentation(intersections,1))
