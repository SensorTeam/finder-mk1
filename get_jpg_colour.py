import cv2

def get_jpg_colour(coords_list, path):
	print("Extracting colour information from the jpg file...")
	image = cv2.imread(path)

	colours_list = []
	r, g, b = 0, 0, 0
	num_pixels = 0, 0, 0, 0

	for coords in coords_list:
		for coord in coords:
			i = coord[0]
			j = coord[1]

			# extract from jpg
			b += image[i][j][0]
			g += image[i][j][1]
			r += image[i][j][2]
			num_pixels += 1

		r, g, b = r/num_pixels, g/num_pixels, b/num_pixels
		colours = [r, g, b]
		colours_list.append(colours)

	return colours_list