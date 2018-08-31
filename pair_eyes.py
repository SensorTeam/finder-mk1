import cv2
import math

#Input: A list of contours
#Output: A list of contours where pairs of eyes have been collected into a tuple
def pair_eyes(contours):
	print("Pairing the eyes...")
	
	#Initialise empty lists
	contour_list = []
	centres = []
	radii = []

	#Loop over the contours...
	for contour in contours:
		#Find the centre (x, y) and the radius of the minimum enclosing circle
		#for the contour and add them to the centres and radii lists
		(x, y), radius = cv2.minEnclosingCircle(contour)
		centres.append((x, y))
		radii.append(radius)
	
	#Compare each circle to each other circle
	for i in range(len(centres)):
		x1 = centres[i][0]
		y1 = centres[i][1]
		radius1 = radii[i]

		for j in range(i + 1, len(centres)):
			x2 = centres[j][0]
			y2 = centres[j][1]
			radius2 = radii[j]

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
			if -30 < angle < 30:
				if norm < 1 * avg_radius:
					if 0.8 < radius_ratio < (1 / 0.8):
						#If they are a pair, add them as a 2-tuple
						contour_list.append((contours[i], contours[j]))
						break
			#If the eye does not have a pair, add it as a 1-tuple
			contour_list.append((contours[i]))

	return contour_list