#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Point

pub_status_right = rospy.Publisher('/right/eye_display/eye_status',String,queue_size=1)
pub_status_left = rospy.Publisher('/left/eye_display/eye_status',String,queue_size=1)
pub_look_right = rospy.Publisher('/right/eye_display/look_at',Point,queue_size=1)
pub_look_left = rospy.Publisher('/left/eye_display/look_at',Point,queue_size=1)

eye_status = 0
look_at_x = 0.0
look_at_y = 0.0

def joy_cb(msg):
    print("in callback")
    
    global eye_status
    global look_at_x
    global look_at_y
    look_at_pub_msg = Point()
    
    if len(msg.buttons)> 0:
        if msg.buttons[0] == 1:
            eye_status = "normal"
        elif msg.buttons[1] == 1:
            eye_status = "blink"
        elif msg.buttons[2] == 1:
            eye_status = "surprised"
        elif msg.buttons[3] == 1:
            eye_status = "sleepy"
        elif msg.buttons[4] == 1:
            eye_status = "angry"
        elif msg.buttons[5] == 1:
            eye_status = "sad"
        elif msg.buttons[6] == 1:
            eye_status = "happy"
        else:
            eye_status = "normal"
    else:
        eye_status = "normal"
    pub_status_right.publish(eye_status)
    pub_status_left.publish(eye_status)

    if len(msg.axes) > 0:
        look_at_x = float(msg.axes[0])*20.0+2.0
        look_at_y = - float(msg.axes[1])*20.0+2.0
        print(f"look_at_x = {look_at_x}, look_at_y = {look_at_y}")
    look_at_pub_msg.x = look_at_x
    look_at_pub_msg.y = look_at_y
    pub_look_left.publish(look_at_pub_msg)
    pub_look_right.publish(look_at_pub_msg)

if __name__ == '__main__':
    rospy.init_node('eye_st_from_joy')
    rospy.Subscriber('/joy',Joy, joy_cb)
    rospy.spin()
