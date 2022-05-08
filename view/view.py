import logging

from attr import dataclass

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import QMainWindow, QWidget, QSlider
from ui.mainwindow import Ui_MainWindow as MainWindow

from view.display import OscilloscopeDisplay
from view.utils import DelayedSliderWrapper


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
        self.trigger = DelayedSliderWrapper(
            self.mainwindow.triggerSlider)
        self._connectSignals()

    def updateData(self, data):
        self.display.updateData(data)

    def updateByModelConfig(self, config: ModelConfig):
        self.display.adjustTrigger(config.processor.triggerVolt)

    def _setupUI(self):
        def _replaceWidget(placeholder: QWidget, new: QWidget):
            containing_layout = placeholder.parent().layout()
            containing_layout.replaceWidget(placeholder, new)

        mainwindow = MainWindow()
        mainwindow.setupUi(self)
        display = OscilloscopeDisplay()
        _replaceWidget(mainwindow.displayPlaceHolder, display)
        return mainwindow, display

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

    def debugAction(self):
        self.newModelConfig.emit(ModelConfig(
            processor=ProcessorConfig(triggerVolt=0.1)))
        logger.info("Debug action triggered")