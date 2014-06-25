import cv2
import numpy


def TransformedDomainRecursiveFilter_Horizontal(input, D, sigma):
  a = numpy.exp(-numpy.sqrt(2) / sigma)

  output = input
  V = a ** D
  s = input.shape

  for i in range(1, s[1]):
    for c in range(s[2]):
      output[:, i, c] = output[:, i, c] + V[:, i] * (output[:, i - 1, c] - output[:, i, c])

  for i in range(s[1], 0):
    for c in range(s[2]):
      output[:, i, c] = output[:, i, c] + V[:, i + 1] * (output[:, i + 1, c] - output[:, i, c])

  return output


def image_transpose(input):
  s = input.shape
  output = numpy.zeros((s[1], s[0], s[2]))

  for c in range(s[2]):
    output[..., c] = input[..., c].T

  return output


def rf(image, sigma_s, sigma_r, num_iterations=3):
  s = image.shape

  dIcdx = numpy.diff(image, 1, 1)
  dIcdy = numpy.diff(image, 1, 0)

  dIdx = numpy.zeros((s[0], s[1]))
  dIdy = numpy.zeros((s[0], s[1]))

  for c in range(s[2]):
    dIdx[:, 1:] = dIdx[:, 1:] + numpy.abs(dIcdx[..., c])
    dIdy[1:, :] = dIdy[1:, :] + numpy.abs(dIcdy[..., c])

  dHdx = (1 + sigma_s / sigma_r * dIdx)
  dVdy = (1 + sigma_s / sigma_r * dIdy).T

  n = num_iterations
  f = image

  sigma_H = sigma_s

  for i in range(num_iterations):
    sigma_H_i = sigma_H * numpy.sqrt(3) * 2 ** (n - (i + 1)) / numpy.sqrt(4 ** n - 1)
    f = TransformedDomainRecursiveFilter_Horizontal(f, dHdx, sigma_H_i)
    f = image_transpose(f)
    f = TransformedDomainRecursiveFilter_Horizontal(f, dVdy, sigma_H_i)
    f = image_transpose(f)

  return f


if __name__ == "__main__":

  image = cv2.imread('/Users/manuelleonhardt/Desktop/sample.png', cv2.CV_LOAD_IMAGE_UNCHANGED).astype(numpy.float)
  image = numpy.dstack((image, image, image)) / 255.0

  print rf(image, 1.0, 1.0)