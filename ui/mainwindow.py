# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 695)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.triggerSlider = QtWidgets.QSlider(self.centralwidget)
        self.triggerSlider.setOrientation(QtCore.Qt.Vertical)
        self.triggerSlider.setObjectName("triggerSlider")
        self.gridLayout.addWidget(self.triggerSlider, 1, 1, 1, 1)
        self.plotPlaceHolder = QtWidgets.QLabel(self.centralwidget)
        self.plotPlaceHolder.setText("")
        self.plotPlaceHolder.setObjectName("plotPlaceHolder")
        self.gridLayout.addWidget(self.plotPlaceHolder, 1, 0, 1, 1)
        self.triggerSliderLabel = QtWidgets.QLabel(self.centralwidget)
        self.triggerSliderLabel.setObjectName("triggerSliderLabel")
        self.gridLayout.addWidget(self.triggerSliderLabel, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 17))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionZoom = QtWidgets.QAction(MainWindow)
        self.actionZoom.setObjectName("actionZoom")
        self.actionDisplay = QtWidgets.QAction(MainWindow)
        self.actionDisplay.setObjectName("actionDisplay")
        self.menuFile.addAction(self.actionNew)
        self.menuView.addAction(self.actionZoom)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionDisplay)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.triggerSliderLabel.setText(_translate("MainWindow", "trigger"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionZoom.setText(_translate("MainWindow", "Zoom"))
        self.actionDisplay.setText(_translate("MainWindow", "Display (Debug)"))
        self.actionDisplay.setToolTip(_translate("MainWindow", "Display for Developer to test."))
