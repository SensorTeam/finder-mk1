import cv2
import math
from config import *

#Input: A list of contours
#Output: A list of contours where pairs of eyes have been collected into a tuple
def pair_eyes(contours):
	print("Pairing the eyes...")
	
	#Initialise empty lists
	contour_indices = []
	centres = []
	radii = []

	#Loop over the contours...
	for contour in contours:
		#Find the centre (x, y) and the radius of the minimum enclosing circle
		#for the contour and add them to the centres and radii lists
		(x, y), radius = cv2.minEnclosingCircle(contour)
		centres.append((x, y))
		radii.append(radius)
	
	# If there is only one signal, add it by itself
	if len(centres) == 1:
		contour_indices.append((0, None))

	else:

		#Compare each circle to each other circle
		for i in range(len(centres)):
			x1 = centres[i][0]
			y1 = centres[i][1]
			radius1 = radii[i]

			for j in range(i + 1, len(centres)):
				x2 = centres[j][0]
				y2 = centres[j][1]
				radius2 = radii[j]

				I = cv2.matchShapes(contours[i], contours[j], 1, 0)
				print(i,j)
				print(I)
				#Find the distance between the circles' centres,
				#the angle of elavation/depression,
				#the averaged radius of the two circles,
				# and the ratio of the circles' radii
				norm = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
				angle = math.degrees(math.atan((y2 - y1) / (x2 - x1)))
				avg_radius = (radius1 + radius2) / 2
				radius_ratio = radius2 / radius1

				#To be considered a pair of eyes, the magnitude of the angle of elavation/depression
				#must be less than 30 degrees, the distance between circles must not exceed 10 times 
				#the circles averaged radius, and the ratio of radii must be less than 0.8
				if -MAX_ANGLE < angle < MAX_ANGLE:
					if norm < AVG_RADIUS_MULTIPLIER * avg_radius:
						# if MIN_RADIUS_RATIO < radius_ratio < (1 / MIN_RADIUS_RATIO):
						if I < HU_MOMENT_DISTANCE:
							#If they are a pair, add them as a 2-tuple
							contour_indices.append((i, j))
							
						else:
							#If the eye does not have a pair, add a 2-tuple with the eye and 'None'
							contour_indices.append((i, None))

	# constuct new list to check doubling up of pairing
	print(contour_indices)
	index_list = []
	for pair in contour_indices:
		for index in pair:
			index_list.append(index)
			if len(set(index_list)) != len(index_list):
				return None

	return contour_indices