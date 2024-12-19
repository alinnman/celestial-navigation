''' Simple sample representing a trip at sea where celestial navigation is supporting
    celestial navigation
    © August Linnman, 2024, email: august@linnman.net
    MIT License (see LICENSE file)    
    
'''

from datetime import datetime
from time import time
from starfix import takeout_course, LatLon, calculate_time_hours, get_representation
def main ():
    ''' Main body of script '''

    starttime = time ()

    # We are sailing from point s1 to point s2, in the Baltic Sea.
    # We have a good estimate of an initial position. (A previous fix)
    s1 = LatLon (58.23,17.91)
    s1_time = datetime.fromisoformat ("2024-06-20 06:14:38+00:00")

    # We reach s2 by applying about 175 degrees with a speed of 20 knots.
    c_course = 175
    speed = 20
    s2_time = datetime.fromisoformat ("2024-06-20 07:13:38+00:00")
    s1_s2_time = calculate_time_hours (s1_time, s2_time)
    s2 = takeout_course (s1, c_course, speed, s1_s2_time)

    # Print coord of destination
    print (get_representation(s2,1))

    endtime = time ()
    taken_ms = round((endtime-starttime)*1000,2)

    print ("Time taken = " +str(taken_ms)+" ms")

if __name__ == '__main__':
    main()
