#!/usr/bin/env python3
############## Task1.1 - ArUco Detection ##############

import numpy as np
import cv2 as cv
import cv2.aruco as aruco
import sys
import math
import time

def detect_ArUco(img):
    ## function to detect ArUco markers in the image using ArUco library
    ## argument: img is the test image
    ## return: dictionary named Detected_ArUco_markers of the format {ArUco_id_no : corners}, where ArUco_id_no indicates ArUco id and corners indicates the four corner position of the aruco(numpy array)
    ## 		   for instance, if there is an ArUco(0) in some orientation then, ArUco_list can be like
    ## 				{0: array([[315, 163],
    #							[319, 263],
    #							[219, 267],
    #							[215,167]], dtype=float32)}

    Detected_ArUco_markers = {}
    ## enter your code here ##
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters = parameters)
    Detected_ArUco_markers = dict(zip(ids[:,0], corners))
    
    return Detected_ArUco_markers


def Calculate_orientation_in_degree(Detected_ArUco_markers):
    ## function to calculate orientation of ArUco with respective to the sscale mentioned in problem statement
    ## argument: Detected_ArUco_markers  is the dictionary returned by the function detect_ArUco(img)
    ## return : Dictionary named ArUco_marker_angles in which keys are ArUco ids and the values are angles (angles have to be calculated as mentioned in the problem statement)
    ##			for instance, if there are two ArUco markers with id 1 and 2 with angles 120 and 164 respectively, the 
    ##			function should return: {1: 120 , 2: 164}

    ArUco_marker_angles = {}
    ## enter your code here ##
    for ids in Detected_ArUco_markers:
        for markerCorner in Detected_ArUco_markers.get(ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            mpX = int((topLeft[0] + topRight[0]) / 2.0)
            mpY = int((topLeft[1] + topRight[1]) / 2.0)
            lineX = int(cX - mpX)
            lineY = int(cY - mpY)
            angle = int(math.degrees(math.atan2(lineY, -lineX)))
            if angle<0:
                angle = int(360+angle)
            ArUco_marker_angles[ids] = angle
    return ArUco_marker_angles	## returning the angles of the ArUco markers in degrees as a dictionary


def mark_ArUco(img,Detected_ArUco_markers,ArUco_marker_angles):
    ## function to mark ArUco in the test image as per the instructions given in problem statement
    ## arguments: img is the test image 
    ##			  Detected_ArUco_markers is the dictionary returned by function detect_ArUco(img)
    ##			  ArUco_marker_angles is the return value of Calculate_orientation_in_degree(Detected_ArUco_markers)
    ## return: image namely img after marking the aruco as per the instruction given in problem statement

    ## enter your code here ##
    for ids in Detected_ArUco_markers:
        for markerCorner in Detected_ArUco_markers.get(ids):
                # extract the marker corners (which are always returned in
                # top-left, top-right, bottom-right, and bottom-left order)
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv.circle(img, (topLeft[0], topLeft[1]), 5, (125, 125, 125), -1)
                cv.circle(img, (topRight[0], topRight[1]), 5, (0,255,0), -1)
                cv.circle(img, (bottomRight[0], bottomRight[1]), 5, (180,105,255), -1)
                cv.circle(img, (bottomLeft[0], bottomLeft[1]), 5, (255,255,255), -1)
                mpX = int((topLeft[0] + topRight[0]) / 2.0)
                mpY = int((topLeft[1] + topRight[1]) / 2.0)
                cv.circle(img, (cX, cY), 5, (0, 0, 255), -1)
                cv.line(img, (cX, cY), (mpX, mpY), (255, 0, 0), 5)
                lineX = int(cX - mpX)
                lineY = int(cY - mpY)
                angle = int(ArUco_marker_angles.get(ids))
                if angle<0:
                    angle = int(360+angle)
                # draw the ArUco marker ID on the image
                cv.putText(img, str(ids),(cX+20, cY), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                cv.putText(img, str(angle),(cX-80, cY), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)            
    return img


