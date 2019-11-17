#!/usr/bin/env python

import rospy
from beginner_tutorials.srv import Colorsrv, ColorsrvResponse

def handle_color(req):
    color = req.color
    response = None
    if color == "red":
        response = "stop"
    elif color == "yellow":
        response = "wait"
    elif color == "green":
        response = "go"
    print(response)
    return ColorsrvResponse("done")

def color_server():
    rospy.init_node("color_server")
    service = rospy.Service('Color', Colorsrv, handle_color)
    rospy.spin()
    
if __name__ == "__main__":
    color_server()