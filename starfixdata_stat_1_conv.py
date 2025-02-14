''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    This sample uses an algorithm for better accuracy using repeated
    refinements of the DR position. 
'''

from time import time
from starfix import Sight, SightCollection, get_representation,\
                    get_google_map_string, IntersectError, LatLonGeodetic, spherical_distance


def get_starfixes (drp_pos : LatLonGeodetic) -> SightCollection :
    ''' Returns a list of used star fixes (SightCollection) '''

    a = Sight (   object_name          = "Sun",
                set_time             = "2024-05-05 15:55:18+00:00",
                gha_time_0           = "45:50.4",
                gha_time_1           = "60:50.4",
                decl_time_0          = "16:30.6",
                decl_time_1          = "16:31.3",
                measured_alt         = "55:8:1.1",
                estimated_position   = drp_pos
                )

    b = Sight (   object_name          = "Sun",
                set_time             = "2024-05-05 23:01:19+00:00",
                gha_time_0           = "165:50.8",
                gha_time_1           = "180:50.8",
                decl_time_0          = "16:36.2",
                decl_time_1          = "16:36.9",
                measured_alt         = "19:28:19",
                )

    c = Sight (   object_name          = "Vega",
                set_time             = "2024-05-06 04:04:13+00:00",
                gha_time_0           = "284:30.4",
                gha_time_1           = "299:32.9",
                decl_time_0          = "38:48.1",
                measured_alt         = "30:16:23.7",
                sha_diff             = "80:33.4",
                )
    return SightCollection ([a, b, c])

def main ():
    ''' Main body of script.'''

    starttime = time ()
    the_pos = LatLonGeodetic (40, -90) # Rough DRP position

    ready = False
    limit = 0.01
    intersections = None
    collection = None
    while not ready:
        # This loop will repeat the sight reduction with successively more
        # accurate DR positions
        collection = get_starfixes (the_pos)
        try:
            intersections, _, _ =\
              collection.get_intersections (return_geodetic=True)
        except IntersectError as ve:
            print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
            print ("Check the circles! " + collection.get_map_developers_string(geodetic=True))
            exit ()
        assert isinstance (intersections, LatLonGeodetic)
        the_distance = spherical_distance (the_pos, intersections)
        if the_distance < limit:
            ready = True
        else:
            the_pos = intersections

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
