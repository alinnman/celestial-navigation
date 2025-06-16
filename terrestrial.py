''' Simple sample for terrestrial navigation (landfall) 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

'''
from time import time
from starfix import get_terrestrial_position, LatLonGeodetic,\
      get_google_map_string, deg_to_rad, EARTH_RADIUS,\
      CircleCollection, show_or_display_file, folium_initialized,\
      spherical_distance

def main ():
    ''' Main body of script '''

    starttime = time ()

    # Simple sample of terrestrial navigation on three lighthouses.

    # Our three lighthouses, ordered left to right
    p1 = [LatLonGeodetic (58.7396,   17.8656),   "Landsort"]
    p2 = [LatLonGeodetic (58.594091, 17.467489), "Gustaf Dalén"]
    p3 = [LatLonGeodetic (58.60355,  17.316041), "Hävringe"]

    angle_1 = 20 # Between p1 and p2
    angle_2 = 45 # Between p2 and p3

    p, c1, c2, _, _  =\
      get_terrestrial_position (p3[0], p2[0], angle_1, p2[0], p1[0], angle_2)
    endtime = time ()
    assert isinstance (p, tuple)
    # Since no estimated position was given we assume we have a tuple

    # Select the real intersection point
    # There is a false intersection located at one of the lighthouses
    # This false intersection must be eliminated
    chosen_p = None
    limit_for_dist = 0.001
    for i in [0,1]:
        invalid = False
        for check_p in [p1[0], p2[0], p3[0]]:
            dist = spherical_distance (p[i], check_p)
            if dist < limit_for_dist:
                invalid = True
                break
        if not invalid:
            chosen_p = i
            break
    assert isinstance (chosen_p, int)
    print ("Your location = " + get_google_map_string(p[chosen_p],4))

    print ("========================")
    print ("Centerpoint 1 = " + get_google_map_string (c1.get_latlon(), 4))
    print ("Radius 1 = " + str(deg_to_rad(c1.get_angle())*EARTH_RADIUS))
    print ("Centerpoint 2 = " + get_google_map_string (c2.get_latlon(), 4))
    print ("Radius 2 = " + str(deg_to_rad(c2.get_angle())*EARTH_RADIUS))

    # Draw a map

    if folium_initialized ():
#pylint: disable=C0415
        from folium import Marker, Icon, Map
#pylint: enable=C0415
        blue = "#0000FF"

        circ_coll = CircleCollection ([c1, c2])

        the_map = circ_coll.render_folium (center_pos = p[chosen_p], adjust_geodetic=False,\
                                           colors=[blue,blue])
        assert isinstance (the_map, Map)
        Marker (location=[p1[0].get_lat(),p1[0].get_lon()],\
                icon=Icon(icon="info", prefix="fa"),\
                popup=p1[1]+ " " +  str(p1[0]),\
                tooltip=p1[1]).add_to(the_map)
        Marker (location=[p2[0].get_lat(),p2[0].get_lon()],\
                icon=Icon(icon="info", prefix="fa"),\
                popup=p2[1]+ " " +  str(p2[0]),\
                tooltip=p2[1]).add_to(the_map)
        Marker (location=[p3[0].get_lat(),p3[0].get_lon()],\
                icon=Icon(icon="info", prefix="fa"),\
                popup=p3[1]+ " " +  str(p2[0]),\
                tooltip=p3[1]).add_to(the_map)

        Marker (location=[p[chosen_p].get_lat(), p[chosen_p].get_lon()],\
                icon=Icon(icon="home", prefix="fa"),\
                popup="You are here " + str(p[0]),\
                tooltip="You are here").add_to(the_map)

        file_name = "./map.html"
        the_map.save (file_name)
        show_or_display_file (file_name)

    taken_ms = round((endtime-starttime)*1000,2)
    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
