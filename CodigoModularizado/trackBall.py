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
import freenect
import yaml
import io

pos=(0,0)
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array

def nothing(x):
	pass

def talker():
     pub = rospy.Publisher('chatter', Point, queue_size=10)
     rospy.init_node('talker', anonymous=True)
     rate = rospy.Rate(30) # 10hz
     position=Point()
     position.x=pos[0]
     position.y=pos[1]	 
     position.z=depth[pos[1],pos[0]]
     pub.publish(position)
     rospy.loginfo(position)
     rate.sleep()

#funcao para pegar a imagem profundidade do kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    #serve para suavizar a captura da profundidade
    #Limitamos o depth para 1023, removendo objetos 
    #muitos distantes e ruidos.
    np.clip(array, 0, 2**10 - 1, array)
    array >>= 2
    #Transforma o array em 8 bit array
    array = array.astype(np.uint8)
    return array

with open("./config/HSV.yaml", 'r') as stream:
    data_loaded = yaml.load(stream)

Hmin_i = data_loaded["Hmin_v"]
Hmax_i = data_loaded["Hmax_v"]
Smin_i = data_loaded["Smin_v"]
Smax_i = data_loaded["Smax_v"]
Vmin_i = data_loaded["Vmin_v"]
Vmax_i = data_loaded["Vmax_v"]


img = np.zeros((300,512,3), dtype=np.uint8)
cv2.namedWindow('image')

cv2.createTrackbar('Hmin', 'image', Hmin_i, 179, nothing)
cv2.createTrackbar('Hmax', 'image', Hmax_i, 179, nothing)
cv2.createTrackbar('Smin', 'image', Smin_i, 255, nothing)
cv2.createTrackbar('Smax', 'image', Smax_i, 255, nothing)
cv2.createTrackbar('Vmin', 'image', Vmin_i, 255, nothing)
cv2.createTrackbar('Vmax', 'image', Vmax_i, 255, nothing)


#struct

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
# if not args.get("video", False):
# 	camera = cv2.VideoCapture(1)

# otherwise, grab a reference to the video file
# else:
# 	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	# (grabbed, frame) = camera.read()

	# # if we are viewing a video and we did not grab a frame,
	# # then we have reached the end of the video
	# if args.get("video") and not grabbed:
	# 	break
	frame = get_video()
	depth = get_depth()
	#depth = cv2.erode(depth, None, iterations=2)
	#depth = cv2.dilate(depth, None, iterations=2)
	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = imutils.resize(frame, width=640, height=480)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	H_min= cv2.getTrackbarPos('Hmin','image')
	H_max= cv2.getTrackbarPos('Hmax','image')
	V_min= cv2.getTrackbarPos('Vmin','image')
	V_max= cv2.getTrackbarPos('Vmax','image')
	S_min= cv2.getTrackbarPos('Smin','image')
	S_max= cv2.getTrackbarPos('Smax','image')
	greenLower = np.array([H_min,V_min,S_min])
	greenUpper = np.array([H_max,V_max,S_max])

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	element = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, element, iterations=2)
	mask = cv2.dilate(mask, element, iterations=2)
	mask = cv2.erode(mask, element)

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
	#print pos
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
	
	cv2.imshow('Depth image',depth)

	talker()

	#print depth[pos[1],pos[0]]
	key = cv2.waitKey(1) & 0xFF
	
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
#camera.release()

data = {'Hmin_v': H_min,
		'Hmax_v': H_max,
		'Vmin_v': V_min,
		'Vmax_v': V_max,
		'Smin_v': S_min,
		'Smax_v': S_max,
        }

with io.open('./config/HSV.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

cv2.destroyAllWindows()
