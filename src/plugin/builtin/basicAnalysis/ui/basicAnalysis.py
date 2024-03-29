# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\plugin\builtin\basicAnalysis\ui\basicAnalysis.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 500)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setTextFormat(QtCore.Qt.MarkdownText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.vTopDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.vTopDoubleSpinBox.setReadOnly(True)
        self.vTopDoubleSpinBox.setDecimals(2)
        self.vTopDoubleSpinBox.setMinimum(-99.0)
        self.vTopDoubleSpinBox.setObjectName("vTopDoubleSpinBox")
        self.horizontalLayout_3.addWidget(self.vTopDoubleSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.vBaseDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.vBaseDoubleSpinBox.setReadOnly(True)
        self.vBaseDoubleSpinBox.setDecimals(2)
        self.vBaseDoubleSpinBox.setMinimum(-100.0)
        self.vBaseDoubleSpinBox.setObjectName("vBaseDoubleSpinBox")
        self.horizontalLayout_4.addWidget(self.vBaseDoubleSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.vAmplitudeDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.vAmplitudeDoubleSpinBox.setReadOnly(True)
        self.vAmplitudeDoubleSpinBox.setDecimals(2)
        self.vAmplitudeDoubleSpinBox.setMinimum(-99.0)
        self.vAmplitudeDoubleSpinBox.setObjectName("vAmplitudeDoubleSpinBox")
        self.horizontalLayout_5.addWidget(self.vAmplitudeDoubleSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_7.addWidget(self.label_8)
        self.vMaxDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.vMaxDoubleSpinBox.setReadOnly(True)
        self.vMaxDoubleSpinBox.setDecimals(2)
        self.vMaxDoubleSpinBox.setMinimum(-99.99)
        self.vMaxDoubleSpinBox.setObjectName("vMaxDoubleSpinBox")
        self.horizontalLayout_7.addWidget(self.vMaxDoubleSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.vMinDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.vMinDoubleSpinBox.setReadOnly(True)
        self.vMinDoubleSpinBox.setDecimals(2)
        self.vMinDoubleSpinBox.setMinimum(-99.99)
        self.vMinDoubleSpinBox.setObjectName("vMinDoubleSpinBox")
        self.horizontalLayout_8.addWidget(self.vMinDoubleSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.vPeakToPeakDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.vPeakToPeakDoubleSpinBox.setReadOnly(True)
        self.vPeakToPeakDoubleSpinBox.setDecimals(2)
        self.vPeakToPeakDoubleSpinBox.setMinimum(-99.99)
        self.vPeakToPeakDoubleSpinBox.setObjectName("vPeakToPeakDoubleSpinBox")
        self.horizontalLayout_6.addWidget(self.vPeakToPeakDoubleSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setTextFormat(QtCore.Qt.MarkdownText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_9.addWidget(self.label_10)
        self.frameRateDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.frameRateDoubleSpinBox.setDecimals(0)
        self.frameRateDoubleSpinBox.setObjectName("frameRateDoubleSpinBox")
        self.horizontalLayout_9.addWidget(self.frameRateDoubleSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "**Waveform Analysis**"))
        self.label_4.setText(_translate("Form", "V_top (40%)"))
        self.label_5.setText(_translate("Form", "V_base (40%)"))
        self.label_6.setText(_translate("Form", "V_amplitude (top - base)"))
        self.label_8.setText(_translate("Form", "V_max"))
        self.label_9.setText(_translate("Form", "V_min"))
        self.label_7.setText(_translate("Form", "V_peak-to-peak"))
        self.label.setText(_translate("Form", "**Oscilloscope Stats**"))
        self.label_10.setText(_translate("Form", "Frame Rate"))
