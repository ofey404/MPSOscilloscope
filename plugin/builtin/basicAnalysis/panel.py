from plugin.helpers.pluginType import PluginConfigType
from .ui.basicAnalysis import Ui_Form as BasicAnalysis

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class BasicAnalysisPanel:
    def __init__(self) -> None:
        self.uiForm = BasicAnalysis()
        self.widget: BasicAnalysis = QWidget()
        self.uiForm.setupUi(self.widget)

    def getWidget(self) -> QWidget:
        return self.widget

    def getSignalUiUpdated(self) -> pyqtSignal(PluginConfigType):
        raise NotImplementedError()
