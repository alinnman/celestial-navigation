''' Simple sample representing a trip at sea with supporting celestial navigation. 
    Used for intercept of a lighthouse or similar on a steady course. 

    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)       
'''

from time import time

from starfix import LatLonGeodetic,\
                    get_great_circle_route, Circle, CircleCollection, get_intersections,\
                    get_line_of_sight, nm_to_km, km_to_nm, EARTH_CIRCUMFERENCE,\
                    show_or_display_file, spherical_distance, folium_initialized,\
                    get_google_map_string
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLonGeodetic (57.662, 18.263)
    s1_gc = s1.get_latlon ()
    #s1_c = s1.get_latlon_geocentric ()
    # We start out at this course
    c_course = 340
    course_gc = get_great_circle_route (s1_gc,
                                        # NOTE: The s1 coordinate must be converted to geocentrical
                                        c_course)

    # This is a position of a lighthouse
    light_house = LatLonGeodetic (58.739, 17.865)
    light_house_gc = light_house.get_latlon ()
    # This is the elevation of the light source (m)
    light_house_elevation = 44.5
    # This is the maximum reach in nm
    light_house_max_visibility_nm = 22
    light_house_max_visibility_m = nm_to_km (light_house_max_visibility_nm) * 1000
    # This is the elevation of the observer (in the ship)
    observer_elevation = 3
    # Calculate the max line of sight
    line_of_sight = get_line_of_sight (light_house_elevation, observer_elevation)
    # The actual line of sight is the minimum of max reach and line of sight
    actual_line_of_sight = min (line_of_sight, light_house_max_visibility_m)
    actual_line_of_sight_nm = km_to_nm (actual_line_of_sight/1000)

    light_house_circle_gc = Circle\
          (light_house_gc, actual_line_of_sight_nm/60, circumference=EARTH_CIRCUMFERENCE)

    c_c = CircleCollection ([light_house_circle_gc, course_gc])
    endtime = time ()
    the_map = None
    if folium_initialized ():
#pylint: disable=C0415
        from folium import Marker, Map, Icon
#pylint: enable=C0415
        the_map = c_c.render_folium (light_house)
        assert isinstance (the_map, Map)
        Marker (location=[s1.get_lat(), s1.get_lon()],\
                icon=Icon(icon="home", prefix="fa"),\
                popup="Starting point " + str(s1),
                tooltip="Starting point").add_to(the_map)

    intersections = get_intersections (course_gc, light_house_circle_gc)
    assert isinstance (intersections[0], tuple)
    m1 = intersections [0][0]
    m1_d = LatLonGeodetic (ll=m1)
    m2 = intersections [0][1]
    m2_d = LatLonGeodetic (ll=m2)
    m1_dist = spherical_distance (m1, s1_gc)
    m2_dist = spherical_distance (m2, s1_gc)
    chosen_point_d = None
    if m1_dist < m2_dist:
        chosen_point_d = m1_d
    else:
        chosen_point_d = m2_d
    print ("Intercept point = " + get_google_map_string(chosen_point_d, 4))
    if folium_initialized():
#pylint: disable=C0415
        from folium import Marker, Map, Icon
#pylint: enable=C0415
        assert isinstance (the_map, Map)
        Marker (location=[chosen_point_d.get_lat(), chosen_point_d.get_lon()],
                popup="Intercept point " + str(chosen_point_d),
                tooltip = "Intercept point").add_to(the_map)
        Marker (location=[light_house.get_lat(),light_house.get_lon()],\
                icon=Icon(icon="info", prefix="fa"),\
                popup="Lighthouse " + str(s1),
                tooltip="Lighthouse").add_to(the_map)
        file_name = "./map.html"
        the_map.save (file_name)
        show_or_display_file (file_name)

    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
