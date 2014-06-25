import string
from PyQt4 import QtGui


def set_ui_from_config(ui, config):
  for key, value in config.items():
    if isinstance(value, bool):
      #ui element is a checkbox
      getattr(ui, key + '_checkbox').setChecked(value)
    elif isinstance(value, int) or isinstance(value, float):
      #ui element is a spinbox
      getattr(ui, key + '_spinbox').setValue(value)


def get_config_from_ui(ui, elements):
  result = {}
  for element in elements:
    temp_element = getattr(ui, element)
    if isinstance(temp_element, QtGui.QCheckBox):
      temp_value = temp_element.isChecked()
    elif isinstance(temp_element, QtGui.QSpinBox):
      temp_value = temp_element.value()
    else:
      temp_value = None

    result[element[0:string.rfind(element, "_")]] = temp_value

  return result


def bind_to_value(widgets, property_holder, property_key):

  property_event = getattr(property_holder, "on_" + property_key + "_changed")
  property_setter = getattr(property_holder, "set_" + property_key)
  property_value = getattr(property_holder, property_key)

  for widget in widgets:
    if hasattr(widget, 'valueChanged'):
      widget.setValue(property_value)
      widget.valueChanged.connect(property_setter)
      property_event.connect(widget.setValue)
    elif hasattr(widget, 'stateChanged'):
      widget.setChecked(property_value)
      widget.stateChanged.connect(property_setter)
      property_event.connect(widget.setChecked)