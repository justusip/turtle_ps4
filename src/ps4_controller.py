#!/usr/bin/env python3
import rospy
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from m2_ps4.msg import Ps4Data

vel = 1
rospy.init_node("ps4_driver")
p = rospy.Publisher(
		"turtle1/cmd_vel", 
		Twist, 
		queue_size = 1
	)

def onControl(data):
	global vel
	vel += data.dpad_y
	vel = max(0, min(vel, 5))

	if data.ps:
		clear()

	c = None
	if data.triangle:
		c = 0, 255, 0
	if data.circle:
		c = 255, 0, 0
	if data.cross:
		c = 0, 0, 255
	if data.square:
		c = 255,0,255
	if c is not None:
		colour(r=c[0], g=c[1], b=c[2])

	t = Twist()
	t.linear.x = data.hat_ly * vel
	t.angular.z = data.hat_rx
	p.publish(t)

rospy.Subscriber("input/ps4_data", Ps4Data, onControl)
clear = rospy.ServiceProxy("/clear", Empty)
colour = rospy.ServiceProxy("/turtle1/set_pen", SetPen)
rospy.spin()