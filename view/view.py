import logging

from attr import dataclass

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget
from ui.mainwindow import Ui_MainWindow as MainWindow

from .display import OscilloscopeDisplay

logger = logging.getLogger(__name__)


@dataclass
class UIConfig:
    pendingOpTimeoutMs: int = 1000


class OscilloscopeUi(QMainWindow):
    """MPS Oscilloscope's view (GUI)."""
    newModelConfig = pyqtSignal(ModelConfig)

    def __init__(self) -> None:
        """View initializer."""
        super().__init__()

        self.config = UIConfig()
        self.mainwindow, self.display = self._setupUI()
        self.timer = QTimer()
        self._connectSignals()
        self.timer.start(self.config.pendingOpTimeoutMs)

        self._recordSliderValue()

    def _replaceWidget(self, placeholder: QWidget, new: QWidget):
        containing_layout = placeholder.parent().layout()
        containing_layout.replaceWidget(placeholder, new)

    def _recordSliderValue(self):
        self.lastSliderValue = self.mainwindow.triggerSlider.value()

    def updateData(self, data):
        self.display.updateData(data)

    def updateByModelConfig(self, config: ModelConfig):
        self.display.adjustTrigger(config.processor.triggerVolt)

    def _setupUI(self):
        mainwindow = MainWindow()
        mainwindow.setupUi(self)
        display = OscilloscopeDisplay()
        self._replaceWidget(mainwindow.displayPlaceHolder, display)
        return mainwindow, display

    def _applyPendingOps(self):
        sliderStopped = (self.lastSliderValue ==
                         self.mainwindow.triggerSlider.value())
        sliderChanged = (self.display.trigger != self.lastSliderValue)
        if sliderChanged and sliderStopped:
            self.display.adjustTrigger(volt=(self.lastSliderValue - 50) / 100)

    def debugAction(self):
        self.newModelConfig.emit(ModelConfig(
            processor=ProcessorConfig(triggerVolt=0.1)))
        logger.info("Debug action triggered")

    def _connectSignals(self):
        self.mainwindow.actionDebug.triggered.connect(self.debugAction)
        self.mainwindow.triggerSlider.valueChanged.connect(self._recordSliderValue)
        self.timer.timeout.connect(self._applyPendingOps)
