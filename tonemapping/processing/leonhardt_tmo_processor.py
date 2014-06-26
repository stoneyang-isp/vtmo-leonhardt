import os

import numpy

from gt_io import Configuration
from .processor import Processor
from tonemapping.leonhardt_tmo import wlsfilter
from ..utilities import remove_specials, EPSILON


class LeonhardtTMOProcessor(Processor):

  def __init__(self, filename=""):
    Processor.__init__(self)

    self.filename = filename
    self.tmo = Configuration.leonhardt_tmo
    self.temporal = Configuration.temporal

    self.temporal.on_propery_changed.connect(self.invalidate_temporal)
    self.tmo.on_contrast_changed.connect(self.invalidate_temporal)

    self.processing_range = Configuration.sequence.frame_range_window

    self.invalidate_temporal()

  def invalidate_temporal(self):
    if self.temporal.is_prepared:
      self.contrast = numpy.zeros(self.temporal.key.shape)
      self.brightness = numpy.zeros(self.temporal.brightness.shape)

      for i in range(self.temporal.key.shape[1]):
        self.brightness[:, i] = wlsfilter(self.temporal.brightness[:, i], self.temporal.lambda_, self.temporal.alpha)
        self.contrast[:, i] = (1 - self.tmo.contrast) + wlsfilter(self.tmo.contrast * self.temporal.key[:, i], self.temporal.lambda_, self.temporal.alpha)

  def __getitem__(self, index):
    abs_index = Configuration.sequence.frame_range.absolutize(index)

    hdr = Configuration.sequence[index]
    hdr = remove_specials(hdr)

    if self.tmo.drawback_details:
      hdr_coarse = numpy.log(hdr + EPSILON)
      for i in range(hdr_coarse.shape[2]):
        hdr_coarse[..., i] = wlsfilter(hdr_coarse[..., i], self.tmo.lambda_, self.tmo.alpha)
      hdr_coarse = (hdr * (1 - self.tmo.detail_drawback) + (numpy.exp(hdr_coarse) - EPSILON) * self.tmo.detail_drawback)
      hdr = hdr * numpy.exp((hdr - hdr_coarse) * self.tmo.detail_highlight)
    else:
      hdr_coarse = hdr

    transfered = numpy.zeros(hdr.shape)
    hdr_mean = numpy.mean(hdr, axis=2)

    for channel_index in range(hdr.shape[2]):
      brightness_map = self.brightness[abs_index, channel_index] + hdr_mean
      ia = hdr_coarse[..., channel_index] / brightness_map
      ib = (hdr_coarse[..., channel_index] + brightness_map) * (brightness_map * numpy.sinh(ia))
      transfered[..., channel_index] = numpy.exp(-self.tmo.brightness_offset) * remove_specials(ib) ** self.contrast[abs_index, channel_index]

    ldr = hdr ** self.tmo.gamma / (hdr_coarse ** self.tmo.gamma + transfered)
    # ldr **= (1.0 / (self.tmo.gamma + numpy.spacing(0.0)))

    return ldr

  def __iter__(self):
    self.invalidate_temporal()
    filename = os.path.join(self.filename, '%08d.exr')
    
    for index in self.processing_range:
      Configuration.sequence.write(filename % index, self[index])
      yield self.processing_range.absolutize(index)