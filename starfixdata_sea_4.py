''' Simple sample representing a trip at sea with supporting celestial navigation

    Used for finding a point where you find a lighthouse at a specific bearing

    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)       
'''

from time import time
from starfix import LatLonGeodetic, LatLonGeocentric, get_representation,\
                    get_great_circle_route, CircleCollection, get_intersections,\
                    get_google_map_string, show_or_display_file, folium_initialized
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLonGeodetic (57.662, 18.263)
    # We start out at this course
    c_course = 340
    course_gc = get_great_circle_route (s1, c_course)

    # This is a position of a lighthouse
    light_house = LatLonGeodetic (58.7396, 17.8657)
    light_house_gc = light_house.get_latlon()
    # The intercept angle for the lighthouse
    light_house_intercept = 45
    light_house_gcr = get_great_circle_route (light_house_gc, light_house_intercept)

    print ("--------- Sight Reduction  --------- ")

    # Get the intersections
    intersections = get_intersections (course_gc, light_house_gcr, estimated_position=s1)
    endtime = time ()
    the_coord = intersections [0]
    assert isinstance (the_coord, LatLonGeocentric)
    the_coord = LatLonGeodetic (ll=the_coord)
    print (get_representation(the_coord,1))
    print (get_google_map_string(the_coord,4))

    print ("--------- Mapping          --------- ")

    c_c = CircleCollection ([course_gc, light_house_gcr])

    if folium_initialized():
#pylint: disable=C0415
        from folium import Marker, Icon, Map
#pylint: enable=C0415
        the_map = c_c.render_folium (light_house, ["#FF0000","#0000FF"])
        assert isinstance (the_map, Map)

        Marker (location=[s1.get_lat(), s1.get_lon()],\
                icon=Icon(icon="home", prefix="fa"),\
                popup="Starting point " + str(s1),
                tooltip="Starting point").add_to(the_map)

        Marker (location=[the_coord.get_lat(), the_coord.get_lon()],
                popup="Intercept point " + str(the_coord),
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
