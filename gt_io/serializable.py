from UserList import UserList
from UserDict import IterableUserDict


class Serializable(IterableUserDict, object):
  def __init__(self, *args, **kwargs):
    super(Serializable, self).__init__(*args, **kwargs)

  def __getattr__(self, attribute):
    return IterableUserDict.__getitem__(self, attribute)

  def __setattr__(self, key, value):
    if key == 'data':
      super(Serializable, self).__setattr__(key, value)

    if hasattr(self.__class__, key):
      property_object = getattr(self.__class__, key)
      if isinstance(property_object, property):
        if property_object.fset is None:
          raise AttributeError
        property_object.fset(self, value)
    else:
      super(Serializable, self).__setitem__(key, value)

  def serialize(self):
    data = {}
    for key in filter(lambda k: k.startswith('_'), self.keys()):
      value = getattr(self, key)
      data[key] = value.serialize() if hasattr(value, 'serialize') else value
    return data

  def clear(self):
    IterableUserDict.clear(self)
    if hasattr(self, 'setup') and callable(getattr(self, 'setup')):
      self.setup()


class SerializableList(UserList):
  def serialize(self):
    if len(self) == 0:
      return []
    else:
      return [value.serialize() if hasattr(value, 'serialize') else value for value in self]