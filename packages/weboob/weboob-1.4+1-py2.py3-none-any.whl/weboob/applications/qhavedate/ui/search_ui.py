# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Search(object):
    def setupUi(self, Search):
        Search.setObjectName("Search")
        Search.resize(438, 349)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Search)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.statusFrame = QtWidgets.QFrame(Search)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusFrame.sizePolicy().hasHeightForWidth())
        self.statusFrame.setSizePolicy(sizePolicy)
        self.statusFrame.setMaximumSize(QtCore.QSize(300, 16777215))
        self.statusFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.statusFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.statusFrame.setObjectName("statusFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.statusFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2.addWidget(self.statusFrame)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.queueLabel = QtWidgets.QLabel(Search)
        self.queueLabel.setText("")
        self.queueLabel.setObjectName("queueLabel")
        self.gridLayout.addWidget(self.queueLabel, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Search)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.frame = QtWidgets.QFrame(Search)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.queryButton = QtWidgets.QPushButton(self.frame)
        self.queryButton.setObjectName("queryButton")
        self.horizontalLayout.addWidget(self.queryButton)
        self.nextButton = QtWidgets.QPushButton(self.frame)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout.addWidget(self.nextButton)
        self.verticalLayout.addWidget(self.frame)
        self.scrollArea = QtWidgets.QScrollArea(Search)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 178, 235))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Search)
        QtCore.QMetaObject.connectSlotsByName(Search)

    def retranslateUi(self, Search):
        _translate = QtCore.QCoreApplication.translate
        Search.setWindowTitle(_translate("Search", "Form"))
        self.label.setText(_translate("Search", "<b>Profiles in queue:</b>"))
        self.queryButton.setText(_translate("Search", "Query"))
        self.nextButton.setText(_translate("Search", "Next"))

