''' This is a sample for celestial navigation for a stationary observer 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

    This sample uses an algorithm for better accuracy using repeated
    refinements of the DR position. 
'''

from time import time
from starfix import Sight, SightCollection, get_representation,\
                    get_google_map_string, IntersectError, LatLonGeodetic, Circle



def get_starfixes (drp_pos : LatLonGeodetic,
                   alt_sigma : float = 0.0,
                   time_sigma : float = 0.0) -> SightCollection :
    ''' Returns a list of used star fixes (SightCollection) '''

    Sight.set_estimated_position (drp_pos)
    Sight.set_alt_diff           (alt_sigma)
    Sight.set_time_diff          (time_sigma)

    TEMPERATURE = 10
    DT_DH = -0.01

    a = Sight (object_name          = "Sun",
               set_time             = "2024-05-05 15:55:18+00:00",
               gha_time_0           = "45:50.4",
               gha_time_1           = "60:50.4",
               decl_time_0          = "16:30.6",
               decl_time_1          = "16:31.3",
               measured_alt         = "55:7:54.4",
               temperature          = TEMPERATURE,
               dt_dh                = DT_DH
               )

    b = Sight (object_name          = "Sun",
               set_time             = "2024-05-05 23:01:19+00:00",
               gha_time_0           = "165:50.8",
               gha_time_1           = "180:50.8",
               decl_time_0          = "16:36.2",
               decl_time_1          = "16:36.9",
               measured_alt         = "19:28:27.4",
               temperature          = TEMPERATURE,
               dt_dh                = DT_DH
               )

    c = Sight (object_name          = "Vega",
               set_time             = "2024-05-06 04:04:13+00:00",
               gha_time_0           = "284:30.4",
               gha_time_1           = "299:32.9",
               decl_time_0          = "38:48.1",
               measured_alt         = "30:16:15.7",
               sha_diff             = "80:33.4",
               temperature          = TEMPERATURE,
               dt_dh                = DT_DH
               )
    return SightCollection ([a, b, c])

def main ():
    ''' Main body of script.'''

    starttime = time ()
    # the_pos = LatLonGeodetic (-40, 90) # BAD DRP position
    the_pos = LatLonGeodetic (40, -90) # Rough DRP position
    assume_good_pos = True
    # The exact position is 41°51'00.1"N 87°39'00.2"W

    try:
        intersections, _, _, collection =\
              SightCollection.get_intersections_conv (return_geodetic=True,
                                                      estimated_position=the_pos,
                                                      get_starfixes=get_starfixes,
                                                      assume_good_estimated_position=\
                                                      assume_good_pos)
    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        if ve.coll_object is not None:
            if isinstance (ve.coll_object, SightCollection):
                print ("Check the circles! " +
                        ve.coll_object.get_map_developers_string(geodetic=True))
        raise ve

    assert intersections is not None
    assert collection is not None
    endtime = time ()
    taken_ms = round((endtime-starttime)*1000,3)
    print (get_representation(intersections,1))
    assert isinstance (intersections, LatLonGeodetic)
    print ("MD = " + collection.get_map_developers_string(geodetic=True, viewpoint=intersections))
    print ("GM = " + get_google_map_string(intersections,4))

    int_circle = Circle (intersections, 0.01)
    print ("INT = " + int_circle.get_map_developers_string(include_url_start=True))

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
        counter += 1
        print (str(counter) + " radius = " +\
                str(round(s.get_circle(geodetic=True).get_radius (),1)))
        print (str(counter) + " GP     = " +\
                get_google_map_string(LatLonGeodetic(ll=s.gp),4))

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
