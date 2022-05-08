import logging

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
from ui.mainwindow import Ui_MainWindow as MainWindow

from .display import OscilloscopeDisplay

logger = logging.getLogger(__name__)


class OscilloscopeUi(QMainWindow):
    """MPS Oscilloscope's view (GUI)."""
    newModelConfig = pyqtSignal(ModelConfig)

    def __init__(self) -> None:
        """View initializer."""
        super().__init__()
        self.mainwindow = MainWindow()
        self.mainwindow.setupUi(self)

        self.display = OscilloscopeDisplay()
        self._replaceWidget(self.mainwindow.displayPlaceHolder, self.display)
        self._connectSignals()

    def _replaceWidget(self, placeholder: QWidget, new: QWidget):
        containing_layout = placeholder.parent().layout()
        containing_layout.replaceWidget(placeholder, new)

    def updateData(self, data):
        self.display.updateData(data)

    def updateByModelConfig(self, config: ModelConfig):
        self.display.adjustTrigger(config.processor.triggerVolt)

    def debugAction(self):
        self.newModelConfig.emit(ModelConfig(
            processor=ProcessorConfig(triggerVolt=0.1)))
        logger.info("Debug action triggered")

    def _connectSignals(self):
        self.mainwindow.actionDebug.triggered.connect(self.debugAction)
