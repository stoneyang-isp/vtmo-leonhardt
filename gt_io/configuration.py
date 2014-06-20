from PyQt4 import QtCore

from PyQt4.QtCore import QObject
import msgpack

from .serializable import Serializable


class ConfigurationKlass(Serializable, QObject):

  on_filename_changed = QtCore.pyqtSignal(str)

  def __init__(self, *args, **kwargs):
    Serializable.__init__(self, *args, **kwargs)
    QObject.__init__(self)

  @property
  def filename(self):
    return self._filename

  @filename.setter
  def filename(self, value):
    if not self._filename == value:
      self._filename = value
      self.on_filename_changed.emit(value)

  def save(self, filename=None):
    if filename:
      self.filename = filename
    with open(self.filename, 'w') as f:
      msgpack.pack(self.serialize(), f)

  def open(self, filename):
    self.clear()
    with open(filename, 'r') as f:
      self.update(msgpack.unpack(f))
    self._filename = None
    self.filename = filename

  def unpack(self, arg):
    self.update(msgpack.unpackb(arg))
    return self

  def pack(self):
    return msgpack.packb(self.serialize())

  def setup(self):
    self._filename = None


class VTMOLeonhardtConfigurationKlass(ConfigurationKlass):
  def __init__(self):
    ConfigurationKlass.__init__(self)

    self.setdefault('_temporal', {})
    self.setdefault('_leonhardt_tmo', {})
    self.setdefault('_sequence', {})

  @property
  def temporal(self):
    return self._temporal

  @temporal.setter
  def temporal(self, value):
    self._temporal = value

  @property
  def leonhardt_tmo(self):
    return self._leonhardt_tmo

  @leonhardt_tmo.setter
  def leonhardt_tmo(self, value):
    self._leonhardt_tmo = value

  @property
  def sequence(self):
    return self._sequence

  @sequence.setter
  def sequence(self, value):
    self._sequence = value

Configuration = VTMOLeonhardtConfigurationKlass()