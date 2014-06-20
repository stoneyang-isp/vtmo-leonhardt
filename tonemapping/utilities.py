import numpy

EPSILON = 10.0 / 65536.0


def fit_to_range(input, limits, use_percentile=False):
  new_limits = numpy.percentile(input, limits) if use_percentile else limits
  return (input - new_limits[0]) / (new_limits[1] - new_limits[0] + numpy.spacing(1))


def remove_specials(input):
  input = numpy.nan_to_num(input)
  input[input < EPSILON] = EPSILON
  return input