import os
import cv2
from extract_colour import *
import sys
sys.path.append('../knn3d')
from classify import *


realtime = True
path = "../scanner/data/"
LABEL = 0
MAX = 100


i = 0
while True:
	dirs = os.listdir( path )
	for file in dirs:
		image_path = path + "file"+str(i)+".JPG"
		if file == "file"+str(i)+".JPG":
			print("==========================\nProcessing " + file)
			if i > (MAX - 1):
				j = i - MAX
				os.remove( path + "file" + str( j ) + ".JPG" )
			i += 1
			# wait until file is written
			while cv2.imread(image_path) is None:
				g=0
			# execute main for new image
			result_raw, result_jpg = extract_colour(image_path,LABEL)
			result_raw, result_jpg = np.asarray(result_raw), np.asarray(result_jpg)
			if realtime:
				print("Classifying...")
				for data in result_raw:		# or result_jpg
					classify(data)
			else:
				print("Successfully added to database")


