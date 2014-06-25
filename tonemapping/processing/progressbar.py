"""Text progress bar library for Python.

A text progress bar is typically used to display the progress of a long
running operation, providing a visual cue that processing is underway.

The ProgressBar class manages the current progress, and the format of the line
is given by a number of widgets. A widget is an object that may display
differently depending on the state of the progress bar. There are three types
of widgets:

 - a string, which always shows itself

 - a ProgressBarWidget, which may return a different value every time its
   update method is called

 - a ProgressBarWidgetHFill, which is like ProgressBarWidget, except it
   expands to fill the remaining width of the line.

The progressbar module is very easy to use, yet very powerful. It will also
automatically enable features like auto-resizing when the system supports it.
"""
from __future__ import division, absolute_import, with_statement

import datetime
import abc
import math

import os
import signal
import sys
import time
from obsub import event


try:
  from fcntl import ioctl
  from array import array
  import termios
except ImportError:  # pragma: no cover
  pass

try:
  from cStringIO import StringIO
except ImportError:  # pragma: no cover
  try:
    from StringIO import StringIO
  except ImportError:
    from io import StringIO


class UnknownLength:
  pass


class ProgressBar(object):
  """The ProgressBar class which updates and prints the bar.

  A common way of using it is like:

  >>> pbar = ProgressBar().start()
  >>> for i in range(100):
  ...     pbar.update(i+1)
  ...     # do something
  ...
  >>> pbar.finish()

  You can also use a ProgressBar as an iterator:

  >>> progress = ProgressBar()
  >>> some_iterable = range(100)
  >>> for i in progress(some_iterable):
  ...     # do something
  ...     pass
  ...

  Since the progress bar is incredibly customizable you can specify
  different widgets of any type in any order. You can even write your own
  widgets! However, since there are already a good number of widgets you
  should probably play around with them before moving on to create your own
  widgets.

  The term_width parameter represents the current terminal width. If the
  parameter is set to an integer then the progress bar will use that,
  otherwise it will attempt to determine the terminal width falling back to
  80 columns if the width cannot be determined.

  When implementing a widget's update method you are passed a reference to
  the current progress bar. As a result, you have access to the
  ProgressBar's methods and attributes. Although there is nothing preventing
  you from changing the ProgressBar you should treat it as read only.

  Useful methods and attributes include (Public API):
   - currval: current progress (0 <= currval <= maxval)
   - maxval: maximum (and final) value
   - finished: True if the bar has finished (reached 100%)
   - start_time: the time when start() method of ProgressBar was called
   - seconds_elapsed: seconds elapsed since start_time and last call to
                      update
   - percentage(): progress in percent [0..100]
  """

  def __init__(self, maximum=100, widgets=None, poll=0.1):
    """Initializes a progress bar with sane defaults"""

    # Don't share a reference with any other progress bars
    if widgets is None:
      widgets = {"simpleProgress": SimpleProgress(), "percentage": Percentage()}

    self.maximum = maximum
    self.widgets = widgets

    self.__iterable = None
    self._time_sensitive = any(getattr(w, 'TIME_SENSITIVE', False) for w in self.widgets)
    self.value = -1
    self.finished = False
    self.last_update_time = None
    self.poll = poll
    self.seconds_elapsed = 0
    self.start_time = None
    self.update_interval = 1

  # def __call__(self, iterable):
  #   """Use a ProgressBar to iterate through an iterable"""
  #
  #   try:
  #     self.maximum = len(iterable)
  #   except:
  #     if self.maximum is None:
  #       self.maximum = UnknownLength
  #
  #   self.__iterable = iter(iterable)
  #   return self
  #
  # def __iter__(self):
  #   return self
  #
  # def __next__(self):
  #   try:
  #     value = next(self.__iterable)
  #     if self.start_time is None:
  #       self.start()
  #     else:
  #       self.update(self.value + 1)
  #     return value
  #   except StopIteration:
  #     self.finish()
  #     raise

  # def __exit__(self, exc_type, exc_value, traceback):
  #   self.finish()
  #
  # def __enter__(self):
  #   return self.start()

  # Create an alias so that Python 2.x won't complain about not being
  # an iterator.
  # next = __next__

  def __iadd__(self, value):
    """Updates the ProgressBar by adding a new value."""
    self.update(self.value + value)
    return self

  def percentage(self):
    """Returns the progress as a percentage."""
    return self.value * 100.0 / self.maximum

  percent = property(percentage)

  def _need_update(self):
    """Returns whether the ProgressBar should redraw the line."""
    if self.value >= self.next_update or self.finished:
      return True

    delta = time.time() - self.last_update_time
    return self._time_sensitive and delta > self.poll

  def update(self, value=None):
    if value is not None and value is not UnknownLength:
      if self.maximum is not UnknownLength and not 0 <= value <= self.maximum and not value < self.value:
        raise ValueError('Value out of range')

      self.value = value

    if self.start_time is None:
      raise RuntimeError('You must call "start" before calling "update"')
    if not self._need_update():
      return

    now = time.time()
    self.seconds_elapsed = now - self.start_time
    self.next_update = self.value + self.update_interval

    for widget in self.widgets.values():
      if hasattr(widget, 'update'):
        widget.update(self)

    self._update()
    self.last_update_time = now

  def _update(self):
    pass

  # def _update_print_msgpack(self):
  #   for widget in self.widgets:
  #     update_updatable(widget, self)
  #
  #   # self.fd.write(msgpack.packb([widget.value for widget in self.widgets]))
  #   # self.fd.flush()

  @property
  def data(self):
    result = {}
    for key, widget in self.widgets.items():
      result[key] = widget.value
    return result

  def start(self):
    self.num_intervals = 100
    self.next_update = 0

    if self.maximum is not UnknownLength:
      if self.maximum < 0:
        raise ValueError('Value out of range')
      self.update_interval = self.maximum / self.num_intervals

    self.start_time = self.last_update_time = time.time()
    self.update(0)

    return self

  def finish(self):
    self.finished = True
    self.update(self.maximum)


