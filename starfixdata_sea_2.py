''' Simple sample representing a trip at sea with supporting celestial navigation
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)       
'''

from datetime import datetime
from time import time
from starfix import Sight, SightTrip, get_representation,\
     LatLon, LatLonGeodetic, IntersectError, get_google_map_string,\
     km_to_nm, spherical_distance, show_or_display_file

def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1 to point s2, in the Baltic Sea.
    # We have a good estimate of an initial position. (A previous fix)
    s1_latlon = LatLonGeodetic (58.7656,18.0025)

    #This is the starting time

    s1 = datetime.fromisoformat ("2024-06-20 06:14:38+00:00")

    # Point s2 is located roughly 20 nautical miles out in the sea.

    # We take a sight here and get this.

    s2 = Sight (object_name          = "Sun",
                set_time             = "2024-06-20 07:14:38+00:00",
                measured_alt         = "38:34:21.6",
                estimated_position   = s1_latlon
                )

    # We reach s2 by applying about 175 degrees with a speed of 20 knots.
    c_course = 175
    speed = 20
    st = SightTrip (sight_start              = s1,\
                    sight_end                = s2,\
                    estimated_starting_point = s1_latlon,\
                    course_degrees           = c_course,\
                    speed_knots              = speed)

    try:
        intersections, _, _ = st.get_intersections (return_geodetic=True)

        endtime = time ()
        taken_ms = round((endtime-starttime)*1000,2)

        print ("--------- Sight Reduction  --------- ")
        assert isinstance (intersections, LatLon)
        print ("Starting point = " + str(get_representation(s1_latlon,1)))
        print ("Starting point GM = " + str(get_google_map_string(s1_latlon,4)))
        print ("End point = " + str(get_representation(intersections,1)))
        print ("End point GM = " + str(get_google_map_string(intersections,4)))
        print ("Distance travelled = " +\
                str(round(km_to_nm(spherical_distance(s1_latlon, intersections)),2)) + " nm")

        print ("--------- Some diagnostics --------- ")
        print ("S2 radius = " + str(round(s2.get_circle(geodetic=False).get_radius (),1)))
        print ("S2 GP     = " + get_google_map_string(LatLonGeodetic(ll=s2.get_gp()),4))

        print ("--------- Mapping (Folium) --------- ")
        m = st.render_folium(intersections)
        file_name = "./map.html"
        m.save (file_name)
        show_or_display_file (file_name)

        print ("Time taken = " +str(taken_ms)+" ms")

    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))

if __name__ == '__main__':
    main()
