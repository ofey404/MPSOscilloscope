from .processor import FFTData
from PyQt5.QtWidgets import QWidget
from .ui.fft import Ui_Form as FFT


class FFTPanel:
    def __init__(self) -> None:
        self.uiForm = FFT()
        self.widget: FFT = QWidget()
        self.uiForm.setupUi(self.widget)

    def getWidget(self) -> QWidget:
        return self.widget

    def updateByData(self, data: FFTData):
        self.uiForm.vTopDoubleSpinBox.setValue(data.vTop)
