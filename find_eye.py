"""
==================================================================
AUTHOR: HIEN VU
LAST MODIFIED: 14-04-18
==================================================================
Locates potential eyeshine signals from an image
Finding potential eye signals from a .jpg by finding bright spots 
in the image. Does not take into account signal duality or orientation.

Modified from PyImageSearch, Rosebreck A. Original code available at
https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
==================================================================
"""

from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import math

###### SET MACROS ####

MINAREA = 10			# refine mask sizes
MAXAREA = 30000

MINCIRCULARITY = 0.65		# between 0 and 1

MAXRADIUS = 3000		# max eye radius

######################


# Returns list of contours refined by size, circularity, and radius
def mask_circles(contours):
	contours_area = []
	contours_circles = []
	contours_radius = []
	# find contours of correct area
	for con in contours:
		area = cv2.contourArea(con)
		if MINAREA < area < MAXAREA:
			contours_area.append(con)
		
			# find contours of sufficient circularity
			perimeter = cv2.arcLength(con, True)
			if perimeter == 0:
				break
			circularity = 4*math.pi*(area/(perimeter*perimeter))
			if MINCIRCULARITY < circularity < 1.0:
				contours_circles.append(con)
				
				# find contours of smaller radius			
				(x, y), radius = cv2.minEnclosingCircle(con)
				if radius < MAXRADIUS:
					contours_radius.append(con)
					
	return contours_radius

# Returns final contours of potential eye signals
def find_eye(thresh):
	# find contours
	_,cnts,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts_final = mask_circles(cnts)
	return cnts_final