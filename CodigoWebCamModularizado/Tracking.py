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

pos=(0,0) 

def nothing(x):
	pass

def talker():
     pub = rospy.Publisher('chatter', Point, queue_size=10)
     rospy.init_node('talker', anonymous=True) # initialize node
     rate = rospy.Rate(30) # 30hz
     position=Point() 
     position.x=pos[0] # position.x holds the "x" coordinate
     position.y=pos[1]  # position.y holds the "y" coordinate
     pub.publish(position) #send message
     rospy.loginfo(position) #show position on the screen
     rate.sleep()

img = np.zeros((300,512,3), dtype=np.uint8)
cv2.namedWindow('image') 

#create trackbars
cv2.createTrackbar('Hmin', 'image', 0, 255, nothing)
cv2.createTrackbar('Vmin', 'image', 0, 255, nothing)
cv2.createTrackbar('Smin', 'image', 0, 255, nothing)
cv2.createTrackbar('Hmax', 'image', 0, 255, nothing)
cv2.createTrackbar('Vmax', 'image', 0, 255, nothing)
cv2.createTrackbar('Smax', 'image', 0, 255, nothing) 

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "orange"
# ball in the HSV color space, then initialize the
# list of tracked points

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	#get position of the trackbar	
	H_min= cv2.getTrackbarPos('Hmin','image')
	V_min= cv2.getTrackbarPos('Vmin','image')
	S_min= cv2.getTrackbarPos('Smin','image')
	H_max= cv2.getTrackbarPos('Hmax','image')
	V_max= cv2.getTrackbarPos('Vmax','image')
	S_max= cv2.getTrackbarPos('Smax','image')

	orangeLower = np.array([H_min,V_min,S_min]) #orangeLower holds the minimum values of the range
	orangeUpper = np.array([H_max,V_max,S_max]) #orangeUpper holds the maximum values of the range

	# construct a mask for the color "orange", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, orangeLower, orangeUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	zero=(0,0)		
	pos=zero
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			pos=center		
	# update the points queue
	pts.appendleft(center)
	
	# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	cv2.imshow("Frame", frame)

	cv2.imshow('mask',mask)
	
	talker() #send message

	key = cv2.waitKey(1) & 0xFF
      
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
