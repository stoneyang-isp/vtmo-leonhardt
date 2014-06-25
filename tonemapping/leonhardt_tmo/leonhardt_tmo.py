from PyQt4 import QtCore
from PyQt4.QtCore import QObject

from gt_io import Serializable


class LeonhardtTMO(Serializable, QObject):

  on_brightness_offset_changed = QtCore.pyqtSignal(float)
  on_contrast_changed = QtCore.pyqtSignal(float)
  on_gamma_changed = QtCore.pyqtSignal(float)
  on_drawback_details_changed = QtCore.pyqtSignal(bool)
  on_detail_drawback_changed = QtCore.pyqtSignal(float)
  on_detail_highlight_changed = QtCore.pyqtSignal(float)
  on_alpha_changed = QtCore.pyqtSignal(float)
  on_lambda__changed = QtCore.pyqtSignal(float)
  on_preview_changed = QtCore.pyqtSignal(bool)

  on_propery_changed = QtCore.pyqtSignal(object, str)

  def __init__(self, *args, **kwargs):
    Serializable.__init__(self, *args, **kwargs)
    QObject.__init__(self)

    self.setdefault('_preview', False)
    self.setdefault('_brightness_offset', 0.0)
    self.setdefault('_contrast', 0.0)
    self.setdefault('_gamma', 0.0)

    self.setdefault('_drawback_details', False)
    self.setdefault('_detail_drawback', 0.0)
    self.setdefault('_detail_highlight', 0.0)
    self.setdefault('_alpha', 0.0)
    self.setdefault('_lambda', 0.0)

    self.processor = None
  
  @property
  def preview(self):
    return self._preview

  @preview.setter
  def preview(self, value):
    if not self._preview == value:
      self._preview = value
      self.on_preview_changed.emit(value)
      self.invalidate('_preview')

  def set_preview(self, value):
    self.preview = value
  
  @property
  def brightness_offset(self):
    return self._brightness_offset

  @brightness_offset.setter
  def brightness_offset(self, value):
    if not self._brightness_offset == value:
      self._brightness_offset = value
      self.on_brightness_offset_changed.emit(value)
      self.invalidate('_brightness_offset')

  def set_brightness_offset(self, value):
    self.brightness_offset = value
    
  @property
  def contrast(self):
    return self._contrast

  @contrast.setter
  def contrast(self, value):
    if not self._contrast == value:
      self._contrast = value
      self.on_contrast_changed.emit(value)
      self.invalidate('_contrast')

  def set_contrast(self, value):
    self.contrast = value
    
  @property
  def gamma(self):
    return self._gamma

  @gamma.setter
  def gamma(self, value):
    if not self._gamma == value:
      self._gamma = value
      self.on_gamma_changed.emit(value)
      self.invalidate('_gamma')

  def set_gamma(self, value):
    self.gamma = value

  @property
  def drawback_details(self):
    return self._drawback_details

  @drawback_details.setter
  def drawback_details(self, value):
    if not self._drawback_details == value:
      self._drawback_details = value
      self.on_drawback_details_changed.emit(value)
      self.invalidate('_drawback_details')

  def set_drawback_details(self, value):
    self.drawback_details = value
    
  @property
  def detail_drawback(self):
    return self._detail_drawback

  @detail_drawback.setter
  def detail_drawback(self, value):
    if not self._detail_drawback == value:
      self._detail_drawback = value
      self.on_detail_drawback_changed.emit(value)
      self.invalidate('_detail_drawback')

  def set_detail_drawback(self, value):
    self.detail_drawback = value
    
  @property
  def detail_highlight(self):
    return self._detail_highlight

  @detail_highlight.setter
  def detail_highlight(self, value):
    if not self._detail_highlight == value:
      self._detail_highlight = value
      self.on_detail_highlight_changed.emit(value)
      self.invalidate('_detail_highlight')

  def set_detail_highlight(self, value):
    self.detail_highlight = value

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

  def invalidate(self, property_key):
    self.on_propery_changed.emit(self, property_key)