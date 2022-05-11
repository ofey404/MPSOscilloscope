import logging

from attr import dataclass

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QSplitter
from ui.mainwindow import Ui_MainWindow as MainWindow

from view.display import OscilloscopeDisplay, DisplayConfig
from view.utils import DelayedSliderWrapper, ScrollBarStepConverter


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
        self._repaintAllScrollBar()

        self.trigger = DelayedSliderWrapper(
            self.mainwindow.triggerSlider)
        self._connectSignals()

    def updateData(self, data):
        self.display.updateData(data)

    def updateByModelConfig(self, config: ModelConfig):
        self.display.updateTrigger(config.processor.triggerVolt)

    def adjustTrigger(self):
        triggerVolt = (self.trigger.slider.value() - 50) / 100
        self.newModelConfig.emit(ModelConfig(
            processor=ProcessorConfig(triggerVolt=triggerVolt)))
        self.display.updateTrigger(volt=triggerVolt)

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
        self.trigger.slider.valueChanged.connect(
            lambda value: self.display.updateNextTriggerIndicator(
                (value - 50) / 100)
        )
        self.trigger.stoppedForTimeout.connect(self.adjustTrigger)

        # Zoom on Y.
        self.mainwindow.voltageZoomIn.clicked.connect(self._zoomInYBySpinBox)
        self.mainwindow.voltageZoomOut.clicked.connect(self._zoomOutYBySpinBox)

        # Zoom on X.
        self.mainwindow.timeZoomIn.clicked.connect(self._zoomInXBySpinBox)
        self.mainwindow.timeZoomOut.clicked.connect(self._zoomOutXBySpinBox)
        self.mainwindow.displayHorizontalScrollBar.valueChanged.connect(lambda i:
            self.display.scrollToX(self.scrollBarConverter.intStepValueToFloat(i, self.display.config.maxXLim)))

        self.mainwindow.displayVerticalScrollBar.valueChanged.connect(lambda i:
            self.display.scrollToY(self.scrollBarConverter.intStepValueToFloat(i, self.display.config.maxYLim)))

    def _zoomInYBySpinBox(self):
        self._zoomYBySpinBox(zoomIn=True)

    def _zoomOutYBySpinBox(self):
        self._zoomYBySpinBox(zoomIn=False)

    def _zoomInXBySpinBox(self):
        self._zoomXBySpinBox(zoomIn=True)

    def _zoomOutXBySpinBox(self):
        self._zoomXBySpinBox(zoomIn=False)

    def _zoomYBySpinBox(self, zoomIn: bool):
        value = self.mainwindow.voltageZoomValue.value()
        if not zoomIn:
            value = - value
        self.display.zoomY(value)
        self._repaintAllScrollBar()

    def _zoomXBySpinBox(self, zoomIn: bool):
        value = self.mainwindow.timeZoomValue.value()
        if not zoomIn:
            value = - value
        self.display.zoomX(value)
        self._repaintAllScrollBar()

        logger.info(f"Zoom in on X axis by {value}.")

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

    def _repaintAllScrollBar(self):
        def rawRepaint(bar, lim, maxLim, value):
            pageStep = lim[1] - lim[0]
            bar.setMinimum(maxLim[0])
            bar.setMaximum(maxLim[1]-pageStep)
            bar.setPageStep(pageStep)
            bar.setValue(value)

        def convertToFixedIntAndPaint(bar, lim, maxLim):
            lim, maxLim = self.scrollBarConverter.limFloatToInt(lim, maxLim)
            rawRepaint(
                bar, lim, maxLim, value=lim[0]
            )

        convertToFixedIntAndPaint(
            bar=self.mainwindow.displayHorizontalScrollBar,
            lim=self.display.xlim(),
            maxLim=self.display.config.maxXLim,
        )

        convertToFixedIntAndPaint(
            bar=self.mainwindow.displayVerticalScrollBar,
            lim=self.display.ylim(),
            maxLim=self.display.config.maxYLim,
        )

    # FIXME: set bottom panel size here, an temporary solution.
    #        Call it after view.show()
    def _temporaryUiFix(self):
        screenBottomPos = self.mainwindow.bottomPanelSplitter.getRange(1)[
            1]
        self.mainwindow.bottomPanelSplitter.moveSplitter(
            screenBottomPos - 500, 1)

    def debugAction(self):
        logger.info("Debug action triggered")
