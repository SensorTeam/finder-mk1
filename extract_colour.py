# Run with
# `python extract_colour.py -i path-to-jpg`
# Output: appends data to two .csv files, results_jpg.csv and results_raw.csv
# Appended info is [filename, label (None if unknown), R, G, B]

import rawpy
import cv2
import numpy as np
import imutils
import math
import csv
from find_eye import *
from find_pairs import *
from contpixels import *

# ####### SET MACROS #######

THRESH = 80		# minimum brightness

# # SET THE FOLLOWING IN FIND_EYES.PY
# MINAREA = 10			# refine mask sizes
# MAXAREA = 30000

# MINCIRCULARITY = 0.6		# between 0 and 1

# MAXRADIUS = 3000		# max eye radius

# ##########################

def extract_colour(filename, label):
	# load image
	raw_filename = filename[:-4]+".CR2"
	image = cv2.imread(filename)

	# find eyes
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, THRESH, 255, cv2.THRESH_BINARY)[1]
	cv2.imwrite("thresh.jpg", thresh)
	conts = find_eye(thresh)
	[con_pairs, pair_det] = find_pairs(image, conts)

	colours = [(255,0,0),(0,0,255),(0,255,0),(255,255,0),(255,0,255),(0,255,255)]
	new = image.copy()
	i=0
	# circle around the pairs found in the image
	for pair in con_pairs:
		i+=1
		col = colours[i%6]
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
				# for each pixel in the contour
				for coord in coords:
					i = coord[0]
					j = coord[1]
					# extract from raw file
					colour = raw.raw_color(i,j)		# which sensor
					value = raw.raw_value_visible(i,j)		# sensor value
					if colour == 0:
						r += value
						r_num += 1
					if colour == 1 or colour == 3:
						g += value
						g_num += 1
					if colour == 2:
						b += value
						b_num += 1
					# extract from jpg
					bjpg += image[i][j][0]
					gjpg += image[i][j][1]
					rjpg += image[i][j][2]
					num_pixels += 1

			# calculate final values for jpg
			rjpg, gjpg, bjpg = rjpg/num_pixels, gjpg/num_pixels, bjpg/num_pixels	# rgb from jpg
			# totjpg = rjpg + gjpg + bjpg	# use r/t, g/t, b/t
			# rjpg, gjpg, bjpg = rjpg/totjpg, gjpg/totjpg, bjpg/totjpg		
			col_list_jpg.append([rjpg,gjpg,bjpg])

			# calculate final values for raw
			r, g, b = r/r_num, g/g_num, b/b_num
			# tot = r + g + b
			# r, g, b = r/tot, g/tot, b/tot		# use r/t, g/t, b/t
			col = [r, g, b]
			col_list.append(col)

	print("Searched " + filename[:-4])
	if len(col_list) != 0:
		print("%s pairs found"%len(con_pairs))

		f = open("results_raw.csv", 'a')
		writer = csv.writer(f)
		raw_eye1 = [filename, label, col_list[0][0], col_list[0][1], col_list[0][2]]
		raw_eye2 = [filename, label, col_list[1][0], col_list[1][1], col_list[1][2]]
		writer.writerow(raw_eye1)		# left eye
		writer.writerow(raw_eye2)		# right eye
		f.close()

		f1 = open("results_jpg.csv", 'a')
		writer = csv.writer(f1)
		jpg_eye1 = [filename, label, col_list_jpg[0][0], col_list_jpg[0][1], col_list_jpg[0][2]]
		jpg_eye2 = [filename, label, col_list_jpg[1][0], col_list_jpg[1][1], col_list_jpg[1][2]]
		writer.writerow(jpg_eye1)
		writer.writerow(jpg_eye2)
		f1.close()
	else:
		print("No pairs found")
	return([raw_eye1, raw_eye2], [jpg_eye1, jpg_eye2])
