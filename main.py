from raw_to_jpg import *
from detect_bright_spots import *
from circle_filter import *
from pair_eyes import *
from contours_to_pixels import *
from get_raw_colour import *
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
		colours_list = get_raw_colour(coords_list, path)
		output_list = []
		for i in range(len(colours_list)):
			output = [path, label] + colours_list[i]
			output_list.append(output)
			print(output_list)
		return output_list
	else:
		return []

extract_data_from('IMG_5652', None)