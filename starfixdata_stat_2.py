''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    This sample uses an algorithm for better accuracy using repeated
    refinements of the DR position. 
'''

from time import time
from starfix import Sight, SightCollection, get_representation,\
                    get_google_map_string, IntersectError, LatLonGeodetic


def get_starfixes (drp_pos : LatLonGeodetic,
                   time_sigma : float = 0.0,
                   alt_sigma  : float = 0.0) -> SightCollection :
    ''' Returns a list of used star fixes (SightCollection) '''

    a = Sight (   object_name          = "Capella",
                set_time             = "2024-09-17 23:36:13+00:00",
                gha_time_0           = "342:21.9",
                gha_time_1           = "357:24.4",
                decl_time_0          = "46 :1.2",
                sha_diff             = "280:22.3",
                measured_alt         = "33 :9    :34",
                estimated_position   = drp_pos
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
    return SightCollection ([a, b, c])

def main ():
    ''' Main body of script.'''

    starttime = time ()
    the_pos = LatLonGeodetic (35, 10) # Rough DRP position

    try:
        intersections, _, _, collection =\
              SightCollection.get_intersections_conv (return_geodetic=True,
                                                      estimated_position=the_pos,
                                                      get_starfixes=get_starfixes)
    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        if ve.coll_object is not None:
            if isinstance (ve.coll_object, SightCollection):
                print ("Check the circles! " +
                        ve.coll_object.get_map_developers_string(geodetic=True))
        exit ()

    assert intersections is not None
    assert collection is not None
    endtime = time ()
    taken_ms = round((endtime-starttime)*1000,3)
    print (get_representation(intersections,1))
    assert isinstance (intersections, LatLonGeodetic)
    print ("MD = " + collection.get_map_developers_string(geodetic=True, viewpoint=intersections))
    print ("GM = " + get_google_map_string(intersections,4))

    # Check azimuth
    assert isinstance (intersections, LatLonGeodetic)
    counter = 0
    for s in collection.sf_list:
        counter += 1
        az = s.get_azimuth (intersections)
        print ("Azimuth " + str(counter) + " = " + str(round(az,2)))

    #Diagnostics for map rendering etc.
    print ("Some useful data follows")
    counter = 0
    for s in collection.sf_list:
        counter += 1
        print (str(counter) + " radius = " +\
                str(round(s.get_circle(geodetic=True).get_radius (),1)))
        print (str(counter) + " GP     = " +\
                get_google_map_string(LatLonGeodetic(ll=s.gp),4))

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
