# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thread_message.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ThreadMessage(object):
    def setupUi(self, ThreadMessage):
        ThreadMessage.setObjectName("ThreadMessage")
        ThreadMessage.resize(552, 76)
        ThreadMessage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        ThreadMessage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ThreadMessage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.imageLabel = QtWidgets.QLabel(ThreadMessage)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.verticalLayout.addWidget(self.imageLabel)
        self.nameLabel = QtWidgets.QLabel(ThreadMessage)
        self.nameLabel.setText("")
        self.nameLabel.setObjectName("nameLabel")
        self.verticalLayout.addWidget(self.nameLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.widget = QtWidgets.QWidget(ThreadMessage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headerLabel = QtWidgets.QLabel(self.widget)
        self.headerLabel.setText("")
        self.headerLabel.setWordWrap(True)
        self.headerLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_2.addWidget(self.headerLabel)
        self.contentLabel = QtWidgets.QLabel(self.widget)
        self.contentLabel.setText("")
        self.contentLabel.setWordWrap(True)
        self.contentLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.contentLabel.setObjectName("contentLabel")
        self.verticalLayout_2.addWidget(self.contentLabel)
        spacerItem1 = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(ThreadMessage)
        QtCore.QMetaObject.connectSlotsByName(ThreadMessage)

    def retranslateUi(self, ThreadMessage):
        _translate = QtCore.QCoreApplication.translate
        ThreadMessage.setWindowTitle(_translate("ThreadMessage", "Frame"))

