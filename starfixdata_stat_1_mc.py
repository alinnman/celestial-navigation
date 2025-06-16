''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    This sample uses an algorithm for testing the accuracy of the 
    intersection algorithm. It uses a simple Monte Carlo simulation
    using deviations of altitude and time values. 
    The "Sigma" result is a measurement of inaccuracy/instability. 
'''

from time import time
from starfix import Sight, SightCollection, get_representation,\
                    get_google_map_string, IntersectError, LatLonGeodetic,\
                    show_or_display_file


def get_starfixes (drp_pos : LatLonGeodetic,
                   alt_sigma : float = 0.0,
                   time_sigma : float = 0.0) -> SightCollection :
    ''' Returns a list of used star fixes (SightCollection) '''

    Sight.set_estimated_position (drp_pos)
    Sight.set_alt_diff           (alt_sigma)
    Sight.set_time_diff          (time_sigma)

    a = Sight ( object_name          = "Sun",
                set_time             = "2024-05-05 15:55:18+00:00",
                gha_time_0           = "45:50.4",
                gha_time_1           = "60:50.4",
                decl_time_0          = "16:30.6",
                decl_time_1          = "16:31.3",
                measured_alt         = "55:8:1.1"
                )

    b = Sight ( object_name          = "Sun",
                set_time             = "2024-05-05 23:01:19+00:00",
                gha_time_0           = "165:50.8",
                gha_time_1           = "180:50.8",
                decl_time_0          = "16:36.2",
                decl_time_1          = "16:36.9",
                measured_alt         = "19:28:19"
                )

    c = Sight ( object_name          = "Vega",
                set_time             = "2024-05-06 04:04:13+00:00",
                gha_time_0           = "284:30.4",
                gha_time_1           = "299:32.9",
                decl_time_0          = "38:48.1",
                measured_alt         = "30:16:23.7",
                sha_diff             = "80:33.4"
                )
    return SightCollection ([a, b, c])

def main ():
    ''' Main body of script.'''

    starttime = time ()
    the_pos = LatLonGeodetic (41, -88) # Rough DRP position
    max_mc_iter = 100
    # The exact position is 41°51'00.1"N 87°39'00.2"W

    intersections = collection = taken_ms = None
    found_intersections = sigma = 0
    try:
        intersections, sigma, found_intersections =\
              SightCollection.get_intersections_mc (return_geodetic=True,
                                                    estimated_position=the_pos,
                                                    get_starfixes=get_starfixes,
                                                    max_mc_iter=max_mc_iter,
                                                    alt_sigma=2,
                                                    time_sigma=2)
    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data?\n" + str(ve))
        if ve.coll_object is not None:
            if isinstance (ve.coll_object, SightCollection):
                collection = ve.coll_object

    if found_intersections < max_mc_iter:
        print ("WARNING : Only " + str(found_intersections) + " intersections could be calculated.")

    assert intersections is not None
    endtime = time ()
    taken_ms = round((endtime-starttime)*1000,3)
    print (get_representation(intersections,1))
    print ("Sigma = " + str(sigma) + " km.")
    print ("GM = " + get_google_map_string(intersections,4))

    if collection is not None and not isinstance (intersections, tuple):
        the_map = collection.render_folium (intersections)
        file_name = "./map.html"
        the_map.save (file_name)
        show_or_display_file (file_name)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
