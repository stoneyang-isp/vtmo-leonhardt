import numpy
from tonemapping.leonhardt_tmo import wlsfilter

if __name__ == "__main__":
  wlsfilter(numpy.random.rand(200,200), 1.0, 1.2)

  # def test(func, *args, **kwargs):
#   t = time.time()
#   func(*args, **kwargs)
#   print func.__name__ + " " + str((t - time.time()))