import os


def build_pattern_from_path(path):
  file_name, file_extension = os.path.splitext(path)
  file_dir = os.path.dirname(file_name)
  file_name = os.path.basename(file_name)

  return os.path.join(file_dir, "%" + "%02d" % len(file_name) + "d" + file_extension)


def deep_dict_key_sanitation(d):
  new = {}
  for k, v in d.iteritems():
    if isinstance(v, dict):
      v = deep_dict_key_sanitation(v)
    while k.startswith('_'):
      k = k[1:]
    new[k] = v
  return new


class FrameRange():
  def __init__(self, lower_limit, upper_limit):
    self._lower_limit = lower_limit
    self._upper_limit = upper_limit
    self._invalidate()

  @property
  def lower_limit(self):
    return self._lower_limit

  @lower_limit.setter
  def lower_limit(self, value):
    self._lower_limit = value
    self._invalidate()

  @property
  def upper_limit(self):
    return self._upper_limit

  @upper_limit.setter
  def upper_limit(self, value):
    self._upper_limit = value
    self._invalidate()

  @property
  def range(self):
    return [self.lower_limit, self.upper_limit]

  @range.setter
  def range(self, value):
    self.lower_limit, self.upper_limit = value

  def __len__(self):
    return len(self._iterator)

  def __iter__(self):
    return iter(self._iterator)

  def _invalidate(self):
    self._iterator = xrange(self.lower_limit, self.upper_limit + 1)

  def serialize(self):
    return self.range

  def absolutize(self, index):
    return index - self.lower_limit