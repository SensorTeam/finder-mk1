import rawpy
from config import *

def get_raw_colour(coords_list, path):
	print("Extracting colour information from the raw file...")
	colours_list = []
	r, g, b = 0, 0, 0
	r_num, g_num, b_num, num_pixels = 0, 0, 0, 0

	with rawpy.imread(path + '.cr2') as raw:
		for coords in coords_list:
			for coord in coords:
				i = coord[0]
				j = coord[1]

				colour = raw.raw_color(i,j)
				value = raw.raw_value_visible(i,j)
				if colour == 0:
					r += value
					r_num += 1
				if colour == 1 or colour == 3:
					g += value
					g_num += 1
				if colour == 2:
					b += value
					b_num += 1

			r, g, b = r / r_num, g / g_num, b / b_num

			colours = [r, g, b]
			colours_list.append(colours)

	return colours_list