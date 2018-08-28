# run with
# `python extract_colour.py -i path-to-jpg`

import rawpy
import cv2
import numpy as np
import imutils
import math
import csv
from find_eye import *
from find_pairs import *
from contpixels import *

# ####### SET MACROS ####

THRESH = 80		# minimum brightness
CLASS = 4
# MINAREA = 10			# refine mask sizes
# MAXAREA = 30000

# MINCIRCULARITY = 0.6		# between 0 and 1

# MAXRADIUS = 3000		# max eye radius

# #######################


###--------START HERE--------###
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the normal image file")
args = vars(ap.parse_args())

# load image
path = 'eyes.jpg'
filename = args["image"]
raw_filename = args["image"][:-4]+".CR2"
image = cv2.imread(filename)

# find eyes
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, THRESH, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("thresh.jpg", thresh)
conts = find_eye(thresh)
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

# load raw image
raw_path = 'eyes.cr2'
raw_path = raw_filename

# stores final colour list
col_list = []
col_list_jpg = []

# get raw colour data for each pair
for pair in con_pairs:
	for cont in pair:
		r, g, b = 0, 0, 0
		r_num, g_num, b_num, num_pixels = 0, 0, 0, 0
		rjpg, gjpg, bjpg = 0, 0, 0
		# get coordinates of pixels inside contour boundary
		coords = get_cont_pixels(cont, thresh)
		with rawpy.imread(raw_path) as raw:
			for coord in coords:
				i = coord[0]
				j = coord[1]
				colour = raw.raw_color(i,j)		# which sensor
				value = raw.raw_value_visible(i,j)		# sensor value
				# print("coordinates: "+ str(i) +", "+ str(j))
				# print("sensor r/g/b: " + str(colour))
				# print("value: "+ str(value) + "\n")
				if colour == 0:
					r += value
					r_num += 1
				if colour == 1 or colour == 3:
					g += value
					g_num += 1
				if colour == 2:
					b += value
					b_num += 1
				bjpg += image[i][j][0]	# rgb from jpg
				gjpg += image[i][j][1]
				rjpg += image[i][j][2]
				num_pixels += 1
		rjpg, gjpg, bjpg = rjpg/num_pixels, gjpg/num_pixels, bjpg/num_pixels	# rgb from jpg
		#totjpg = rjpg + gjpg + bjpg
		#rjpg, gjpg, bjpg = rjpg/totjpg, gjpg/totjpg, bjpg/totjpg		# use r/t, g/t, b/t
		col_list_jpg.append([rjpg,gjpg,bjpg])

		r, g, b = r/r_num, g/g_num, b/b_num
		#tot = r + g + b
		#r, g, b = r/tot, g/tot, b/tot		# use r/t, g/t, b/t
		col = [r, g, b]
		col_list.append(col)


print(filename)
if len(col_list) != 0:
	print(len(col_list))
	print(col_list[0])
	print(col_list[1])
	for item in col_list_jpg:
		print(item)

	f = open("results_raw.csv", 'a')
	writer = csv.writer(f)
	writer.writerow([filename, CLASS, col_list[0][0], col_list[0][1], col_list[0][2]])
	writer.writerow([filename, CLASS, col_list[1][0], col_list[1][1], col_list[1][2]])
	f.close()

	f1 = open("results_jpg.csv", 'a')
	writer = csv.writer(f1)
	writer.writerow([filename, CLASS, col_list_jpg[0][0], col_list_jpg[0][1], col_list_jpg[0][2]])
	writer.writerow([filename, CLASS, col_list_jpg[1][0], col_list_jpg[1][1], col_list_jpg[1][2]])
	f1.close()
else:
	print("no pairs found")

