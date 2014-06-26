import cv2
import time
import numpy
from gt_io import ImageSequence

sequence = ImageSequence({'_file_pattern': '/Volumes/Daten/EXR/fire/%05d.exr'})

t = time.time()
cv2_image = cv2.imread('/Volumes/Daten/EXR/fire/00800.exr', cv2.CV_LOAD_IMAGE_UNCHANGED)
print time.time() - t

t = time.time()
bind_image = sequence[800]
print time.time() - t

print cv2_image.dtype
print bind_image.dtype

cv2_image = numpy.roll(cv2_image, 1, axis=2)

diff = cv2_image - bind_image
print numpy.max(numpy.abs(diff))