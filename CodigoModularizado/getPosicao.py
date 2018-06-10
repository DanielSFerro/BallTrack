#!/usr/bin/env python
# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import rospy
from geometry_msgs.msg import Point
import struct
import serial #import the serial library

ser = serial.Serial() #create an object to read a serial
ser.baudrate=9600 
ser.port = '/dev/ttyACM0' #change it if it's isn't the right port for you
ser.open()
x=0
y=0


def listener():
 
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", Point, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def callback(data):
    #rospy.loginfo(data)
    y=data.y
    x=data.x
    #print (x,y)	
    vel_linear=0
    vel_angular=0
    if y>350:
	flag=2
    elif x<100:
	flag=-1
    elif x>400:
	flag=1
    else:
	flag=0
	if y<300:
		vel_linear = 30
	else: 
		vel_linear= 30 * (400-y) / 400
	if x<340 and x>300:    
   		 vel_angular = 0                
     	else:
        	vel_angular = (x-250) * .4/100
    comando=str(vel_linear)+','+ str(vel_angular)+','+str(flag)+'\n'+'\0' #vel_linear,vel_angular,FLAG_esteira
	
    print comando
    ser.write(comando)
	
    key = cv2.waitKey(1) & 0xFF

    #if the 'q' key is pressed, stop the loop
    if key == ord("q"):
	ser.close()
	exit()
listener()
