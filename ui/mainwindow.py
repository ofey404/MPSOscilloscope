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
        MainWindow.resize(1500, 1500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.leftPanelSplitter = QtWidgets.QSplitter(self.centralwidget)
        self.leftPanelSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.leftPanelSplitter.setObjectName("leftPanelSplitter")
        self.configTab = QtWidgets.QTabWidget(self.leftPanelSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configTab.sizePolicy().hasHeightForWidth())
        self.configTab.setSizePolicy(sizePolicy)
        self.configTab.setMaximumSize(QtCore.QSize(256, 16777215))
        self.configTab.setMovable(True)
        self.configTab.setTabBarAutoHide(False)
        self.configTab.setObjectName("configTab")
        self.viewTab = QtWidgets.QWidget()
        self.viewTab.setObjectName("viewTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.viewTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.viewTab)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.configTab.addTab(self.viewTab, "")
        self.modelTab = QtWidgets.QWidget()
        self.modelTab.setObjectName("modelTab")
        self.configTab.addTab(self.modelTab, "")
        self.horizontalWidget = QtWidgets.QWidget(self.leftPanelSplitter)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.horizontalWidget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.bottomPanelSplitter = QtWidgets.QSplitter(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottomPanelSplitter.sizePolicy().hasHeightForWidth())
        self.bottomPanelSplitter.setSizePolicy(sizePolicy)
        self.bottomPanelSplitter.setOrientation(QtCore.Qt.Vertical)
        self.bottomPanelSplitter.setObjectName("bottomPanelSplitter")
        self.gridLayoutWidget = QtWidgets.QWidget(self.bottomPanelSplitter)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.gridLayoutWidget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.displayPlaceHolder = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayPlaceHolder.sizePolicy().hasHeightForWidth())
        self.displayPlaceHolder.setSizePolicy(sizePolicy)
        self.displayPlaceHolder.setBaseSize(QtCore.QSize(0, 0))
        self.displayPlaceHolder.setText("")
        self.displayPlaceHolder.setObjectName("displayPlaceHolder")
        self.gridLayout_2.addWidget(self.displayPlaceHolder, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)
        self.displayVerticalScrollBar = QtWidgets.QScrollBar(self.gridLayoutWidget)
        self.displayVerticalScrollBar.setPageStep(99)
        self.displayVerticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.displayVerticalScrollBar.setObjectName("displayVerticalScrollBar")
        self.gridLayout_2.addWidget(self.displayVerticalScrollBar, 1, 0, 1, 1)
        self.displayHorizontalScrollBar = QtWidgets.QScrollBar(self.gridLayoutWidget)
        self.displayHorizontalScrollBar.setMinimum(0)
        self.displayHorizontalScrollBar.setMaximum(100)
        self.displayHorizontalScrollBar.setPageStep(99)
        self.displayHorizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.displayHorizontalScrollBar.setObjectName("displayHorizontalScrollBar")
        self.gridLayout_2.addWidget(self.displayHorizontalScrollBar, 2, 1, 1, 1)
        self.triggerSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.triggerSlider.setProperty("value", 50)
        self.triggerSlider.setOrientation(QtCore.Qt.Vertical)
        self.triggerSlider.setObjectName("triggerSlider")
        self.gridLayout_2.addWidget(self.triggerSlider, 1, 2, 1, 1)
        self.displayTitle = QtWidgets.QLabel(self.gridLayoutWidget)
        self.displayTitle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayTitle.setObjectName("displayTitle")
        self.gridLayout_2.addWidget(self.displayTitle, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.voltageZoomIn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.voltageZoomIn.setObjectName("voltageZoomIn")
        self.verticalLayout.addWidget(self.voltageZoomIn)
        self.voltageZoomOut = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.voltageZoomOut.setObjectName("voltageZoomOut")
        self.verticalLayout.addWidget(self.voltageZoomOut)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.voltageZoomValue = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.voltageZoomValue.setDecimals(4)
        self.voltageZoomValue.setProperty("value", 0.1)
        self.voltageZoomValue.setObjectName("voltageZoomValue")
        self.horizontalLayout.addWidget(self.voltageZoomValue)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.timeZoomIn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.timeZoomIn.setObjectName("timeZoomIn")
        self.verticalLayout_6.addWidget(self.timeZoomIn)
        self.timeZoomOut = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.timeZoomOut.setObjectName("timeZoomOut")
        self.verticalLayout_6.addWidget(self.timeZoomOut)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.timeZoomValue = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.timeZoomValue.setDecimals(4)
        self.timeZoomValue.setProperty("value", 0.05)
        self.timeZoomValue.setObjectName("timeZoomValue")
        self.horizontalLayout_2.addWidget(self.timeZoomValue)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.rightSliderSelector = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.rightSliderSelector.setObjectName("rightSliderSelector")
        self.rightSliderSelector.addItem("")
        self.rightSliderSelector.addItem("")
        self.rightSliderSelector.addItem("")
        self.horizontalLayout_7.addWidget(self.rightSliderSelector)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.rightSliderValueTitle1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.rightSliderValueTitle1.setObjectName("rightSliderValueTitle1")
        self.horizontalLayout_8.addWidget(self.rightSliderValueTitle1)
        self.rightSliderValueSpinBox1 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.rightSliderValueSpinBox1.setDecimals(4)
        self.rightSliderValueSpinBox1.setMinimum(-9999999.0)
        self.rightSliderValueSpinBox1.setMaximum(999999.0)
        self.rightSliderValueSpinBox1.setSingleStep(0.01)
        self.rightSliderValueSpinBox1.setObjectName("rightSliderValueSpinBox1")
        self.horizontalLayout_8.addWidget(self.rightSliderValueSpinBox1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.rightSliderValueTitle2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.rightSliderValueTitle2.setObjectName("rightSliderValueTitle2")
        self.horizontalLayout_9.addWidget(self.rightSliderValueTitle2)
        self.rightSliderValueSpinBox2 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.rightSliderValueSpinBox2.setDecimals(4)
        self.rightSliderValueSpinBox2.setMinimum(-99999999.0)
        self.rightSliderValueSpinBox2.setMaximum(99999999.0)
        self.rightSliderValueSpinBox2.setSingleStep(0.01)
        self.rightSliderValueSpinBox2.setObjectName("rightSliderValueSpinBox2")
        self.horizontalLayout_9.addWidget(self.rightSliderValueSpinBox2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.sliderVisibilityToggler = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.sliderVisibilityToggler.setObjectName("sliderVisibilityToggler")
        self.verticalLayout_7.addWidget(self.sliderVisibilityToggler)
        self.horizontalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.tabWidget = QtWidgets.QTabWidget(self.bottomPanelSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWidget.setBaseSize(QtCore.QSize(0, 0))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        self.controlTab = QtWidgets.QWidget()
        self.controlTab.setObjectName("controlTab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.controlTab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(self.controlTab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1199, 828))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_3.addWidget(self.pushButton_4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.scrollArea)
        self.tabWidget.addTab(self.controlTab, "")
        self.logTab = QtWidgets.QWidget()
        self.logTab.setObjectName("logTab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.logTab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.logTab)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout_4.addWidget(self.plainTextEdit)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.logTab)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_4.addWidget(self.pushButton_6)
        self.pushButton_5 = QtWidgets.QPushButton(self.logTab)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_4.addWidget(self.pushButton_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.logTab, "")
        self.gridLayout_4.addWidget(self.bottomPanelSplitter, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.leftPanelSplitter, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 17))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionZoom = QtWidgets.QAction(MainWindow)
        self.actionZoom.setObjectName("actionZoom")
        self.actionDebug = QtWidgets.QAction(MainWindow)
        self.actionDebug.setObjectName("actionDebug")
        self.actionToggleConfigPanel = QtWidgets.QAction(MainWindow)
        self.actionToggleConfigPanel.setObjectName("actionToggleConfigPanel")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionOpen_config_file = QtWidgets.QAction(MainWindow)
        self.actionOpen_config_file.setObjectName("actionOpen_config_file")
        self.actionToggleControlPanel = QtWidgets.QAction(MainWindow)
        self.actionToggleControlPanel.setObjectName("actionToggleControlPanel")
        self.menuFile.addAction(self.actionNew)
        self.menuView.addAction(self.actionZoom)
        self.menuOptions.addAction(self.actionPreferences)
        self.menuOptions.addAction(self.actionOpen_config_file)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.toolBar.addAction(self.actionToggleConfigPanel)
        self.toolBar.addAction(self.actionToggleControlPanel)
        self.toolBar.addAction(self.actionDebug)

        self.retranslateUi(MainWindow)
        self.configTab.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.configTab.setTabText(self.configTab.indexOf(self.viewTab), _translate("MainWindow", "View"))
        self.configTab.setTabText(self.configTab.indexOf(self.modelTab), _translate("MainWindow", "Model"))
        self.label_3.setText(_translate("MainWindow", "▼"))
        self.displayTitle.setText(_translate("MainWindow", "Right Slider"))
        self.label_7.setText(_translate("MainWindow", "Y Axis"))
        self.voltageZoomIn.setText(_translate("MainWindow", "Zoom In (+)"))
        self.voltageZoomOut.setText(_translate("MainWindow", "Zoom Out (-)"))
        self.label.setText(_translate("MainWindow", "Step (Volt)"))
        self.label_6.setText(_translate("MainWindow", "X Axis"))
        self.timeZoomIn.setText(_translate("MainWindow", "Zoom In (+)"))
        self.timeZoomOut.setText(_translate("MainWindow", "Zoom Out (-)"))
        self.label_2.setText(_translate("MainWindow", "Step (ms)"))
        self.label_4.setText(_translate("MainWindow", "Right Slider Controls"))
        self.rightSliderSelector.setItemText(0, _translate("MainWindow", "Trigger (Red)"))
        self.rightSliderSelector.setItemText(1, _translate("MainWindow", "Cursor 1"))
        self.rightSliderSelector.setItemText(2, _translate("MainWindow", "Cursor 2"))
        self.rightSliderValueTitle1.setText(_translate("MainWindow", "Value Title 1"))
        self.rightSliderValueTitle2.setText(_translate("MainWindow", "Value Title 2"))
        self.sliderVisibilityToggler.setText(_translate("MainWindow", "Toggle Visibility"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.controlTab), _translate("MainWindow", "Basic Analysis"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Test"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logTab), _translate("MainWindow", "Log"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionZoom.setText(_translate("MainWindow", "Zoom"))
        self.actionDebug.setText(_translate("MainWindow", "Debug"))
        self.actionDebug.setToolTip(_translate("MainWindow", "Debug action"))
        self.actionToggleConfigPanel.setText(_translate("MainWindow", "Config Panel"))
        self.actionToggleConfigPanel.setToolTip(_translate("MainWindow", "Toggle Config Panel"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionOpen_config_file.setText(_translate("MainWindow", "Open config file"))
        self.actionToggleControlPanel.setText(_translate("MainWindow", "Analysis Panel"))
