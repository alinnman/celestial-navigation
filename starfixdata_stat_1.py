''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    This sample uses an algorithm for better accuracy using repeated
    refinements of the DR position. 

    Data is picked from the nautical almanac.
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
                measured_alt         = "55:8:1.1"
                )

    b = Sight ( object_name          = "Sun",
                set_time             = "2024-05-05 23:01:19+00:00",
                measured_alt         = "19:28:19"
                )

    c = Sight ( object_name          = "Vega",
                set_time             = "2024-05-06 04:04:13+00:00",
                measured_alt         = "30:16:23.7",
                )
    return SightCollection ([a, b, c])

def main ():
    ''' Main body of script.'''

    starttime = time ()
    # the_pos = LatLonGeodetic (-40, 90) # BAD DRP position
    the_pos = LatLonGeodetic (40, -90) # Rough DRP position
    assume_good_pos = True
    # The exact position is 41°51'00.1"N 87°39'00.2"W

    intersections = collection = None
    taken_ms = 0
    try:
        intersections, _, _, collection =\
              SightCollection.get_intersections_conv (return_geodetic=True,
                                                      estimated_position=the_pos,
                                                      get_starfixes=get_starfixes,
                                                      assume_good_estimated_position=\
                                                      assume_good_pos)
        assert intersections is not None
        assert collection is not None
        endtime = time ()
        taken_ms = round((endtime-starttime)*1000,3)
        print (get_representation(intersections,1))
        assert isinstance (intersections, LatLonGeodetic)
        print ("Google Maps Coordinate = " + get_google_map_string(intersections,4))

        # Check azimuth
        assert isinstance (intersections, LatLonGeodetic)
        counter = 0
        for s in collection.sf_list:
            counter += 1
            az = s.get_azimuth (intersections)
            print ("Azimuth " + str(counter) + " = " + str(round(az,2)))

        # Diagnostics for map rendering etc.
        print ("Some useful data follows")
        counter = 0
        for s in collection.sf_list:
            assert isinstance (s, Sight)
            counter += 1
            print (str(counter) + " radius = " +\
                    str(round(s.get_circle(
                        geodetic=True).get_radius (),1)))
            print (str(counter) + " GP     = " +\
                    get_google_map_string(LatLonGeodetic(ll=s.get_gp()),4))

    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        if ve.coll_object is not None:
            if isinstance (ve.coll_object, SightCollection):
                collection = ve.coll_object

    if collection is not None and not isinstance (intersections, tuple):
        the_map = collection.render_folium (intersections)
        file_name = "./map.html"
        the_map.save (file_name)
        show_or_display_file (file_name)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
