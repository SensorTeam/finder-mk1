# Function takes a contour in an image and returns the pixels in the contour boundary

import cv2
import numpy as np
import imutils


# Inputs: (con, img) con is the contour and img is the thresholded image
# Returns: array of tuples containing coordinates of pixels inside the contour boundary
def get_cont_pixels(con, img):
	# Initialize empty list
	coords = []

	# Create a mask image that contains the contour filled in
	cimg = np.zeros_like(img)
	cv2.drawContours(cimg, [con], 0, color=255, thickness=-1)

	# Access the image pixels and create a 1D numpy array then add to list
	rows, cols = np.where(cimg == 255)
	for i in range(len(rows)):
		coords.append((rows[i], cols[i]))

	return coords

"""
# IGNORE: Used for testing
image = cv2.imread("IMG_2396.JPG")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# threshold the image to reveal light regions in the blurred image
# any pixel with brightness greater than THRESH is set to white, everything else set to black
thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("threshold.jpg", thresh)

_,contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for con in contours:
	coords = get_cont_pixels(con, thresh)
"""

