''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

'''

from time import time
from starfix import Sight, SightCollection, get_representation,\
                    get_google_map_string, IntersectError, LatLon

def main ():
    ''' Main body of script.'''

    starttime = time ()

    # Our starfix data

    a = Sight (   object_name          = "Sun", \
                set_time             = "2024-05-05 15:55:18+00:00", \
                gha_time_0           = "45:50.4", \
                gha_time_1           = "60:50.4", \
                decl_time_0          = "16:30.6", \
                decl_time_1          = "16:31.3", \
                measured_alt         = "55:8:1.8" \
                )

    b = Sight (   object_name          = "Sun", \
                set_time             = "2024-05-05 23:01:19+00:00", \
                gha_time_0           = "165:50.8", \
                gha_time_1           = "180:50.8", \
                decl_time_0          = "16:36.2", \
                decl_time_1          = "16:36.9", \
                measured_alt         = "19:28:18" \
                )

    c = Sight (   object_name          = "Vega", \
                set_time             = "2024-05-06 04:04:13+00:00", \
                gha_time_0           = "284:30.4", \
                gha_time_1           = "299:32.9", \
                decl_time_0          = "38:48.1", \
                measured_alt         = "30:16:24.6", \
                sha_diff             = "80:33.4" \
                )

    print ("Two daytime observations of the sun")
    collection = SightCollection ([a, b])
    try:
        intersections, _, _ = collection.get_intersections ()
    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        print ("Check the circles! " + collection.get_map_developers_string())
        exit ()
    print (get_representation(intersections,1))
    print ("-----------------------------------")
    print ("We add an additional night time observation of Vega")
    collection = SightCollection ([a, b, c])
    try:
        intersections, _, _ = collection.get_intersections ()
    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        print ("Check the circles! " + collection.get_map_developers_string())
        exit ()
    endtime = time ()
    taken_ms = round((endtime-starttime)*1000,3)
    print (get_representation(intersections,1))
    print ("MD = " + collection.get_map_developers_string())
    print ("GM = " + get_google_map_string(intersections,4))

    # Check azimuth
    assert isinstance (intersections, LatLon)
    az = a.get_azimuth (intersections)
    print ("Azimuth A = " + str(round(az,2)))
    az = b.get_azimuth (intersections)
    print ("Azimuth B = " + str(round(az,2)))
    az = c.get_azimuth (intersections)
    print ("Azimuth C = " + str(round(az,2)))

    #Diagnostics for map rendering etc.
    print ("Some useful data follows")
    print ("A radius = " + str(round(a.get_radius (),1)))
    print ("A GP     = " + get_google_map_string(a.gp,4))

    print ("B radius = " + str(round(b.get_radius (),1)))
    print ("B GP     = " + get_google_map_string(b.gp,4))

    print ("C radius = " + str(round(c.get_radius (),1)))
    print ("C GP     = " + get_google_map_string(c.gp,4))

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
