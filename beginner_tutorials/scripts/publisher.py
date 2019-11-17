#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def publisher():
    img = cv2.imread('images/g2.png')
    pub = rospy.Publisher('images', Image, queue_size=10)
    bridge = CvBridge()
    rospy.init_node('image_sender', anonymous=True)
    publish_msg = "sent image"
    ros_img = bridge.cv2_to_imgmsg(img, "bgr8")
    pub.publish(ros_img)
    rospy.loginfo(publish_msg)
    

if __name__ == "__main__":
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass



