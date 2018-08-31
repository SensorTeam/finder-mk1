import cv2

#Input: Contour list (cnts) and thresholded image (image)
def show_contours(cnts, image)

# loop over the contours
for (i, c) in enumerate(cnts):
	# draw the bright spot on the image
	(x, y, w, h) = cv2.boundingRect(c)
	((cX, cY), radius) = cv2.minEnclosingCircle(c)
	cv2.circle(image, (int(cX), int(cY)), int(radius),
		(0, 0, 255), 3)
	cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
		cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

# show the output image
image = cv2.resize(image, (954, 634))
cv2.imshow("Image", image)
cv2.waitKey(0)

def show_thresh():
	# show the output image
	thresh = cv2.resize(thresh, (954, 634))
	cv2.imshow("Thresh", thresh)
	cv2.waitKey(0)

def circularity(contours):
# find contours of correct area
	i = 0
	for con in contours:
		i += 1
		area_contour = cv2.contourArea(con)			
		(x, y), radius = cv2.minEnclosingCircle(con)
		area_circle = math.pi * radius ** 2
		circularity = area_contour / area_circle
		print(f'#{i}:	Circularity:{circularity}')