import math
import numpy
from gt_io import Configuration

from .processor import Processor
from ..utilities import remove_specials, EPSILON


class PrepareProcessor(Processor):

  def __init__(self):
    Processor.__init__(self)
    self.temporal = Configuration.temporal
    self.processing_range = Configuration.sequence.frame_range

    self.brightness = numpy.zeros(shape=(len(self.processing_range), 3))
    self.key = numpy.zeros(shape=(len(self.processing_range), 3))

  def __iter__(self):
    for index in self.processing_range:
      frame = Configuration.sequence[index]
      abs_index = self.processing_range.absolutize(index)

      for channel_index in range(frame.shape[-1]):
        channel = remove_specials(frame[..., channel_index])
        [min_lum, max_lum] = numpy.percentile(channel, [self.temporal.quantile_lower * 100.0, self.temporal.quantile_upper * 100.0])
        channel_percentiled = numpy.clip(channel, min_lum, max_lum)
        min_lum = numpy.log(min_lum)
        max_lum = numpy.log(max_lum)
        world_lum = numpy.mean(numpy.log(channel_percentiled))
        self.key[abs_index, channel_index] = (max_lum - world_lum) / (max_lum - min_lum + EPSILON)
        self.brightness[abs_index, channel_index] = math.exp((max_lum + min_lum) / (max_lum - min_lum + EPSILON))

      yield abs_index

  def after(self):
    Configuration.temporal.update({'_key': self.key, '_brightness': self.brightness})
    Configuration.temporal.is_prepared = True
    Configuration.temporal.invalidate()
