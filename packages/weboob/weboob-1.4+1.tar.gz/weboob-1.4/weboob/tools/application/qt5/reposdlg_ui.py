# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reposdlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RepositoriesDlg(object):
    def setupUi(self, RepositoriesDlg):
        RepositoriesDlg.setObjectName("RepositoriesDlg")
        RepositoriesDlg.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(RepositoriesDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.reposEdit = QtWidgets.QTextEdit(RepositoriesDlg)
        self.reposEdit.setObjectName("reposEdit")
        self.verticalLayout.addWidget(self.reposEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(RepositoriesDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RepositoriesDlg)
        self.buttonBox.rejected.connect(RepositoriesDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(RepositoriesDlg)

    def retranslateUi(self, RepositoriesDlg):
        _translate = QtCore.QCoreApplication.translate
        RepositoriesDlg.setWindowTitle(_translate("RepositoriesDlg", "Repositories"))

