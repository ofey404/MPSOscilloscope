import logging

import mps060602
from dataclasses import dataclass
from controller.pluginManager import PluginStatus

from model import ModelConfig, ProcessorConfig
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog
from plugin.helpers.pluginType import PluginType
from ui.mainwindow import Ui_MainWindow as MainWindow

from view.display import OscilloscopeDisplay, DisplayConfig
from view.internalControllers.pluginPanelControl import PluginPanelControl
from view.internalControllers.configPanelControl import ConfigPanelControl
from view.internalControllers.displayZoomControl import DisplayZoomControl
from view.utils import ScrollBarStepConverter, replaceWidget
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
    togglePlugins = pyqtSignal(PluginStatus)

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
            postProcessorListWidget=self.mainwindow.postProcessorListWidget,
            postProcessorOrderUpButton=self.mainwindow.postProcessorOrderUpButton,
            postProcessorOrderDownButton=self.mainwindow.postProcessorOrderDownButton,
        )

        self.pluginPanelControl = PluginPanelControl(
            updatePluginButton=self.mainwindow.updatePluginButton,
            configFilePathLineEdit=self.mainwindow.configFilePathLineEdit,
            enabledPluginsListWidget=self.mainwindow.enabledPluginsListWidget,
            allAvailablePluginsListWidget=self.mainwindow.allAvailablePluginsListWidget,
            pluginAddButton=self.mainwindow.pluginAddButton,
            pluginRemoveButton=self.mainwindow.pluginRemoveButton,
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
        self.configPanelControl.respondToModelConfig(config)

    def show(self):
        super().show()
        self._adjustPanel()

    def updateByPluginManager(self, pluginStatus: PluginStatus):
        self.pluginPanelControl.respondToPluginStatus(pluginStatus)
        self._updateAllAnalysisPanel(pluginStatus)
        logger.info("View updated by pluginManager.")

    # ============== DEBUG ACTION ================================
    def debugAction(self):
        logger.info("Debug action triggered")

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _setupUI(self):
        self.mainwindow = MainWindow()
        self.mainwindow.setupUi(self)
        self.display = OscilloscopeDisplay(DisplayConfig())
        replaceWidget(self.mainwindow.displayPlaceHolder, self.display)
        self.mainwindow.analysisTabWidget.removeTab(0)

    def _updateAllAnalysisPanel(self, pluginStatus: PluginStatus):
        for i in range(len(pluginStatus.allPlugins)):
            plugin, enabled = pluginStatus.allPlugins[i], pluginStatus.enabled[i]
            if enabled:
                pluginStatus.controlTab[i] = self._addAnalysisPanel(plugin)
            else:
                controlTab = pluginStatus.controlTab[i]
                if controlTab is not None:
                    self._removeAnalysisPanel(controlTab)

    def _removeAnalysisPanel(self, controlTab: QWidget):
        analysisTabWidget = self.mainwindow.analysisTabWidget
        tabIndex = analysisTabWidget.indexOf(controlTab)
        analysisTabWidget.removeTab(tabIndex)
        logger.info("Removed widget from plugin panel.")

    def _addAnalysisPanel(self, plugin: PluginType):
        if plugin.getPanel() is None:
            logger.debug(f"No panel, plugin {plugin}")
            return
        content = plugin.getPanel().getWidget()
        tabTitle = plugin.getMetadata().tab_title
        id = plugin.getMetadata().id
        _translate = QtCore.QCoreApplication.translate
        analysisTabWidget = self.mainwindow.analysisTabWidget

        controlTab = QtWidgets.QWidget()
        controlTab.setObjectName("controlTab"+id)

        horizontalLayout = QtWidgets.QHBoxLayout(controlTab)
        horizontalLayout.setObjectName("horizontalLayout"+id)
        scrollArea = QtWidgets.QScrollArea(controlTab)
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName("scrollArea"+id)
        scrollAreaWidgetContents = QtWidgets.QWidget()
        scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1247, 668))
        scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents"+id)
        verticalLayout = QtWidgets.QVBoxLayout(scrollAreaWidgetContents)
        verticalLayout.setObjectName("verticalLayout"+id)
        verticalLayout.addWidget(content)
        scrollArea.setWidget(scrollAreaWidgetContents)
        horizontalLayout.addWidget(scrollArea)
        analysisTabWidget.addTab(controlTab, "")
        analysisTabWidget.setTabText(analysisTabWidget.indexOf(
            controlTab), _translate("MainWindow", tabTitle))

        logger.info("Added widget to plugin panel.")
        return controlTab

    def _removeWidgetFromPanel(self, widget: QWidget):
        ...

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

    def _adjustPanel(self):
        screenBottomPos = self.mainwindow.bottomPanelSplitter.getRange(1)[
            1]
        self.mainwindow.bottomPanelSplitter.moveSplitter(
            screenBottomPos - 500, 1)

        self.mainwindow.leftPanelSplitter.moveSplitter(400, 1)
