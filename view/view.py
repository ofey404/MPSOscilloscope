import logging

from attr import dataclass

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import QMainWindow, QWidget, QSlider
from ui.mainwindow import Ui_MainWindow as MainWindow

from .display import OscilloscopeDisplay

logger = logging.getLogger(__name__)


@dataclass
class UIConfig:
    pendingOpTimeoutMs: int = 1000


class DelayedSliderWrapper(QObject):
    stoppedForTimeout = pyqtSignal(int)

    def __init__(self, slider: QSlider, timeoutMs: int = 100):
        super().__init__()
        self.slider = slider
        self.timer = QTimer()
        self.moving = False
        self._connectSignals()
        self.lastSliderValue = self.slider.value()
        self.timer.start(timeoutMs)

    def _connectSignals(self):
        self.timer.timeout.connect(self._checkSliderStopped)

    def _checkSliderStopped(self):
        if self.moving:
            if self.lastSliderValue == self.slider.value():
                self.moving = False
                self.stoppedForTimeout.emit(self.lastSliderValue)
        else:
            if self.lastSliderValue != self.slider.value():
                self.moving = True
        self.lastSliderValue = self.slider.value()


class OscilloscopeUi(QMainWindow):
    """MPS Oscilloscope's view (GUI)."""
    newModelConfig = pyqtSignal(ModelConfig)

    def __init__(self) -> None:
        """View initializer."""
        super().__init__()

        self.config = UIConfig()
        self.mainwindow, self.display = self._setupUI()
        self.trigger = DelayedSliderWrapper(
            self.mainwindow.triggerSlider)
        self._connectSignals()

    def _replaceWidget(self, placeholder: QWidget, new: QWidget):
        containing_layout = placeholder.parent().layout()
        containing_layout.replaceWidget(placeholder, new)

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

    def debugAction(self):
        self.newModelConfig.emit(ModelConfig(
            processor=ProcessorConfig(triggerVolt=0.1)))
        logger.info("Debug action triggered")

    def adjustTrigger(self):
        triggerVolt = (self.trigger.slider.value() - 50) / 100
        self.newModelConfig.emit(ModelConfig(
            processor=ProcessorConfig(triggerVolt=triggerVolt)))
        self.display.adjustTrigger(volt=triggerVolt)

    def _connectSignals(self):
        self.mainwindow.actionDebug.triggered.connect(self.debugAction)
        self.trigger.slider.valueChanged.connect(
            lambda value: self.display.adjustNextTriggerIndicator(
                (value - 50) / 100)
        )
        self.trigger.stoppedForTimeout.connect(self.adjustTrigger)
