import cv2
import numpy as np
from config import *

#Input: Tupled contour list, thresholded image
#Output: List where each element is a list of coordinates
def contours_to_pixels(contour_indices, contours, img, image):
	print("Converting contours to pixels...")
	
	#Initialise an empty list for the coordinate lists
	coords_list = []

	#Loop over the pairs
	for i in range(len(contour_indices)):

		#Initialise an empty list for the coordinates
		coords = []

		#Loop over each eye
		for j in range(len(contour_indices[i])):
			#If there is only one eye in the pair, stop
			contour_index = contour_indices[i][j]

			if contour_index == None:
				break

			#Create a mask of zeroes with same dimension as the thresholded image
			cimg = np.zeros_like(img)
			#Construct a thresholded image that has the pixels within the contour as white
			cv2.drawContours(cimg, contours, j, color=255, thickness=-1)

			#Add the coordinates to the coords list
			rows, cols = np.where(cimg == 255)
			for k in range(len(rows)):
				coords.append((rows[k], cols[k]))

		#Add the coords list to coords_list list
		coords_list.append(coords)

	return coords_list