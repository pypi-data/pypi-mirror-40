# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(709, 572)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchEdit = QtWidgets.QLineEdit(self.widget)
        self.searchEdit.setObjectName("searchEdit")
        self.horizontalLayout.addWidget(self.searchEdit)
        self.searchButton = QtWidgets.QToolButton(self.widget)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)
        self.verticalLayout.addWidget(self.widget)
        self.bugList = QtWidgets.QTableView(self.centralwidget)
        self.bugList.setAlternatingRowColors(True)
        self.bugList.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.bugList.setSortingEnabled(True)
        self.bugList.setCornerButtonEnabled(False)
        self.bugList.setObjectName("bugList")
        self.bugList.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.bugList)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 709, 20))
        self.menubar.setObjectName("menubar")
        self.menuIssues = QtWidgets.QMenu(self.menubar)
        self.menuIssues.setObjectName("menuIssues")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionBackends = QtWidgets.QAction(MainWindow)
        self.actionBackends.setObjectName("actionBackends")
        self.actionBulk = QtWidgets.QAction(MainWindow)
        self.actionBulk.setObjectName("actionBulk")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuIssues.addAction(self.actionOpen)
        self.menuIssues.addAction(self.actionBulk)
        self.menubar.addAction(self.menuIssues.menuAction())
        self.toolBar.addAction(self.actionBackends)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QBoobTracker"))
        self.searchEdit.setPlaceholderText(_translate("MainWindow", "Search query"))
        self.searchButton.setText(_translate("MainWindow", "Go"))
        self.menuIssues.setTitle(_translate("MainWindow", "Issues"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionBackends.setText(_translate("MainWindow", "Backends"))
        self.actionBulk.setText(_translate("MainWindow", "Bulk &edit"))
        self.actionBulk.setShortcut(_translate("MainWindow", "Alt+E"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Alt+O"))

