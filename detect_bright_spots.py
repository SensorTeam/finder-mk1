from imutils import contours
from skimage import measure
from .diagnostic_tool import *
import numpy as np
import imutils
import cv2
from config import *

#Input: JPG image
#Outputs: Contours corresponding to bright patches in the JPG image, thresholded image
def detect_bright_spots(image):
	print("Finding bright spots...")
	# load the image, convert it to grayscale, and blur it
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (11, 11), 0)


	# threshold the image to reveal light regions in the
	# blurred image
	thresh = cv2.threshold(blurred, MIN_THRESHOLD, MAX_THRESHOLD, cv2.THRESH_BINARY)[1]

	# perform a series of erosions and dilations to remove
	# any small blobs of noise from the thresholded image
	thresh = cv2.erode(thresh, None, iterations=2)
	thresh = cv2.dilate(thresh, None, iterations=4)
	show_thresh(thresh)
	# perform a connected component analysis on the thresholded
	# image, then initialize a mask to store only the "large"
	# components
	labels = measure.label(thresh, neighbors=8, background=0)
	mask = np.zeros(thresh.shape, dtype="uint8")

	# loop over the unique components
	for label in np.unique(labels):
		# if this is the background label, ignore it
		if label == 0:
			continue

		# otherwise, construct the label mask and count the
		# number of pixels 
		labelMask = np.zeros(thresh.shape, dtype="uint8")
		labelMask[labels == label] = 255
		numPixels = cv2.countNonZero(labelMask)

		# if the number of pixels in the component is sufficiently
		# large, then add it to our mask of "large blobs"
		print(numPixels)
		if MIN_NUM_PIXELS < numPixels < MAX_NUM_PIXELS:
			mask = cv2.add(mask, labelMask)

	# find the contours in the mask, then sort them from left to
	# right
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	print(cnts)
	# put through dark surround test
	final_cnts = []
	if (len(cnts) == 0):
		pass
	else:
		cnts = contours.sort_contours(cnts)[0]
		for cnt in cnts:
			if (dark_surround(cnt, gray)):
				final_cnts.append(cnt)
	print(final_cnts)
	return final_cnts, thresh



# return list of contours that pass the 'dark surround' test
# NAE signals will have higher contrast between the eye and its
# immediate surroundings, as the animals face will generally appear much darker.
def dark_surround(contours, gray):

	final_contours = []

	# Create a mask of zeroes with same dimension as the thresholded image
	simg = np.zeros_like(gray)

	contours = [contours]	# so that it works with cv2.drawContours()
	# Construct a thresholded image that has radius of 4 pixels around the contour white
	cv2.drawContours(simg, contours, 0, color=255, thickness=50)
	# Add the contour in grey
	cv2.drawContours(simg, contours, 0, color=100, thickness=-1)
	# cv2.imwrite("simg.jpg", simg)
	# cv2.imshow("simg",simg)
	# cv2.waitKey(0)

	#Initialise an empty list for the coordinate lists
	surr_coords = []
	cont_coords = []

	# Surrounding area total brightness, surrounding area total pixels
	# Contour total brightness, contour total pixels
	surr_tot, surr_pix = 0, 0
	cont_tot, cont_pix = 0, 0

	rows, cols = np.where(simg == 255)
	for k in range(len(rows)):
		x, y = rows[k], cols[k]
		surr_tot += gray[x,y]
		surr_pix += 1
		surr_coords.append((x,y))

	crows, ccols = np.where(simg == 100)
	for k in range(len(crows)):
		x, y = crows[k], ccols[k]
		cont_tot += gray[x,y]
		cont_pix += 1
		cont_coords.append((x,y))


	# print(cont_tot/cont_pix, surr_tot/surr_pix)
	surr_contrast = (cont_tot/cont_pix) - (surr_tot/surr_pix) 	# the contrast between the eye and its surrounding area
	# print("surrounding contrast: %s" % surr_contrast)
	if surr_contrast > MIN_SURROUNDING_CONTRAST:
		return True
	else:
		return False
