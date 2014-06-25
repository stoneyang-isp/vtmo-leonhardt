from PyQt4 import QtCore, QtGui
from .processing_view import Ui_ProcessingDialog


class ProcessorDialog(QtGui.QDialog):
  formatted_elements = ['label', 'label_2', 'label_3']
  on_progress = QtCore.pyqtSignal(int, object)
  on_finish = QtCore.pyqtSignal()

  def __init__(self, processor, parent=None):
    QtGui.QDialog.__init__(self, parent)

    # GUI
    self.ui = Ui_ProcessingDialog()
    self.ui.setupUi(self)

    self.formatted_elements = [getattr(self.ui, key) for key in self.formatted_elements]
    self.formatted_elements = zip([str(widget.text()) for widget in self.formatted_elements], self.formatted_elements)

    for format, widget in self.formatted_elements:
      widget.setText("")

    self.on_progress.connect(self.progress)
    self.on_finish.connect(self.finish)
    self.processor = processor
    self.ui.progressBar.setRange(0, len(self.processor.processing_range))
    self.processor.on_progress += self.processor_on_progress
    self.processor.on_finish += self.processor_on_finish

    self.processor.start()

  def processor_on_progress(self, sender, index, progressbar):
    self.on_progress.emit(index, progressbar)

  def progress(self, index, progressbar):
    for format, widget in self.formatted_elements:
      widget.setText(format.format(**progressbar.data))
    self.ui.progressBar.setValue(index)

  def finish(self):
    self.close()

  def processor_on_finish(self, sender):
    self.on_finish.emit()

  def reject(self):
    self.processor.cancel()
    QtGui.QDialog.reject(self)