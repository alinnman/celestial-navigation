''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    A simple test using Stellarium data. Moon altitude used, and parallax values used. 
'''

from time import time
from starfix import Sight, SightCollection, get_representation,\
                    get_google_map_string, IntersectError, LatLonGeodetic, LatLonGeocentric


def main ():
    ''' Main body of script '''

    starttime = time ()

    # Our starfix data

    the_pos = LatLonGeodetic (37, 10)

    a = Sight (   object_name          = "Capella",
                set_time             = "2024-09-17 23:36:13+00:00",
                gha_time_0           = "342:21.9",
                gha_time_1           = "357:24.4",
                decl_time_0          = "46 :1.2",
                sha_diff             = "280:22.3",
                measured_alt         = "33 :9    :34",
                estimated_position   = the_pos
                )

    b = Sight (   object_name          = "Moon",
                set_time             = "2024-09-17 23:41:13+00:00",
                gha_time_0           = "347:55.7" ,
                gha_time_1           = "2  :24.6",
                decl_time_0          = "-3 :43.5",
                decl_time_1          = "-3 :25.3",
                horizontal_parallax  = 61.2,
                measured_alt         = "48 :22  :5.2"
                )

    c = Sight (   object_name          = "Vega",
                set_time             = "2024-09-17 23:46:13+00:00",
                gha_time_0           = "342:21.9",
                gha_time_1           = "357:24.4",
                decl_time_0          = "38 :48.6",
                sha_diff             = "80 :33.3",
                measured_alt         = "25 :39:4"
                )

    collection = SightCollection ([a,b,c])
    try:
        intersections, _, _ = collection.get_intersections (return_geodetic=True)
    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        print ("Check the circles! " + collection.get_map_developers_string(geodetic=True))
        exit ()
    endtime = time ()
    taken_ms = round((endtime-starttime)*1000,2)
    print (get_representation(intersections,1))
    assert isinstance (intersections, LatLonGeodetic)
    print ("MD = " + collection.get_map_developers_string(geodetic=True, viewpoint=intersections))
    print ("GM = " + get_google_map_string(intersections,4))

    #Diagnostics for map rendering etc.
    print ("Some useful data follows")
    print ("A radius = " + str(round(a.get_circle(geodetic=True).get_radius(),1)))
    print ("A GP     = " + get_google_map_string(LatLonGeodetic(ll=a.gp),4))

    print ("B radius = " + str(round(b.get_circle(geodetic=True).get_radius(),1)))
    print ("B GP     = " + get_google_map_string(LatLonGeodetic(ll=b.gp),4))

    print ("C radius = " + str(round(c.get_circle(geodetic=True).get_radius(),1)))
    print ("C GP     = " + get_google_map_string(LatLonGeodetic(ll=c.gp),4))

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
