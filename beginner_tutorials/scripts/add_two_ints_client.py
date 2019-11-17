#!/usr/bin/env python

import sys
import rospy
from beginner_tutorials.srv import *

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        resp1 = add_two_ints(x, y)
        return resp1.sum
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    x = 0
    y = 1
    try: 
        while not rospy.is_shutdown():
            print "Requesting %s+%s"%(x, y)
            print "%s + %s = %s"%(x, y, add_two_ints_client(x, y))
            x = x + 1
            y = y + 1
    except InterruptedError as e:
        print(e)
    
    
