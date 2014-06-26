import numpy
from gt_io import Configuration
from tonemapping.leonhardt_tmo import wlsfilter

if __name__ == "__main__":
  Configuration.open('/Volumes/Daten/EXR/Untitled.vtmo')

  brightness = numpy.array(Configuration['_temporal']['_brightness'])

  for i in range(brightness.shape[1]):
    brightness[:, i] = wlsfilter(brightness[:, i], 1.0, 1.2)

  # print wlsfilter(numpy.array([1 ,2, 3]), 1.0, 1.2)
