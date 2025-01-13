''' Simple sample representing a trip at sea with supporting celestial navigation
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)       
'''

from time import time
from starfix import LatLon, get_representation,\
                    get_great_circle_route, Circle, CircleCollection, get_intersections,\
                    EARTH_CIRCUMFERENCE
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLon (57.662, 18.263)
    # We start out at a course of 355 degrees
    c_course = 355
    course_gc = get_great_circle_route (s1, c_course)

    # This is a position of a lighthouse
    light_house = LatLon (58.739, 17.865)
    # The intercept angle for the lighthouse is 300 degrees
    light_house_intercept = 300
    light_house_gc = get_great_circle_route (light_house, light_house_intercept)

    # Get the intersections
    intersections = get_intersections (course_gc, light_house_gc)
    endtime = time ()
    assert isinstance (intersections[0], tuple)
    print (get_representation(intersections[0],1))

    intersection1 = Circle (intersections[0][0],1/60,circumference=EARTH_CIRCUMFERENCE)
    start         = Circle (s1, 1/60,                circumference=EARTH_CIRCUMFERENCE)

    # Check the circles
    c_c = CircleCollection ([course_gc, light_house_gc, intersection1, start])
    print ("MD = " + c_c.get_map_developers_string())

    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
