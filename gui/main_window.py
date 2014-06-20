import os
import functools

from PyQt4 import QtGui

from .processing import ProcessorDialog
from tonemapping import Temporal, LeonhardtTMO
from tonemapping.processing.leonhardt_tmo_processor import LeonhardtTMOProcessor
from .widgets import Viewer
from tonemapping.processing import PrepareProcessor
from .main_window_view import Ui_MainWindow
from gt_io import \
  Configuration, \
  ImageSequence, \
  build_pattern_from_path, \
  QFILEDIALOG_IMAGE_SEQUENCE_FILTER, \
  QFILEDIALOG_CONFIGURATION_FILTER, \
  QFILEDIALOG_MATLAB_FILTER
from .utilities import bind_to_value


class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)

    # GUI
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # GUI Controller
    self.view = Viewer()
    self.ui.graphics_view.setCentralItem(self.view)

    # File Menu Action
    self.ui.action_new.triggered.connect(self.on_new_triggered)
    self.ui.action_open.triggered.connect(self.on_open_triggered)
    self.ui.action_save.triggered.connect(self.on_save_triggered)
    self.ui.action_save_as.triggered.connect(self.on_save_as_triggered)
    self.ui.action_render.triggered.connect(self.on_render_triggered)
    self.ui.action_export.triggered.connect(self.on_export_triggered)
    self.ui.action_close.triggered.connect(self.on_close_triggered)

    # GUI Action
    self.ui.timeline_slider.valueChanged.connect(self.on_index_valuechanged)
    self.ui.timeline_frame_index_spinbox.valueChanged.connect(self.on_index_valuechanged)
    self.ui.timeline_frame_range_window_upper_spinbox.valueChanged.connect(
      self.on_timeline_frame_range_window_upper_spinbox_valuechanged)
    self.ui.timeline_frame_range_window_lower_spinbox.valueChanged.connect(
      self.on_timeline_frame_range_window_lower_spinbox_valuechanged)

    self.ui.temporal_prepare_pushbutton.clicked.connect(self.on_temporal_prepare_triggered)

    Configuration.on_filename_changed.connect(self.on_filename_changed)

    self.soft_reset()

  def on_new_triggered(self):
    filename = QtGui.QFileDialog.getOpenFileName(parent=self, caption='New Session...',
                                                 filter=QFILEDIALOG_IMAGE_SEQUENCE_FILTER)
    self.activateWindow()
    if filename:
      self.hard_reset()
      Configuration.update({'_sequence': {'_file_pattern': build_pattern_from_path(str(filename))}})

      self.setup()

  def on_open_triggered(self):
    filename = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open...',
                                                 filter=QFILEDIALOG_CONFIGURATION_FILTER)
    self.activateWindow()
    if filename:
      Configuration.open(str(filename))
      self.setup()

  def on_save_triggered(self):
    if Configuration.filename:
      Configuration.save()
    else:
      self.on_save_as_triggered()

  def on_save_as_triggered(self):
    filename = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Save...',
                                                 filter=QFILEDIALOG_CONFIGURATION_FILTER)
    self.activateWindow()
    if filename:
      Configuration.save(str(filename))

  def on_render_triggered(self):
    pass

  def on_export_triggered(self):
    filename = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Save...',
                                                 filter=QFILEDIALOG_MATLAB_FILTER)
    self.activateWindow()
    if filename:
      pass

  def on_close_triggered(self):
    self.hard_reset()

  @staticmethod
  def on_index_valuechanged(index):
    Configuration.sequence.index = index

  @staticmethod
  def on_timeline_frame_range_window_lower_spinbox_valuechanged(new_value):
    Configuration.sequence.frame_range_window.lower_limit = new_value

  @staticmethod
  def on_timeline_frame_range_window_upper_spinbox_valuechanged(new_value):
    Configuration.sequence.frame_range_window.upper_limit = new_value

  def on_temporal_prepare_triggered(self):
    ProcessorDialog(PrepareProcessor(), self).exec_()

  def setup(self):
    self.soft_reset()

    Configuration.sequence = ImageSequence(Configuration.sequence)
    Configuration.temporal = Temporal(Configuration.temporal)
    Configuration.leonhardt_tmo = LeonhardtTMO(Configuration.leonhardt_tmo)

    Configuration.leonhardt_tmo.processor = LeonhardtTMOProcessor()

    for widget in [self.ui.options_widget,
                   self.ui.timeline_widget]:
      widget.setEnabled(True)

    for widget in [self.ui.timeline_slider,
                   self.ui.timeline_frame_index_spinbox,
                   self.ui.timeline_frame_range_window_lower_spinbox,
                   self.ui.timeline_frame_range_window_upper_spinbox]:
      widget.blockSignals(True)
      widget.setRange(*Configuration.sequence.frame_range.range)
      widget.blockSignals(False)

    self.ui.timeline_frame_range_window_lower_spinbox.setValue(Configuration.sequence.frame_range_window.lower_limit)
    self.ui.timeline_frame_range_window_upper_spinbox.setValue(Configuration.sequence.frame_range_window.upper_limit)

    self.ui.timeline_frame_range_lower.setText(str(Configuration.sequence.frame_range.lower_limit))
    self.ui.timeline_frame_range_upper.setText(str(Configuration.sequence.frame_range.upper_limit))

    bind_to_value(
      widgets=[self.ui.timeline_slider, self.ui.timeline_frame_index_spinbox],
      property_holder=Configuration.sequence,
      property_key='index'
    )

    Configuration.sequence.on_index_changed.connect(self.view.invalidate_by_index)
    Configuration.sequence.index = Configuration.sequence.frame_range.lower_limit

    Configuration.temporal.on_propery_changed.connect(self.view.invalidate)
    Configuration.leonhardt_tmo.on_propery_changed.connect(self.view.invalidate)
    Configuration.sequence.on_exposure_offset_changed.connect(self.view.invalidate)

    bind_to_value(
      widgets=[self.ui.viewer_exposure_slider, self.ui.viewer_exposure_spinbox],
      property_holder=self.view,
      property_key='exposure'
    )

    bind_to_value(
      widgets=[self.ui.sequence_exposure_offset_slider, self.ui.sequence_exposure_offset_spinbox],
      property_holder=Configuration.sequence,
      property_key='exposure_offset'
    )

    bind_to_value(
      widgets=[self.ui.tonemapper_preview_checkbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='preview'
    )

    bind_to_value(
      widgets=[self.ui.tonemapper_brightness_offset_slider, self.ui.tonemapper_brightness_offset_spinbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='brightness_offset'
    )

    bind_to_value(
      widgets=[self.ui.tonemapper_contrast_slider, self.ui.tonemapper_contrast_spinbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='contrast'
    )

    bind_to_value(
      widgets=[self.ui.tonemapper_gamma_slider, self.ui.tonemapper_gamma_spinbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='gamma'
    )

    bind_to_value(
      widgets=[self.ui.detaildrawback_drawback_details_checkbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='drawback_details'
    )

    bind_to_value(
      widgets=[self.ui.detaildrawback_detail_drawback_slider, self.ui.detaildrawback_detail_drawback_spinbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='detail_drawback'
    )

    bind_to_value(
      widgets=[self.ui.detaildrawback_detail_highlight_slider, self.ui.detaildrawback_detail_highlight_spinbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='detail_highlight'
    )

    bind_to_value(
      widgets=[self.ui.detaildrawback_alpha_slider, self.ui.detaildrawback_alpha_spinbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='alpha'
    )

    bind_to_value(
      widgets=[self.ui.detaildrawback_lambda_slider, self.ui.detaildrawback_lambda_spinbox],
      property_holder=Configuration.leonhardt_tmo,
      property_key='lambda_'
    )

    bind_to_value(
      widgets=[self.ui.temporal_quantile_lower_slider, self.ui.temporal_quantile_lower_spinbox],
      property_holder=Configuration.temporal,
      property_key='quantile_lower'
    )

    bind_to_value(
      widgets=[self.ui.temporal_quantile_upper_slider, self.ui.temporal_quantile_upper_spinbox],
      property_holder=Configuration.temporal,
      property_key='quantile_upper'
    )

    bind_to_value(
      widgets=[self.ui.temporal_alpha_slider, self.ui.temporal_alpha_spinbox],
      property_holder=Configuration.temporal,
      property_key='alpha'
    )

    bind_to_value(
      widgets=[self.ui.temporal_lambda_slider, self.ui.temporal_lambda_spinbox],
      property_holder=Configuration.temporal,
      property_key='lambda_'
    )

  def soft_reset(self):
    for widget in [self.ui.options_widget,
                   self.ui.timeline_widget]:
      widget.setEnabled(False)
    self.view.clear()

  def hard_reset(self):
    self.soft_reset()
    Configuration.clear()
    self.setWindowTitle("")

  def on_filename_changed(self, filename):
    filename = str(filename)
    if filename:
      self.setWindowTitle("{0:s} - [{1:s}]".format(os.path.basename(filename), filename))
    else:
      self.setWindowTitle("untitled")


  # @staticmethod
  # def bind(widgets, property_owner, property_key, property_event):
  #   def bind_property(property_owner, property_key, value):
  #     if hasattr(property_owner.__class__, property_key):
  #       property_object = getattr(property_owner.__class__, property_key)
  #       if isinstance(property_object, property):
  #         if property_object.fset is None:
  #           raise AttributeError
  #         property_object.fset(property_owner, value)
  #
  #   def bind_widget(widget, sender, value):
  #     widget.blockSignals(True)
  #     widget.setValue(value)
  #     widget.blockSignals(False)
  #
  #   for widget in widgets:
  #     widget.setValue
  #     widget.valueChanged.connect(functools.partial(bind_property, property_owner, property_key))
  #     property_event += functools.partial(bind_widget, widget)
