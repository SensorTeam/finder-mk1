import rawpy
import imageio
from config import *

#Takes in the path of a RAW file, postprocesses the RAW file into a JPG
#and returns the JPG.
def raw_to_jpg(path):
	print("Converting raw image to jpg...")
	with rawpy.imread(path + '.CR2') as raw:
		#Parameters can be added to postprocess() to change brightness
		#and gamma correction
		jpg = raw.postprocess(bright = 0.1)
		imageio.imwrite(path + '_pp.jpg', jpg)
		return jpg
