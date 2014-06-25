from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QSlider


class QDoubleSlider(QSlider):

  valueChanged = pyqtSignal(float)

  def __init__(self, parent=None):
    QSlider.__init__(self, parent)
    self.resolution = 1000

    super(QDoubleSlider, self).valueChanged.connect(self.__set_value)

  def convert(self, value):
    return int(value * self.resolution)

  def convert_back(self, value):
    return float(value) / self.resolution

  def value(self):
    return self.convert_back(QSlider.value(self))

  def maximum(self):
    return self.convert_back(QSlider.maximum(self))

  def minimum(self):
    return self.convert_back(QSlider.minimum(self))

  def setValue(self, value):
    QSlider.setValue(self, self.convert(value))

  def __set_value(self, value):
    if not self.value() == value:
      self.valueChanged.emit(self.value())

  def setMaximum(self, value):
    QSlider.setMaximum(self, self.convert(value))

  def setMinimum(self, value):
    QSlider.setMinimum(self, self.convert(value))

  def setRange(self, value_lower, value_upper):
    QSlider.setRange(self, self.convert(value_lower), self.convert(value_upper))