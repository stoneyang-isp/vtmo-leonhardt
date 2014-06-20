# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/manuelleonhardt/Dropbox/Workspaces/pycharm/gazetrack/gui/processing/processing_view.ui'
#
# Created: Sat Jun 14 17:15:55 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ProcessingDialog(object):
    def setupUi(self, ProcessingDialog):
        ProcessingDialog.setObjectName(_fromUtf8("ProcessingDialog"))
        ProcessingDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ProcessingDialog.resize(729, 112)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProcessingDialog.sizePolicy().hasHeightForWidth())
        ProcessingDialog.setSizePolicy(sizePolicy)
        ProcessingDialog.setMinimumSize(QtCore.QSize(729, 0))
        ProcessingDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(ProcessingDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressBar = QtGui.QProgressBar(ProcessingDialog)
        self.progressBar.setMaximum(0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(ProcessingDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(ProcessingDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_3 = QtGui.QLabel(ProcessingDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ProcessingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ProcessingDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProcessingDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProcessingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProcessingDialog)

    def retranslateUi(self, ProcessingDialog):
        ProcessingDialog.setWindowTitle(_translate("ProcessingDialog", "Working...", None))
        self.label.setText(_translate("ProcessingDialog", "Elapsed: {timer}", None))
        self.label_2.setText(_translate("ProcessingDialog", "Frame {simpleProgress[value]} of {simpleProgress[max]} ({percentage})", None))
        self.label_3.setText(_translate("ProcessingDialog", "Remaining {eta[value]}", None))

