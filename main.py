
from raw_to_jpg import *
from detect_bright_spots import *
from circle_filter import *
from pair_eyes import *
from contours_to_pixels import *
from get_raw_colour import *
from get_jpg_colour import *
from diagnostic_tool import *
from config import *
import os


def extract_data_from(path, label):
	jpg = raw_to_jpg(path)
	cnts, thresh = detect_bright_spots(jpg)
	
	show_thresh(thresh)

	contours = circle_filter(cnts)

	show_contours(contours, jpg)

	contour_indices = pair_eyes(contours)

	if contour_indices == None:
		print("COULD NOT DETERMINE PAIRS", "\n")

	else:
		show_pairs(contours, jpg, contour_indices)
		
		print('{} ANIMAL(S) FOUND'.format(len(contour_indices)))
		
		coords_list = contours_to_pixels(contour_indices, contours, thresh, jpg)
		

		if coords_list is not None:
			# get colour from jpg or raw
			# if COLOUR_SOURCE == "JPG":
			jpg_camera = path+".JPG"
			j_colours_list = get_jpg_colour(coords_list, jpg_camera)
			# elif COLOUR_SOURCE == "RAW":
			r_colours_list = get_raw_colour(coords_list, path)
			# else:
			# 	raise ValueError("COLOUR_SOURCE must be RAW or JPG. Check config.py")
			# create result data [filename, label, r, g, b]
			j_output_list = []
			r_output_list = []
			for i in range(len(j_colours_list)):
				j_output = [path, label] + j_colours_list[i]
				j_output_list.append(j_output)
			for i in range(len(r_colours_list)):
				r_output = [path, label] + r_colours_list[i]
				r_output_list.append(r_output)
				# print(output_list)
			return r_output_list, j_output_list

		else:
			return []

# # Loop over every image in the folder
# directory_in_str = "C:\\Users\\Dan\\Documents\\GitHub\\finder-mk1\\Cow_eyes_field_test\\"
# directory = os.fsencode(directory_in_str)

# for file in os.listdir(directory):
# 	filename = os.fsdecode(file)
# 	if filename.endswith(".JPG"):
# 		path = filename[:-4]
# 		label = None
# 		print(path)
# 		extract_data_from("Cow_eyes_field_test\\" + path, label)

# # Run main on one image
# path = "images/sheep/head3_20m/IMG_6955"
# label = None
# print(extract_data_from(path, label))