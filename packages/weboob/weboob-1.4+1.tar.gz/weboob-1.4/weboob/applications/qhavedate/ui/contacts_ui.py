# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contacts.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Contacts(object):
    def setupUi(self, Contacts):
        Contacts.setObjectName("Contacts")
        Contacts.resize(478, 374)
        self.verticalLayout = QtWidgets.QVBoxLayout(Contacts)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(Contacts)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QComboBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout.addWidget(self.groupBox)
        self.refreshButton = QtWidgets.QToolButton(self.frame)
        self.refreshButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../usr/share/icons/oxygen/16x16/actions/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout.addWidget(self.refreshButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.contactList = QtWidgets.QListWidget(self.frame)
        self.contactList.setIconSize(QtCore.QSize(120, 120))
        self.contactList.setWordWrap(True)
        self.contactList.setSelectionRectVisible(False)
        self.contactList.setObjectName("contactList")
        self.verticalLayout_2.addWidget(self.contactList)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.urlEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.urlEdit.setObjectName("urlEdit")
        self.verticalLayout_3.addWidget(self.urlEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.backendsList = QtWidgets.QComboBox(self.groupBox_2)
        self.backendsList.setObjectName("backendsList")
        self.horizontalLayout_2.addWidget(self.backendsList)
        self.urlButton = QtWidgets.QPushButton(self.groupBox_2)
        self.urlButton.setObjectName("urlButton")
        self.horizontalLayout_2.addWidget(self.urlButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Contacts)
        QtCore.QMetaObject.connectSlotsByName(Contacts)

    def retranslateUi(self, Contacts):
        _translate = QtCore.QCoreApplication.translate
        Contacts.setWindowTitle(_translate("Contacts", "Form"))
        self.contactList.setSortingEnabled(True)
        self.groupBox_2.setTitle(_translate("Contacts", "From URL"))
        self.urlButton.setText(_translate("Contacts", "Display"))

