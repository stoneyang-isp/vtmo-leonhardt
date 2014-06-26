import numpy
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve

from tonemapping.utilities import EPSILON


def wlsfilter(image, lambda_, alpha):
  s = image.shape
  k = numpy.prod(s)

  dy = numpy.diff(image, 1, 0)
  dy = -lambda_ / (numpy.absolute(dy) ** alpha + EPSILON)
  if dy.ndim > 1:
    dy = numpy.vstack((dy, numpy.zeros(s[1], )))
  else:
    dy = numpy.append(dy, [0])
  dy = dy.flatten(1)

  if image.ndim > 1:
    dx = numpy.diff(image, 1, 1)
    dx = -lambda_ / (numpy.absolute(dx) ** alpha + EPSILON)
    dx = numpy.hstack((dx, numpy.zeros(s[0], )[:, numpy.newaxis]))
    dx = dx.flatten(1)
  else:
    dx = numpy.zeros(s[0], )

  a = spdiags(numpy.vstack((dx, dy)), [-s[0], -1], k, k)
  d = 1 - (dx + numpy.roll(dx, s[0]) + dy + numpy.roll(dy, 1))
  a = a + a.T + spdiags(d, 0, k, k)

  output = spsolve(a, image.flatten(1))

  if image.ndim > 1:
    output = numpy.rollaxis(output.reshape(s[::-1]), 1)

  return output