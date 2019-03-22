# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/dump_media_device.ui',
# licensing of 'UI/dump_media_device.ui' applies.
#
# Created: Fri Mar 22 17:06:10 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(410, 240)
        self.okButton = QtWidgets.QDialogButtonBox(Dialog)
        self.okButton.setGeometry(QtCore.QRect(30, 200, 371, 32))
        self.okButton.setOrientation(QtCore.Qt.Horizontal)
        self.okButton.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.okButton.setObjectName("okButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 101, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(150, 20, 231, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 111, 16))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 180, 411, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(0, 130, 411, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 150, 391, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(150, 60, 231, 31))
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 111, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(150, 90, 231, 31))
        self.comboBox_2.setCurrentText("")
        self.comboBox_2.setObjectName("comboBox_2")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dump media device", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Project Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Source Drive", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Trarget Drive", None, -1))

