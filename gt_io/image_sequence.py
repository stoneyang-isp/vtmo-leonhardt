from PyQt4 import QtCore
import os
import glob
from OpenEXR import InputFile
from PyQt4.QtCore import QObject

import numpy
from obsub import event
import Imath

from .utilities import FrameRange
from .serializable import Serializable


class ImageSequence(Serializable, QObject):

  on_exposure_offset_changed = QtCore.pyqtSignal(float)
  on_index_changed = QtCore.pyqtSignal(int)

  def __init__(self, *args, **kwargs):
    Serializable.__init__(self, *args, **kwargs)
    QObject.__init__(self)

    # Internals
    self.cache_index = self._current_absolute_index = self.__index = self.width = self.height = -1
    self.cache = self.shape = None

    # Facts
    files = glob.glob(os.path.join(os.path.dirname(self.file_pattern), "*" + os.path.splitext(self.file_pattern)[1]))
    self.frame_range = FrameRange(int(os.path.splitext(os.path.basename(files[0]))[0]),
                                  int(os.path.splitext(os.path.basename(files[-1]))[0]))

    # Defaults
    self.setdefault('_file_pattern', None)
    self.setdefault('_frame_range_window', self.frame_range.range)
    self.setdefault('_exposure_offset', 0.0)

    self.frame_range_window = FrameRange(*self.frame_range_window)
    self.setup()

  @property
  def exposure_offset(self):
    return self._exposure_offset

  @exposure_offset.setter
  def exposure_offset(self, value):
    if not self._exposure_offset == value:
      self._exposure_offset = value
      self.on_exposure_offset_changed.emit(value)

  def set_exposure_offset(self, value):
    self.exposure_offset = value

  @property
  def index(self):
    return self.__index

  @index.setter
  def index(self, value):
    if not self.__index == value:
      self.__index = value
      self.on_index_changed.emit(value)

  def set_index(self, value):
    self.index = value

  @property
  def frame_range_window(self):
    return self._frame_range_window

  @frame_range_window.setter
  def frame_range_window(self, value):
    if not self._frame_range_window == value:
      self._frame_range_window = value

  @property
  def file_pattern(self):
    return self._file_pattern

  @file_pattern.setter
  def file_pattern(self, value):
    if not self._file_pattern == value:
      self._file_pattern = value

  def __len__(self):
    return len(self.frame_range)

  def __getitem__(self, index):

    if isinstance(index, str):
      return super(ImageSequence, self).__getitem__(index)

    if index == self.cache_index:
      return self.cache * numpy.exp(self.exposure_offset)

    if not isinstance(index, int) and index in self.frame_range:
      raise IndexError

    exrfile = InputFile(self.file_pattern % index)

    channels = ('R', 'G', 'B')

    output = numpy.ndarray(dtype=numpy.float, shape=(self.height, self.width, channels.__len__()))

    for channel_index, channel in enumerate(channels):
      output[:, :, channel_index] = numpy.fromstring(exrfile.channel(channel, Imath.PixelType(Imath.PixelType.HALF)), dtype=numpy.float16).astype(numpy.float).reshape([self.height, self.width])

    self.cache = output
    self.cache_index = index

    return output * numpy.exp(self.exposure_offset)

  def setup(self):
    sample = InputFile(self.file_pattern % self.frame_range.lower_limit)
    dw = sample.header()['dataWindow']
    (self.width, self.height) = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    self.shape = (self.height, self.width, len(sample.header()['channels']))