class TextProgressBar(ProgressBar):

  _DEFAULT_TERMSIZE = 80

  def __init__(self, maximum=100, widgets=None, terminal_width=_DEFAULT_TERMSIZE, poll=0.1, left_justify=True,
               fd=sys.stderr, redirect_stderr=False, redirect_stdout=False, format=""):
    """Initializes a progress bar with sane defaults"""
    ProgressBar.__init__(self, maximum=maximum, widgets=widgets, poll=poll)
    self.fd = fd
    self.left_justify = left_justify
    self.redirect_stderr = redirect_stderr
    self.redirect_stdout = redirect_stdout
    self.format = format

    self.signal_set = False
    if terminal_width is not None:
      self.terminal_width = terminal_width
    else:
      try:
        self._handle_resize()
        signal.signal(signal.SIGWINCH, self._handle_resize)
        self.signal_set = True
      except (SystemExit, KeyboardInterrupt):  # pragma: no cover
        raise
      except:  # pragma: no cover
        self.terminal_width = self._env_size()

  def _update(self):
    if self.redirect_stderr and sys.stderr.tell():
      self.fd.write('\r' + ' ' * self.terminal_width + '\r')
      self._stderr.write(sys.stderr.getvalue())
      self._stderr.flush()
      sys.stderr = StringIO()

    if self.redirect_stdout and sys.stdout.tell():
      self.fd.write('\r' + ' ' * self.terminal_width + '\r')
      self._stdout.write(sys.stdout.getvalue())
      self._stdout.flush()
      sys.stdout = StringIO()

    self.fd.write('\r' + self._format_line())

  def _format_line(self):
    self._format_widgets()

    result = self.format.format(**self.data)

    if self.left_justify:
      return result.ljust(self.terminal_width)
    else:
      return result.rjust(self.terminal_width)

  def _format_widgets(self):
    result = []
    expanding = []
    width = self.terminal_width

    for index, widget in enumerate(self.widgets.values()):
      # if isinstance(widget, WidgetHFill):
      # result.append(widget)
      # expanding.insert(0, index)
      # else:
      if hasattr(widget, 'update'):
        widget.update(self)

      widget = str(widget)
      result.append(widget)
      width -= len(widget)

    count = len(expanding)
    while count:
      portion = max(int(math.ceil(width * 1. / count)), 0)
      index = expanding.pop()
      count -= 1

      widget = result[index].update(self, portion)
      width -= len(widget)
      result[index] = widget

  def start(self):
    self.num_intervals = max(100, self.terminal_width)

    if self.redirect_stderr:
      self._stderr = sys.stderr
      sys.stderr = StringIO()

    if self.redirect_stdout:
      self._stdout = sys.stdout
      sys.stdout = StringIO()

    return ProgressBar.start(self)

  def finish(self):
    ProgressBar.finish(self)
    self.fd.write('\n')
    if self.signal_set:
      signal.signal(signal.SIGWINCH, signal.SIG_DFL)

    if self.redirect_stderr:
      self._stderr.write(sys.stderr.getvalue())
      sys.stderr = self._stderr

    if self.redirect_stdout:
      self._stdout.write(sys.stdout.getvalue())
      sys.stdout = self._stdout

  def _env_size(self):
    """Tries to find the term_width from the environment."""

    return int(os.environ.get('COLUMNS', self._DEFAULT_TERMSIZE)) - 1

  def _handle_resize(self, signum=None, frame=None):
    """Tries to catch resize signals sent from the terminal."""

    h, w = array('h', ioctl(self.fd, termios.TIOCGWINSZ, '\0' * 8))[:2]
    self.terminal_width = w


