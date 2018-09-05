
from raw_to_jpg import *
from detect_bright_spots import *
from circle_filter import *
from pair_eyes import *
from contours_to_pixels import *
from get_raw_colour import *
from get_jpg_colour import *
from diagnostic_tool import *
from config import *


def extract_data_from(path, label):
	jpg = raw_to_jpg(path)
	cnts, thresh = detect_bright_spots(jpg)
	contours = circle_filter(cnts)

	contour_indices = pair_eyes(contours)
	
	show_thresh(thresh)
	show_contours(contours, jpg)
	
	print('{} ANIMAL(S) FOUND'.format(len(contour_indices)))
	
	coords_list = contours_to_pixels(contour_indices, contours, thresh, jpg)
	

	if coords_list is not None:
		# get colour from jpg or raw
		if COLOUR_SOURCE == "JPG":
			jpg_camera = path + ".JPG"
			colours_list = get_jpg_colour(coords_list, jpg_camera)
		elif COLOUR_SOURCE == "RAW":
			colours_list = get_raw_colour(coords_list, path)
		else:
			raise ValueError("COLOUR_SOURCE must be RAW or JPG. Check config.py")
		# create result data [filename, label, r, g, b]
		output_list = []
		for i in range(len(colours_list)):
			output = [path, label] + colours_list[i]
			output_list.append(output)
			print(output_list)
		return output_list

	else:
		return []

extract_data_from('images\\IMG_5652', None)