import logging

from attr import dataclass

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QSplitter
from ui.mainwindow import Ui_MainWindow as MainWindow

from view.display import OscilloscopeDisplay
from view.utils import DelayedSliderWrapper


logger = logging.getLogger(__name__)


@dataclass
class UIConfig:
    pendingOpTimeoutMs: int = 1000
    leftPanelVisible: bool = True
    bottomPanelVisible: bool = True


class OscilloscopeUi(QMainWindow):
    """MPS Oscilloscope's view (GUI)."""
    newModelConfig = pyqtSignal(ModelConfig)

    def __init__(self) -> None:
        """View initializer."""
        super().__init__()

        self.config = UIConfig()
        self.mainwindow, self.display = self._setupUI()
        self.savedUiState = dict()
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
        self.mainwindow.actionToggleConfigPanel.triggered.connect(
            self._toggleLeftPanel)
        self.mainwindow.actionToggleControlPanel.triggered.connect(
            self._toggleBottomPanel)
        self.trigger.slider.valueChanged.connect(
            lambda value: self.display.adjustNextTriggerIndicator(
                (value - 50) / 100)
        )
        self.trigger.stoppedForTimeout.connect(self.adjustTrigger)

    def _toggleLeftPanel(self):
        if self.config.leftPanelVisible:
            self.savedUiState["leftPanel"] = self.mainwindow.leftPanelSplitter.saveState(
            )
            self.mainwindow.leftPanelSplitter.moveSplitter(0, 1)
            self.config.leftPanelVisible = False
        else:
            state = self.savedUiState.get("leftPanel")
            if state:
                self.mainwindow.leftPanelSplitter.restoreState(state)
            else:
                self.mainwindow.leftPanelSplitter.moveSplitter(256, 1)
            self.config.leftPanelVisible = True

    def _toggleBottomPanel(self):
        if self.config.bottomPanelVisible:
            self.savedUiState["bottomPanel"] = self.mainwindow.bottomPanelSplitter.saveState(
            )
            screenBottomPos = self.mainwindow.bottomPanelSplitter.getRange(1)[
                1]
            self.mainwindow.bottomPanelSplitter.moveSplitter(
                screenBottomPos, 1)
            self.config.bottomPanelVisible = False
        else:
            state = self.savedUiState.get("bottomPanel")
            if state:
                self.mainwindow.bottomPanelSplitter.restoreState(state)
            else:
                self.mainwindow.bottomPanelSplitter.moveSplitter(512, 1)
            self.config.bottomPanelVisible = True

    def debugAction(self):
        print(self.mainwindow.leftPanelSplitter.saveState())
        logger.info("Debug action triggered")
