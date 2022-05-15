import logging

from attr import dataclass
import mps060602

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout
from ui.mainwindow import Ui_MainWindow as MainWindow

from view.display import OscilloscopeDisplay, DisplayConfig
from view.internalControllers.configPanelControl import ConfigPanelControl
from view.internalControllers.displayZoomControl import DisplayZoomControl
from view.utils import ScrollBarStepConverter, replaceWidget
from view.internalControllers.rightSliderControl import RightSliderControl

from plugin.basicAnalysis.ui.basicAnalysis import Ui_Form as BasicAnalysis


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
        self._setupUI()

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
            zoomResetButtonX=self.mainwindow.timeZoomReset,
            zoomResetButtonY=self.mainwindow.voltageZoomReset,
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

        self.configPanelControl = ConfigPanelControl(
            updateConfigButton=self.mainwindow.updateConfigButton,
            deviceNumberSpinBox=self.mainwindow.deviceNumberSpinBox,
            bufferSizeSpinBox=self.mainwindow.bufferSizeSpinBox,
            inputChannelComboBox=self.mainwindow.inputChannelComboBox,
            ADCRangeComboBox=self.mainwindow.ADCRangeComboBox,
            windowTimeDoubleSpinBox=self.mainwindow.windowTimeDoubleSpinBox,
            sampleRateSpinBox=self.mainwindow.sampleRateSpinBox,
            frameRateSpinBox=self.mainwindow.frameRateSpinBox,
            retryTriggerSpinBox=self.mainwindow.retryTriggerSpinBox,
            triggerSelectionComboBox=self.mainwindow.triggerSelectionComboBox,
        )

        self._connectSignals()

    def updateData(self, data):
        self.display.updateData(data)

    def updateByModelConfig(self, config: ModelConfig):
        gain = config.dataWorker.Gain
        if gain == mps060602.PGAAmpRate.range_10V:
            lim = (-10, 10)
        if gain == mps060602.PGAAmpRate.range_5V:
            lim = (-5, 5)
        if gain == mps060602.PGAAmpRate.range_2V:
            lim = (-2, 2)
        if gain == mps060602.PGAAmpRate.range_1V:
            lim = (-1, 1)
        self.display.updateVoltLim(lim)
        self.displayZoomControl.recalculateDefaultZoomStep()
        self.displayZoomControl.repaintAllScrollBar()

        self.display.updateTimeLim(
            config.dataWorker.bufferSize, config.dataWorker.ADSampleRate)

        self.display.updateTrigger(config.processor.triggerVolt)

    def show(self):
        super().show()
        self._adjustPanel()

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _setupUI(self):
        self.mainwindow = MainWindow()
        self.mainwindow.setupUi(self)
        self.display = OscilloscopeDisplay(DisplayConfig())
        replaceWidget(self.mainwindow.displayPlaceHolder, self.display)
        self._setupAnalysisPanel()

    def _setupAnalysisPanel(self):
        analysisPanel = BasicAnalysis()
        self.basicAnalysisPanel: BasicAnalysis = QWidget()
        analysisPanel.setupUi(self.basicAnalysisPanel)

        replaceWidget(
            self.mainwindow.basicAnalysisPlaceHolder,
            self.basicAnalysisPanel
        )

    def _connectSignals(self):
        self.mainwindow.actionDebug.triggered.connect(self.debugAction)
        self.mainwindow.actionToggleConfigPanel.triggered.connect(
            self._toggleLeftPanel)
        self.mainwindow.actionToggleControlPanel.triggered.connect(
            self._toggleBottomPanel)

        self.rightSliderControl.triggerSelected.connect(
            self._adjustTrigger)

        self.configPanelControl.configUpdated.connect(self._requestModelConfig)

    def _adjustTrigger(self, triggerVolt):
        self.newModelConfig.emit(ModelConfig(
            processor=ProcessorConfig(triggerVolt=triggerVolt)))

    def _requestModelConfig(self, config: ModelConfig):
        self.newModelConfig.emit(config)

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
        logger.info("Debug action triggered")

    def _adjustPanel(self):
        screenBottomPos = self.mainwindow.bottomPanelSplitter.getRange(1)[
            1]
        self.mainwindow.bottomPanelSplitter.moveSplitter(
            screenBottomPos - 500, 1)

        self.mainwindow.leftPanelSplitter.moveSplitter(300, 1)
