import sys
from PyQt4 import QtGui
from gui import MainWindow


def main():
  app = QtGui.QApplication([])

  main_window = MainWindow()
  main_window.showMaximized()
  main_window.raise_()

  sys.exit(app.exec_())


if __name__ == "__main__":
  main()