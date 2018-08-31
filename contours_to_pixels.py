import cv2
import numpy as np

#Input: Tupled contour list, thresholded image
#Output: List where each element is a list of coordinates
def contours_to_pixels(contours, img, image):
	print("Converting contours to pixels...")
	
	#Initialise an empty list for the coordinate lists
	coords_list = []

	#Loop over the contours
	for element in contours:

		#Initialise an empty list for the coordinates
		coords = []

		#Loop over the contours in the tuples
		for i in range(len(element)):

			#Create a mask of zeroes with same dimension as the thresholded image
			cimg = np.zeros_like(img)
			#Construct a thresholded image that has the pixels within the contour as white
			cv2.drawContours(cimg, element, i, color=255, thickness=-1)

			#Add the coordinates to the coords list
			rows, cols = np.where(cimg == 255)
			for i in range(len(rows)):
				coords.append((rows[i], cols[i]))

		#Add the coords list to coords_list list
		coords_list.append(coords)
		
		return coords_list