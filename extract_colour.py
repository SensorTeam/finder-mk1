import rawpy
import cv2
import numpy as np
import imutils
import math
from find_eye import *
from find_pairs import *
from contpixels import *

# ####### SET MACROS ####

THRESH = 70		# minimum brightness

# MINAREA = 10			# refine mask sizes
# MAXAREA = 30000

# MINCIRCULARITY = 0.6		# between 0 and 1

# MAXRADIUS = 3000		# max eye radius

# #######################


###--------START HERE--------###

# load image
path = 'eyes.jpg'
image = cv2.imread(path)
# find eyes
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, THRESH, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("thresh.jpg", thresh)
conts = find_eye(thresh)
[con_pairs, pair_det] = find_pairs(image, conts)
# load raw image
raw_path = 'eyes.cr2'
r, g, b = 0, 0, 0
r_num, g_num, b_num = 0, 0, 0
col_list = []
# get raw colour data for each pair
for pair in con_pairs:
	for cont in pair:
		# get coordinates of pixels inside contour boundary
		coords = get_cont_pixels(cont, thresh)
		with rawpy.imread(raw_path) as raw:
			for coord in coords:
				i = coord[0]
				j = coord[1]
				colour = raw.raw_color(i,j)		# which sensor
				value = raw.raw_value(i,j)		# sensor value
				print(i,j)
				print('colour = ' + str(colour))
				print('val = ' +str(value))
				if colour == 0:
					r += value
					r_num += 1
				if colour == 1 or colour == 3:
					g += value
					g_num += 1
				if colour == 2:
					b += value
					b_num += 1
		r, g, b = r/r_num, g/g_num, b/b_num
		tot = r + g + b
		r, g, b = r/tot, g/tot, b/tot		# use r/t, g/t, b/t
		col = [r, g, b]
		col_list.append(col)
print(col_list)
		