import math

import msgpack
import numpy

from gt_io import ImageSequence
from tonemapping.utilities import remove_specials


brightness_offset_parameter = 0.5
contrast_parameter = 1.0
gamma_parameter = 2.2
quantile_lower_parameter = 0.05
quantile_upper_parameter = 0.999
EPSILON = numpy.spacing(1.0)

frame_index = 898

if __name__ == '__main__':

  filename = "/Volumes/Daten/EXR/Untitled.vtmo"
  with open(filename, 'r') as f:
    config = msgpack.unpack(f)

  sequence = ImageSequence(config['_sequence'])
  frame = sequence[frame_index]
  abs_index = sequence.frame_range.absolutize(frame_index)

  brightness = numpy.zeros(shape=(len(sequence.frame_range), 3))
  key = numpy.zeros(shape=(len(sequence.frame_range), 3))

  for channel_index in range(frame.shape[-1]):
    channel = remove_specials(frame[..., channel_index])
    [min_lum, max_lum] = numpy.percentile(channel, [quantile_lower_parameter * 100.0, quantile_upper_parameter * 100.0])
    channel_percentiled = numpy.clip(channel, min_lum, max_lum)
    min_lum = numpy.log(min_lum)
    max_lum = numpy.log(max_lum)
    world_lum = numpy.mean(numpy.log(channel_percentiled))
    key[abs_index, channel_index] = (max_lum - world_lum) / (max_lum - min_lum + EPSILON)
    brightness[abs_index, channel_index] = math.exp((max_lum + min_lum) / (max_lum - min_lum + EPSILON))

  contrast = numpy.zeros(key.shape)

  for i in range(key.shape[1]):
    # brightness[..., i] = wlsfilter(brightness[..., i], 1.2, 1.0)
    contrast[..., i] = (1 - contrast_parameter) + (contrast_parameter * key[..., i])

  hdr = sequence[frame_index]
  hdr = remove_specials(hdr)

  hdr_coarse = hdr.copy()

  transfered = numpy.zeros(hdr.shape)

  hdr_mean = numpy.mean(hdr, axis=2)

  for channel_index in range(hdr.shape[2]):
    brightness_map = brightness[abs_index, channel_index] + hdr_mean
    ia = hdr_coarse[..., channel_index] / brightness_map
    ib = (hdr_coarse[..., channel_index] + brightness_map) * (brightness_map * 0.5 * (numpy.exp(ia) - numpy.exp(-ia)))
    transfered[..., channel_index] = numpy.exp(-brightness_offset_parameter) * remove_specials(ib) ** contrast[
      abs_index, channel_index]

  ldr = hdr ** gamma_parameter / (hdr_coarse ** gamma_parameter + transfered)