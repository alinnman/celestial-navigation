''' Simple sample representing a trip at sea with supporting celestial navigation
    © August Linnman, 2024, email: august@linnman.net
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
    s1_gc = s1.get_latlon()
    # We start out at a course of 355 degrees
    c_course = 355
    course_gc = get_great_circle_route (s1, c_course)

    # This is a position of a lighthouse
    light_house = LatLonGeodetic (58.7396, 17.8657)
    light_house_gc = light_house.get_latlon()
    # The intercept angle for the lighthouse is 300 degrees
    light_house_intercept = 260 
    light_house_gcr = get_great_circle_route (light_house_gc, light_house_intercept)
    print (get_google_map_string(LatLonGeodetic(ll=light_house_gcr.latlon),4))

    # Get the intersections
    intersections = get_intersections (course_gc, light_house_gcr, estimated_position=s1)
    endtime = time ()
    #assert isinstance (intersections[0], LatLon)
    print (get_representation(intersections[0],1))
    assert isinstance (intersections[0], LatLon)
    intersections_gd = LatLonGeodetic(ll=intersections[0])
    print (get_google_map_string(intersections_gd,4))

    intersection1 = Circle (intersections_gd,1/60,circumference=EARTH_CIRCUMFERENCE)
    intersection1.make_geodetic()
    start         = Circle (s1, 1/60, circumference=EARTH_CIRCUMFERENCE)
    start.make_geodetic()
    light_house_circle = Circle (light_house, 1/60, circumference=EARTH_CIRCUMFERENCE)

    # Check the circles
    course_gc.make_geodetic()
    #light_house_gcr.make_geodetic()
    c_c = CircleCollection ([intersection1, start, light_house_circle])
    #c_c.make_geodetic()
    print ("MD = " + c_c.get_map_developers_string())

    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
