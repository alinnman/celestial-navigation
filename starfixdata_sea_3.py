''' Simple sample representing a trip at sea where celestial navigation is supporting
    celestial navigation
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)    
    
'''

from time import time
from starfix import LatLon, get_representation,\
                    get_great_circle_route, Circle, get_intersections
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLon (57.662, 18.263)
    #s1_time = datetime.fromisoformat ("2024-06-20 06:14:38+00:00")

    # We reach s2 by applying about 175 degrees with a speed of 20 knots.
    c_course = 350
    #speed = 20
    course_gc = get_great_circle_route (s1, c_course)
    light_house = LatLon (58.739439, 17.865486)
    light_house_circle = Circle (light_house, 10/60)
    intersections = get_intersections (course_gc, light_house_circle)
    endtime = time ()
    assert isinstance (intersections, tuple)
    #s2_time = datetime.fromisoformat ("2024-06-20 07:13:38+00:00")
    #s1_s2_time = calculate_time_hours (s1_time, s2_time)
    #s2 = takeout_course (s1, c_course, speed, s1_s2_time)

    # Print coord of destination
    print (get_representation(intersections[0],1))
    #print (get_representation(intersections[1],1))


    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
