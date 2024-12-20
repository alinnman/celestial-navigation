''' Simple sample for terrestrial navigation (landfall) 
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)

'''
from time import time
from starfix import get_terrestrial_position, LatLon,\
      get_google_map_string, deg_to_rad, EARTH_RADIUS,\
      Circle, CircleCollection

def main ():
    ''' Main body of script '''

    starttime = time ()

    # Simple sample of terrestrial navigation on three lighthouses.

    # Our three lighthouses
    p1 = LatLon (58.739439, 17.865486)
    p2 = LatLon (58.594091, 17.467489)
    p3 = LatLon (58.60355, 17.316041)

    angle_1 = 20
    angle_2 = 45

    p, c1, c2, _, _  =\
      get_terrestrial_position (p3, p2, angle_1, p2, p1, angle_2)
    endtime = time ()    
    assert isinstance (p, tuple)
    print ("Your location 1 = " + get_google_map_string(p[0],4))
    print ("Your location 2 = " + get_google_map_string(p[1],4))


    print ("========================")
    print ("Centerpoint 1 = " + get_google_map_string (c1.latlon, 4))
    print ("Radius 1 = " + str(deg_to_rad(c1.angle)*EARTH_RADIUS))
    print ("Centerpoint 2 = " + get_google_map_string (c2.latlon, 4))
    print ("Radius 2 = " + str(deg_to_rad(c2.angle)*EARTH_RADIUS))

    # Draw a map
    circ1 = Circle (p1, 1/120)
    circ2 = Circle (p2, 1/120)
    circ3 = Circle (p3, 1/120)
    circ4 = Circle (c1.latlon, c1.angle)
    circ5 = Circle (c2.latlon, c2.angle)
    circ_coll = CircleCollection ([circ1, circ2, circ3, circ4, circ5])
    print ("MD = " + circ_coll.get_map_developers_string())

    taken_ms = round((endtime-starttime)*1000,2)
    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
