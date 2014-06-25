from copy import deepcopy


def dict_deep_merge(a, b):
  if not isinstance(b, dict):
    return b
  result = deepcopy(a)
  for k, v in b.iteritems():
    if k in result and isinstance(result[k], dict):
      result[k] = dict_deep_merge(result[k], v)
    else:
      result[k] = deepcopy(v)
  return result