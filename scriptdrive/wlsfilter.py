import cv2
import numpy
from numpy.linalg import linalg
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve
from gt_io import ImageSequence

small_eps = 0.0001

def wlsfilter(image, lambda_, alpha):
  s = image.shape

  k = numpy.prod(s)

  dy = numpy.diff(image, 1, 0)
  dy = -lambda_ / (numpy.absolute(dy) ** alpha + small_eps)
  dy = numpy.vstack((dy, numpy.zeros(s[1], )))
  dy = dy.flatten(1)

  dx = numpy.diff(image, 1, 1)
  dx = -lambda_ / (numpy.absolute(dx) ** alpha + small_eps)
  dx = numpy.hstack((dx, numpy.zeros(s[0], )[:, numpy.newaxis]))
  dx = dx.flatten(1)

  a = spdiags(numpy.vstack((dx, dy)), [-s[0], -1], k, k)

  d = 1 - (dx + numpy.roll(dx, s[0]) + dy + numpy.roll(dy, 1))
  a = a + a.T + spdiags(d, 0, k, k)

  return spsolve(a, image.flatten(1)).reshape(s[::-1])


if __name__ == "__main__":
  lambda_ = 1.0
  alpha = 1.2

  # image = cv2.imread('/Users/manuelleonhardt/Desktop/sample.png', cv2.CV_LOAD_IMAGE_UNCHANGED).astype(numpy.float)
  # image = numpy.tile(image, (2, 1))
  #
  # output = wlsfilter(image, lambda_, alpha) / 255.0

  sequence = ImageSequence({'_file_pattern': '/Volumes/Daten/EXR/fire/%05d.exr'})
  image = sequence[866].astype(numpy.float)
  image = image[..., 0]

  output = wlsfilter(image, lambda_, alpha)

  #
  # output = numpy.zeros((s[1], s[0], s[2]))
  #
  # for channel_index in range(image.shape[2]):
  #   output[..., channel_index] = wlsfilter(image[..., channel_index], lambda_, alpha)
  #
  cv2.imshow('', numpy.rollaxis(output, 1))
  cv2.waitKey()


# t = time.time()
# output = linalg.lstsq(A.todense(), image.flatten(1))[0].reshape(s)
# print time.time() - t
# # print output

# t = time.time()
# output = lsqr(A, image.flatten(1))[0].reshape(s)
# print time.time() - t
# print output

# output = spsolve(A, image.flatten(1)).reshape(s)