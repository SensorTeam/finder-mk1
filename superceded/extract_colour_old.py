import cv2
import numpy as np
import imutils
from skimage import measure
import math
from find_pairs import *

####### SET MACROS ####

THRESH = 150		# minimum brightness

MINAREA = 10			# refine mask sizes
MAXAREA = 30000

MINCIRCULARITY = 0.8		# between 0 and 1

MAXRADIUS = 3000		# max eye radius

#######################


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
def find_eye(image):
	 
	# make a copy of the image and convert it to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# threshold the image to reveal light regions in the blurred image
	# any pixel with brightness greater than THRESH is set to white, everything else set to black
	thresh = cv2.threshold(gray, THRESH, 255, cv2.THRESH_BINARY)[1]
	#thresh = cv2.erode(thresh, None, iterations=2)
	#thresh = cv2.dilate(thresh, None, iterations=4)
	cv2.imwrite("threshold.jpg", thresh)

	# find contours
	# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	_,cnts,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	cnts_final = mask_circles(cnts)

	return cnts_final

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

###--------START HERE--------###

path = "eyes.jpg"
image = cv2.imread(path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, THRESH, 255, cv2.THRESH_BINARY)[1]


raw_path = 'eyes.cr2'
raw_image = cv2.imread(raw_path)

conts = find_eye(image)
[con_pairs, pair_det] = find_pairs(image, conts)

colours = [(255,0,0),(0,0,255),(0,255,0),(255,255,0),(255,0,255),(0,255,255),(100,200,100),(100,0,200),(200,100,200),(200,100,100)]
i=0
new = image.copy()
# circle around the pairs found in the image
for pair in con_pairs:
	i+=1
	col = colours[i%10]
	if len(pair)==2:
		for eye in pair:
			(cX, cY), radius = cv2.minEnclosingCircle(eye)
			cv2.circle(new, (int(cX), int(cY)), int(radius+8), col, 5)
	else:
		pass
# save circled image
cv2.imwrite("circled.jpg", new)

print(len(con_pairs))

for pair in con_pairs:
	for con in pair:
		print(len(con))
		coords = get_cont_pixels(con, thresh)
		print(coords)
