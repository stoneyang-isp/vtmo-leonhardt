from PyQt4 import QtCore
from PyQt4.QtCore import QObject
import numpy
from pyqtgraph.graphicsItems.ImageItem import ImageItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox

from gt_io import Configuration
from tonemapping.utilities import remove_specials


class Viewer(ViewBox, QObject):
  on_exposure_changed = QtCore.pyqtSignal(float)

  def __init__(self):
    super(Viewer, self).__init__()
    self.setAspectLocked(True)
    self.invertY(True)
    self._exposure = 0.0

  @property
  def exposure(self):
    return self._exposure

  @exposure.setter
  def exposure(self, value):
    if not self._exposure == value:
      self._exposure = value
      self.on_exposure_changed.emit(value)
      self.invalidate()

  def set_exposure(self, value):
    self.exposure = value

  def invalidate(self, *args):
    self.invalidate_by_index(Configuration.sequence.index)

  def invalidate_by_index(self, index):
    if Configuration.leonhardt_tmo.preview:
      image = Configuration.leonhardt_tmo.processor[index]
    else:
      image = Configuration.sequence[index]

    image = remove_specials(numpy.rollaxis(image, 1) * numpy.exp(self.exposure))

    # Linear to sRGB
    image = numpy.where(image <= 0.0031308,
                        image * 12.92,
                        1.055 * numpy.power(image, 1.0 / 2.4) - 0.055)

    self.image_item.setImage(image, levels=[0, 1])

  def clear(self):
    ViewBox.clear(self)
    self.image_item = ImageItem()
    self.addItem(self.image_item)