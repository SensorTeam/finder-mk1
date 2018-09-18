# run in terminal using:
# for f in path/to/folder/*.JPG; do python3 collectdata.py -i $f -l label; done

import argparse
import csv
from main import *

# take path as argument (w/o file extension)
# take label as argument
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the normal image file")
ap.add_argument("-l", "--label", help = "path to the normal image file")
args = vars(ap.parse_args())

# load the image
path = args["image"][:-4]
label = args["label"]

r_results, j_results = extract_data_from(path, label)
print(r_results)
print(j_results)

f = open("sheep_data_raw.csv", 'a')
writer = csv.writer(f)
for entry in r_results:
	writer.writerow(entry)
f.close()

f2 = open("sheep_data_jpg.csv", 'a')
writer = csv.writer(f2)
for entry in j_results:
	writer.writerow(entry)
f2.close()

f1 = open("txt.csv", 'a')
writer = csv.writer(f1)
for entry in r_results:
	writer.writerow([len(r_results), path])
f1.close()

f3 = open("txt2.csv", 'a')
writer = csv.writer(f3)
for entry in j_results:
	writer.writerow([len(j_results), path])
f3.close()
