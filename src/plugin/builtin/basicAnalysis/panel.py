from .processor import BasicAnalysisData

from .ui.basicAnalysis import Ui_Form as BasicAnalysis

from PyQt5.QtWidgets import QWidget


class BasicAnalysisPanel:
    def __init__(self) -> None:
        self.uiForm = BasicAnalysis()
        self.widget: BasicAnalysis = QWidget()
        self.uiForm.setupUi(self.widget)

    def getWidget(self) -> QWidget:
        return self.widget

    def updateByData(self, data: BasicAnalysisData):
        self.uiForm.vTopDoubleSpinBox.setValue(data.vTop)
        self.uiForm.vBaseDoubleSpinBox.setValue(data.vBase)
        self.uiForm.vAmplitudeDoubleSpinBox.setValue(data.vAmplitude)
        self.uiForm.vMaxDoubleSpinBox.setValue(data.vMax)
        self.uiForm.vMinDoubleSpinBox.setValue(data.vMin)
        self.uiForm.vPeakToPeakDoubleSpinBox.setValue(data.vPeakToPeak)
        self.uiForm.frameRateDoubleSpinBox.setValue(data.frameRate)
