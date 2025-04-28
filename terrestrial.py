''' Simple sample for terrestrial navigation (landfall) 
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)

'''
from time import time
from starfix import get_terrestrial_position, LatLonGeodetic,\
      get_google_map_string, deg_to_rad, EARTH_RADIUS,\
      CircleCollection, show_or_display_file, folium_initialized

def main ():
    ''' Main body of script '''

    starttime = time ()

    # Simple sample of terrestrial navigation on three lighthouses.

    # Our three lighthouses
    p1 = LatLonGeodetic (58.739439, 17.865486)
    p2 = LatLonGeodetic (58.594091, 17.467489)
    p3 = LatLonGeodetic (58.60355, 17.316041)

    angle_1 = 20
    angle_2 = 45

    p, c1, c2, _, _  =\
      get_terrestrial_position (p3, p2, angle_1, p2, p1, angle_2)
    endtime = time ()
    assert isinstance (p, tuple)
    print ("Your location 1 = " + get_google_map_string(p[0],4))
    print ("Your location 2 = " + get_google_map_string(p[1],4))


    print ("========================")
    print ("Centerpoint 1 = " + get_google_map_string (c1.get_latlon(), 4))
    print ("Radius 1 = " + str(deg_to_rad(c1.get_angle())*EARTH_RADIUS))
    print ("Centerpoint 2 = " + get_google_map_string (c2.get_latlon(), 4))
    print ("Radius 2 = " + str(deg_to_rad(c2.get_angle())*EARTH_RADIUS))

    # Draw a map

    circ_coll = CircleCollection ([c1, c2])

    if folium_initialized ():
        from folium import Marker, Icon, Map
        blue = "#0000FF"
        the_map = circ_coll.render_folium (center_pos = p2, adjust_geodetic=False,\
                                        colors=[blue,blue])
        assert isinstance (the_map, Map)
        Marker (location=[p1.get_lat(),p1.get_lon()],\
                icon=Icon(icon="info", prefix="fa"),\
                popup="Lighthouse 1" + str(p1),
                tooltip="Lighthouse 1").add_to(the_map)
        Marker (location=[p2.get_lat(),p2.get_lon()],\
                icon=Icon(icon="info", prefix="fa"),\
                popup="Lighthouse 2" + str(p2),\
                tooltip="Lighthouse 2").add_to(the_map)
        Marker (location=[p3.get_lat(),p3.get_lon()],\
                icon=Icon(icon="info", prefix="fa"),\
                popup="Lighthouse 3" + str(p3),\
                tooltip="Lighthouse 3").add_to(the_map)

        Marker (location=[p[0].get_lat(), p[0].get_lon()],\
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
