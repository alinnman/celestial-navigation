''' Simple sample representing a trip at sea with supporting celestial navigation
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)       
'''

from time import time
from starfix import LatLonGeodetic, LatLon, get_representation,\
                    get_great_circle_route, Circle, CircleCollection, get_intersections,\
                    EARTH_CIRCUMFERENCE, get_google_map_string
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLonGeodetic (57.662, 18.263)
    # We start out at a course of 355 degrees
    c_course = 355
    course_gc = get_great_circle_route (s1, c_course)

    # This is a position of a lighthouse
    light_house = LatLonGeodetic (58.7396, 17.8657)
    light_house_gc = light_house.get_latlon()
    # The intercept angle for the lighthouse is 300 degrees
    light_house_intercept = 270
    light_house_gcr = get_great_circle_route (light_house_gc, light_house_intercept)

    print ("--------- Sight Reduction  --------- ")
    # print (get_google_map_string(LatLonGeodetic(ll=light_house_gcr.latlon),4))

    # Get the intersections
    intersections = get_intersections (course_gc, light_house_gcr, estimated_position=s1)
    endtime = time ()
    the_coord = intersections [0]
    assert isinstance (the_coord, LatLon)
    the_coord = LatLonGeodetic (ll=the_coord)
    print (get_representation(the_coord,1))
    print (get_google_map_string(the_coord,4))

    print ("--------- Mapping          --------- ")
    intersection1 = Circle (the_coord,1/60,circumference=EARTH_CIRCUMFERENCE)
    start         = Circle (s1, 1/60, circumference=EARTH_CIRCUMFERENCE)
    light_house_circle = Circle (light_house, 1/60, circumference=EARTH_CIRCUMFERENCE)

    c_c = CircleCollection ([intersection1, start, light_house_circle])
    print ("MD = " + c_c.get_map_developers_string())

    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
