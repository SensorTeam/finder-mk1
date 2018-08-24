import rawpy
import imageio

path = 'eyes.cr2'
with rawpy.imread(path) as raw:
	jpg = raw.postprocess(bright=1)
imageio.imwrite('eyes.jpg', jpg)