''' Simple sample representing a trip at sea with supporting celestial navigation
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)       
'''

from time import time
from starfix import Sight, SightTrip, get_representation, get_google_map_string,\
     LatLonGeodetic, IntersectError

def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1 to point s2, in the Baltic Sea.
    # We have a rough estimate of an initial position of 59N;18E to start with
    # This estimate is used for selecting the correct intersection point on Earth.
    s1_latlon = LatLonGeodetic (59, 18)

    #This is the star fix for s1, the starting point

    s1 = Sight (  object_name          = "Sun",
                set_time             = "2024-06-20 06:14:38+00:00",
                gha_time_0           = "269:35.2",
                gha_time_1           = "284:35.1",
                decl_time_0          = "23:26.2",
                measured_alt         = "30:51:27.1",
                estimated_position   =  s1_latlon
                )


    # Point s2 is located roughly 20 nautical miles out in the sea.

    # We take a sight here and get this.

    s2 = Sight (  object_name          = "Sun",
                set_time             = "2024-06-20 07:13:38+00:00",
                gha_time_0           = "284:35.1",
                gha_time_1           = "299:35.0",
                decl_time_0          = "23:26.2",
                measured_alt         = "38:34:21.6",
                estimated_position   = s1_latlon
                )

    # We reach s2 by applying about 175 degrees with a speed of 20 knots.
    c_course = 175
    speed = 20
    st = SightTrip (sight_start               = s1,\
                    sight_end                = s2,\
                    estimated_starting_point = s1_latlon,\
                    course_degrees           = c_course,\
                    speed_knots              = speed)

    try:
        intersections, _, _ = st.get_intersections ()
    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        print ("Check the circles! " + st.get_map_developers_string(geodetic=False))
        exit ()

    endtime = time ()
    taken_ms = round((endtime-starttime)*1000,2)

    print ("MD = " + st.get_map_developers_string (geodetic=False))
    assert isinstance (intersections, tuple)
    print ("Starting point = " + str(get_representation(intersections[1],1)))
    print ("End point = " + str(get_representation(intersections[0],1)))
    #print ("Distance = " +\
    #       str(round(km_to_nm(distance_between_points(intersections[0], intersections[1])),2)) +\
    #          " nm")

    # Diagnostics for map rendering etc.

    print ("S1 radius = " + str(round(s1.get_circle(geodetic=False).get_radius (),1)))
    print ("S1 GP     = " + get_google_map_string(s1.gp,4))

    print ("S2 radius = " + str(round(s2.get_circle(geodetic=False).get_radius (),1)))
    print ("S2 GP     = " + get_google_map_string(s2.gp,4))

    print ("Starting point GM = " + get_google_map_string (intersections[1],4))
    print ("Ending   point GM = " + get_google_map_string (intersections[0],4))



    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