class AbstractWidget(object):
  __metaclass__ = abc.ABCMeta


class Widget(AbstractWidget):
  """The base class for all widgets

  The ProgressBar will call the widget's update value when the widget should
  be updated. The widget's size may change between calls, but the widget may
  display incorrectly if the size changes drastically and repeatedly.

  The boolean TIME_SENSITIVE informs the ProgressBar that it should be
  updated more often because it is time sensitive.
  """

  TIME_SENSITIVE = False

  def __init__(self):
    self.value = None

  @abc.abstractmethod
  def update(self, progress_bar):
    """Updates the widget.

    pbar - a reference to the calling ProgressBar
    """

  def __str__(self):
    return self.value


class Timer(Widget):
  """Widget which displays the elapsed seconds."""

  TIME_SENSITIVE = True

  def __init__(self):
    super(Timer, self).__init__()

  @staticmethod
  def format_time(seconds):
    """Formats time as the string "HH:MM:SS"."""

    return str(datetime.timedelta(seconds=int(seconds)))

  def update(self, progress_bar):
    """Updates the widget to show the elapsed time."""

    self.value = self.format_time(progress_bar.seconds_elapsed)

  def __str__(self):
    return str(self.value)


class ETA(Timer):
  """Widget which attempts to estimate the time of arrival."""

  TIME_SENSITIVE = True

  def update(self, progress_bar):
    """Updates the widget to show the ETA or total time when finished."""

    if progress_bar.value == 0:
      self.value = {
        'prefix': 'Remaining',
        'value': '--:--:--'
      }
    elif progress_bar.finished:
      self.value = {
        'prefix': 'Total',
        'value': self.format_time(progress_bar.seconds_elapsed)
      }
    else:
      elapsed = progress_bar.seconds_elapsed
      eta = elapsed * progress_bar.maximum / progress_bar.value - elapsed
      self.value = {
        'prefix': 'Remaining',
        'value': self.format_time(eta)
      }

  def __str__(self):
    return self.value['prefix'] + self.value['value']


class Percentage(Widget):
  """Displays the current percentage as a number with a percent sign."""

  def update(self, progress_bar):
    self.value = '%3d%%' % progress_bar.percentage()


class SimpleProgress(Widget):
  """Returns progress as a count of the total (e.g.: "5 of 47")"""

  def __init__(self, delimiter=' of '):
    super(SimpleProgress, self).__init__()
    self.delimiter = delimiter

  def update(self, progress_bar):
    self.value = {
      'value': progress_bar.value,
      'max': progress_bar.maximum
    }

  def __str__(self):
    return ('%0' + str(int(math.log10(self.value['max'])) + 1) + 'd%s%d') % (self.value['value'], self.delimiter, self.value['max'])