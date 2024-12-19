''' Simple sample representing a trip at sea where celestial navigation is supporting
    celestial navigation
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)    
    
'''

from time import time
from starfix import LatLon, get_representation,\
                    get_great_circle_route, Circle, CircleCollection, get_intersections
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLon (57.662, 18.263)
    # We start out at a course of 350 degrees
    c_course = 350
    course_gc = get_great_circle_route (s1, c_course)

    # This is lighthouse with estimated visibility 10 nautical miles
    light_house = LatLon (58.739, 17.865)
    light_house_circle = Circle (light_house, 10/60)

    # Get the intersections
    intersections = get_intersections (course_gc, light_house_circle)
    endtime = time ()
    assert isinstance (intersections, tuple)
    print (get_representation(intersections[0],1))

    # Check the circles
    c_c = CircleCollection ([course_gc, light_house_circle, Circle(s1, 1/60)])
    print ("MD = " + c_c.get_map_developers_string())

    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
