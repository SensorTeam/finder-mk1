import cv2
import math

#Input: List of contours
#Output: List of contours filtered so that only sufficiently circular contours remain
def circle_filter(contours):
	print("Applying circle filter to contours...")
	#Initialise empty list for new contours
	contours_new = []
	#Loop over each contour in the contours list...
	for con in contours:
		#Find the area of the contour
		area_contour = cv2.contourArea(con)
		#Find the centre position (x, y) and radius of the minimum enclosing circle
		(x, y), radius = cv2.minEnclosingCircle(con)
		#Find the area of the minimum enclosing circle
		area_circle = math.pi * radius ** 2
		#Define circularity as the ratio of the contour area to the minimum enclosing circle area
		circularity = area_contour / area_circle

		#Only add contours which satisfy the circularity requirement to the new contour list
		if 0.9 < circularity < 1.0:
			contours_new.append(con)

	return contours_new