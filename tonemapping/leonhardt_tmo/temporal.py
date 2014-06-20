from PyQt4 import QtCore
from PyQt4.QtCore import QObject
import numpy

from gt_io import Serializable


class Temporal(Serializable, QObject):

  on_quantile_lower_changed = QtCore.pyqtSignal(float)
  on_quantile_upper_changed = QtCore.pyqtSignal(float)
  on_alpha_changed = QtCore.pyqtSignal(float)
  on_lambda__changed = QtCore.pyqtSignal(float)

  on_propery_changed = QtCore.pyqtSignal(object, str)

  def __init__(self, *args, **kwargs):
    Serializable.__init__(self, *args, **kwargs)
    QObject.__init__(self)

    self.setdefault('_quantile_lower', 0.0)
    self.setdefault('_quantile_upper', 1.0)
    self.setdefault('_alpha', 0.0)
    self.setdefault('_lambda', 0.0)
    self.setdefault('_key', [])
    self.setdefault('_brightness', [])
    self.setdefault('_is_prepared', False)

    self._brightness = numpy.array(self._brightness)
    self._key = numpy.array(self._key)

  @property
  def quantile_lower(self):
    return self._quantile_lower

  @quantile_lower.setter
  def quantile_lower(self, value):
    if not self._quantile_lower == value:
      self._quantile_lower = value
      self.on_quantile_lower_changed.emit(value)

  def set_quantile_lower(self, value):
    self.quantile_lower = value

  @property
  def quantile_upper(self):
    return self._quantile_upper

  @quantile_upper.setter
  def quantile_upper(self, value):
    if not self._quantile_upper == value:
      self._quantile_upper = value
      self.on_quantile_upper_changed.emit(value)

  def set_quantile_upper(self, value):
    self.quantile_upper = value

  @property
  def alpha(self):
    return self._alpha

  @alpha.setter
  def alpha(self, value):
    if not self._alpha == value:
      self._alpha = value
      self.on_alpha_changed.emit(value)
      self.invalidate('_alpha')

  def set_alpha(self, value):
    self.alpha = value

  @property
  def lambda_(self):
    return self._lambda

  @lambda_.setter
  def lambda_(self, value):
    if not self._lambda == value:
      self._lambda = value
      self.on_lambda__changed.emit(value)
      self.invalidate('_lambda')

  def set_lambda_(self, value):
    self.lambda_ = value
      
  @property
  def key(self):
    return self._key

  @key.setter
  def key(self, value):
    self._key = value
    self.invalidate('_key')

  def set_key(self, value):
    self.key = value

  @property
  def brightness(self):
    return self._brightness

  @brightness.setter
  def brightness(self, value):
    self._brightness = value
    self.invalidate('_brightness')

  def set_brightness(self, value):
    self.brightness = value

  @property
  def is_prepared(self):
    return self._is_prepared

  @is_prepared.setter
  def is_prepared(self, value):
    if not self._is_prepared == value:
      self._is_prepared = value
      self.invalidate('_is_prepared')

  def invalidate(self, property_key=''):
    self.on_propery_changed.emit(self, property_key)

  def serialize(self):
    result = Serializable.serialize(self)
    result.update({
      '_key': result['_key'].tolist(),
      '_brightness': result['_brightness'].tolist()
    })
    return result