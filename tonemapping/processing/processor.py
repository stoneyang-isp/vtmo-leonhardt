from threading import Thread
from obsub import event

from .progressbar import ProgressBar, Timer, SimpleProgress, Percentage, ETA


class Processor(Thread):
  def __init__(self):
    Thread.__init__(self)
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
      self.on_progress(index, self.progress)

    if hasattr(self, 'after') and not self._cancel_requested:
      self.after()

    self._cancel_requested = False
    self.progress.finish()
    self.on_finish()

  def __iter__(self):
    pass

  def cancel(self):
    self._cancel_requested = True

  @event
  def on_progress(self, index, data):
    pass

  @event
  def on_finish(self):
    pass