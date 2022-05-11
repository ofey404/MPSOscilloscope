import logging

from attr import dataclass

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
from ui.mainwindow import Ui_MainWindow as MainWindow

from view.display import OscilloscopeDisplay, DisplayConfig
from view.internalControllers.displayZoomControl import DisplayZoomControl
from view.utils import ScrollBarStepConverter
from view.internalControllers.rightSliderControl import RightSliderControl


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

        self.scrollBarConverter = ScrollBarStepConverter()

        self.displayZoomControl = DisplayZoomControl(
            display=self.display,
            scrollBarX=self.mainwindow.displayHorizontalScrollBar,
            scrollBarY=self.mainwindow.displayVerticalScrollBar,
            zoomSpinBoxX=self.mainwindow.timeZoomValue,
            zoomInButtonX=self.mainwindow.timeZoomIn,
            zoomOutButtonX=self.mainwindow.timeZoomOut,
            zoomSpinBoxY=self.mainwindow.voltageZoomValue,
            zoomInButtonY=self.mainwindow.voltageZoomIn,
            zoomOutButtonY=self.mainwindow.voltageZoomOut,
        )

        self.rightSliderControl = RightSliderControl(
            display=self.display,
            slider=self.mainwindow.triggerSlider,
            sliderSelector=self.mainwindow.rightSliderSelector,
            sliderVisibilityToggler=self.mainwindow.sliderVisibilityToggler,
            valueSpinBox1=self.mainwindow.rightSliderValueSpinBox1,
            valueSpinBox2=self.mainwindow.rightSliderValueSpinBox2,
            valueTitle1=self.mainwindow.rightSliderValueTitle1,
            valueTitle2=self.mainwindow.rightSliderValueTitle2,
        )

        self._connectSignals()

    def updateData(self, data):
        self.display.updateData(data)

    def updateByModelConfig(self, config: ModelConfig):
        self.display.updateTrigger(config.processor.triggerVolt)

    def adjustTrigger(self, triggerVolt):
        self.newModelConfig.emit(ModelConfig(
            processor=ProcessorConfig(triggerVolt=triggerVolt)))

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _setupUI(self):
        def _replaceWidget(placeholder: QWidget, new: QWidget):
            containing_layout = placeholder.parent().layout()
            containing_layout.replaceWidget(placeholder, new)

        mainwindow = MainWindow()
        mainwindow.setupUi(self)
        display = OscilloscopeDisplay(DisplayConfig())
        _replaceWidget(mainwindow.displayPlaceHolder, display)

        return mainwindow, display

    def _connectSignals(self):
        self.mainwindow.actionDebug.triggered.connect(self.debugAction)
        self.mainwindow.actionToggleConfigPanel.triggered.connect(
            self._toggleLeftPanel)
        self.mainwindow.actionToggleControlPanel.triggered.connect(
            self._toggleBottomPanel)

        self.rightSliderControl.triggerSelected.connect(
            self.adjustTrigger)

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

    # FIXME: set bottom panel size here, an temporary solution.
    #        Call after view.show()
    def _temporaryUiFix(self):
        screenBottomPos = self.mainwindow.bottomPanelSplitter.getRange(1)[
            1]
        self.mainwindow.bottomPanelSplitter.moveSplitter(
            screenBottomPos - 500, 1)

    def debugAction(self):
        logger.info("Debug action triggered")
        self.display.toggleTriggerLine()
