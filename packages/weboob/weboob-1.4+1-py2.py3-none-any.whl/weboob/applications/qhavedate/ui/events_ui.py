# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'events.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Events(object):
    def setupUi(self, Events):
        Events.setObjectName("Events")
        Events.resize(497, 318)
        self.verticalLayout = QtWidgets.QVBoxLayout(Events)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.typeBox = QtWidgets.QComboBox(Events)
        self.typeBox.setObjectName("typeBox")
        self.horizontalLayout_2.addWidget(self.typeBox)
        self.refreshButton = QtWidgets.QToolButton(Events)
        self.refreshButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../usr/share/icons/oxygen/16x16/actions/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout_2.addWidget(self.refreshButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.eventsList = QtWidgets.QTreeWidget(Events)
        self.eventsList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.eventsList.setAlternatingRowColors(True)
        self.eventsList.setIconSize(QtCore.QSize(64, 64))
        self.eventsList.setRootIsDecorated(False)
        self.eventsList.setAnimated(True)
        self.eventsList.setObjectName("eventsList")
        self.verticalLayout.addWidget(self.eventsList)

        self.retranslateUi(Events)
        QtCore.QMetaObject.connectSlotsByName(Events)

    def retranslateUi(self, Events):
        _translate = QtCore.QCoreApplication.translate
        Events.setWindowTitle(_translate("Events", "Form"))
        self.eventsList.setSortingEnabled(True)
        self.eventsList.headerItem().setText(0, _translate("Events", "Contact"))
        self.eventsList.headerItem().setText(1, _translate("Events", "Date"))
        self.eventsList.headerItem().setText(2, _translate("Events", "Type"))
        self.eventsList.headerItem().setText(3, _translate("Events", "Message"))

