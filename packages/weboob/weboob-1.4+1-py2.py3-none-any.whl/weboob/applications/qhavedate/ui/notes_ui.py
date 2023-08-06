# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notes.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Notes(object):
    def setupUi(self, Notes):
        Notes.setObjectName("Notes")
        Notes.resize(430, 323)
        self.verticalLayout = QtWidgets.QVBoxLayout(Notes)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(Notes)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.saveButton = QtWidgets.QPushButton(Notes)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)

        self.retranslateUi(Notes)
        QtCore.QMetaObject.connectSlotsByName(Notes)

    def retranslateUi(self, Notes):
        _translate = QtCore.QCoreApplication.translate
        Notes.setWindowTitle(_translate("Notes", "Form"))
        self.saveButton.setText(_translate("Notes", "Save"))

