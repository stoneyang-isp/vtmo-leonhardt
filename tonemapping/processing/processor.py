from PyQt4.QtCore import QThread, pyqtSignal

from .progressbar import ProgressBar, Timer, SimpleProgress, Percentage, ETA


class Processor(QThread):
  on_progress = pyqtSignal(int, ProgressBar)
  on_finish = pyqtSignal()

  def __init__(self):
    QThread.__init__(self)
    self._cancel_requested = False
    self.processing_range = None

    widgets = {"eta": ETA(), "timer": Timer(), "simpleProgress": SimpleProgress(delimiter="/"), "percentage": Percentage()}
    self.progress = ProgressBar(widgets=widgets).start()

  def run(self):
    self.progress.maximum = len(self.processing_range)

    if hasattr(self, 'before'):
      self.before()

    self.progress.start()
    for index in iter(self):
      if self._cancel_requested:
        break
      self.progress.update(index)
      self.on_progress.emit(index, self.progress)

    if hasattr(self, 'after') and not self._cancel_requested:
      self.after()

    self._cancel_requested = False
    self.progress.finish()
    self.on_finish.emit()

  def __iter__(self):
    pass

  def cancel(self):
    self._cancel_requested = True