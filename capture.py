#!/usr/bin/env python
# coding=utf-8
'''
@Autor: Lethal
@Date: 2019-09-05 17:33:26
@LastEditer: Lethal
@LastEditTime : 2020-01-13 14:19:00
'''
import cv2
import sys
import math
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[3]
 
    #if int(minor_ver) < 3:
        #tracker = cv2.Tracker_create(tracker_type)
    #else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
 
    # Read video
    video = cv2.VideoCapture("1.mp4")
    #video = cv2.VideoCapture(0)
    # Exit if video not opened.
    if not video.isOpened():
        print "Could not open video"
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print 'Cannot read video file'
        sys.exit()
     
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)
    points_list = []
    speed = []
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
    x = (bbox[0] + bbox[2] / 2)
    y = (bbox[1] + bbox[3] / 2)
    points_list.append((int(x),int(y)))
    speed.append((x,y))
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    i = 0
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
        #print "position:",bbox
        x = (bbox[0] + bbox[2] / 2)
        y = (bbox[1] + bbox[3] / 2)
        print "zhongxin(",x,",",y,")"
        points_list.append((int(x),int(y)))
        speed.append((x,y))
        point_size = 1
        point_color = (0, 0, 255) # BGR
        thickness = 4 # 可以为 0 、4、8
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
        
        point_color = (0, 0, 255) # BGR
        thickness = 1
        lineType = 8
        #if len(points_list) < i+1:
        #print points_list[i]
        for i in range(len(points_list)-1):
            cv2.line(frame, points_list[i], points_list[i+1], point_color, thickness, lineType)
            speeds = math.sqrt((speed[i][0]-speed[i+1][0]) * (speed[i][0]-speed[i+1][0]) + (speed[i][1]-speed[i+1][1]) * (speed[i][1]-speed[i+1][1]))*fps
        #i = i + 1
        
        cv2.putText(frame, "SPEED : " + str(speeds), (100,500), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break