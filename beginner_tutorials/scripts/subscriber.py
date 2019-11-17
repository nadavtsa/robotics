#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from beginner_tutorials.srv import *

def is_circle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 4, 20, 
    param1=50, param2=30, minRadius=0, maxRadius=0)
    if circles is None:
        return False
    detected_circles = np.uint16(np.around(circles))
    return len(list(detected_circles)[0]) >= 1

def detect_color(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red = ("red", np.array([0, 127, 127]), np.array([20, 255, 255]))
    yellow =("yellow", np.array([21, 127, 127]), np.array([35, 255, 255]))
    green= ("green", np.array([36, 127, 127]), np.array([60, 255, 255]))
    for color in [red, yellow, green]:
        lower = color[1]
        upper = color[2]
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        if is_circle(result):
            return color[0]
    return None


def send_color_to_service(color):
    rospy.wait_for_service("Color")
    try:
        server_done = rospy.ServiceProxy('Color', Colorsrv)
        resp = server_done(color)
        print(resp.response)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
    

def my_callback(ros_img):
    bridge = CvBridge()
    img = None
    try:
        img = bridge.imgmsg_to_cv2(ros_img, "bgr8")
    except CvBridgeError as error:
        print(error)
        exit()
    color = detect_color(img)
    print(color)
    send_color_to_service(color)
    

def subscriber():
    rospy.init_node('image_processor', anonymous=True)
    rospy.Subscriber('images', Image, callback=my_callback)
    rospy.spin()

if __name__ == "__main__":
    subscriber()    
    
