# celestial-navigation
Contains a simple python script to be used for celestial navigation. <br>
Starfixes have to be obtained using a sextant, a nautical almanac and an accurate watch. <br>
The python script takes care of the sight reduction. For two fixes you will get two possible coordinates. For three or more fixes you will get one coordinate (calculated as a mean value). 

The python script only uses basic libraries (no numpy or similar) and could be installed in PyDroid to allow for use on a mobile phone. 

## 1. Creating star fixes

You create a star fix with code like this

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
                  
The data is picked from your clock, sextant and the Nautical Almanac in the following way

| Argument             | Description                                     | Remark                   |
| :-------------       | :-------------                                  | :-------------           | 
| date                 | Current day                                     | Not used in calculations. |
| object               | Name of celestial object                        | Not used in calculations. |
| time_hour            | Observation time - Hours (0-23)                 | From clock. In UTC.       |
| time_minute          | Observation time - Minutes (0-59)               | From clock. In UTC.       |
| time_second          | Observation time - Seconds (0-59)               | From clock. In UTC.       |
| gha_time_0_degrees   | GHA degrees reading for this hour         | From Nautical Almanac. For stars use GHA of Aries.   |
| gha_time_0_minutes   | GHA minutes reading for this hour         | From Nautical Almanac. Can be zero (use decimal degrees). For stars use GHA of Aries. |
| gha_time_1_degrees   | GHA degrees reading for next hour         | From Nautical Almanac. For stars use GHA of Aries.   |
| gha_time_1_minutes   | GHA minutes reading for next hour         | From Nautical Almanac. Can be zero (use decimal degrees). For stars use GHA of Aries.|
| decl_time_0_degrees  | Declination degrees reading for this hour | From Nautical Almanac.    |
| decl_time_0_minutes  | Declination minutes reading for this hour | From Nautical Almanac. Can be zero (use decimal degrees) |  | decl_time_1_degrees  | Declination degrees reading for next hour | From Nautical Almanac.    |
| decl_time_1_minutes  | Declination minutes reading for next hour | From Nautical Almanac. Can be zero (use decimal degrees) |
| measured_alt_degrees | Altitude of object in degrees (0-90)      | From sextant.  |
| measured_alt_minutes | Altitude of object in minutes (0-60)      | From sextant. Can be zero (use decimal degrees) |
| measured_alt_seconds | Altitude of object in seconds (0-60)      | From sextant. Can be zero (use decimal degrees/minutes) |
| sha_diff_degrees     | SHA of star vs Aries in degrees           | From Nautical Almanac. Only use for stars. Otherwise skip|
| sha_diff_degrees     | SHA of star vs Aries in minutes           | From Nautical Almanac. Only use for stars. Otherwise skip|

## 2. Sight reduction

### 2.1. Using two star fixes

Using two star fixes a sight reduction can be done in the following way 

    a = starfix (....Parameters....)
    b = starfix (....Parameters....)
    
    collection = starFixCollection ([a, b])
    intersections = collection.getIntersections ()
    print (intersections)
    
The result will be a tuple of **two** coordinates (intersections of two circles of equal altitude). 

The intersections are calculated using an algorithm based on [this article](https://math.stackexchange.com/questions/4510171/how-to-find-the-intersection-of-two-circles-on-a-sphere)

### 2.2 Using three or more star fixes

Using three (or more) star fixes a sight reduction can be done in the following way 

    from starfix import starFix, starFixCollection
    a = starFix (....Parameters....)
    b = starFix (....Parameters....)
    c = starFix (....Parameters....)
    
    collection = starFixCollection ([a, b, c]) # Add more star fixes if needed
    intersections = collection.getIntersections ()
    print (intersections)
    
The result will be a **single** coordinate (mean value of intersections). 

