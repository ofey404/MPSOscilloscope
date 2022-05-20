import logging
import typing

from tomlkit import item
from model.model import ModelConfig
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton, QDoubleSpinBox, QListWidget
import PyQt5.QtCore

from model.trigger import EdgeTrigger

from model.worker import DataWorkerConfig, MPSDataWorker, ProcessorConfig
import mps060602
from plugin.helpers.pluginType import ProcessorType
from view.utils import showError


logger = logging.getLogger(__name__)


class ConfigError(Exception):
    pass


_TRIGGER_MAP = {
    "Up Edge": EdgeTrigger(upEdge=True),
    "Down Edge": EdgeTrigger(upEdge=False),
}

_ADC_RANGE_MAP = {
    "10 V": mps060602.PGAAmpRate.range_10V,
    "5 V": mps060602.PGAAmpRate.range_5V,
    "2 V": mps060602.PGAAmpRate.range_2V,
    "1 V": mps060602.PGAAmpRate.range_1V,
}

_INPUT_CHANNEL_MAP = {
    "In 1": mps060602.ADChannelMode.in1,
    "In 2": mps060602.ADChannelMode.in2,
    "In 1 & 2": mps060602.ADChannelMode.in1_and_2,
}


class ConfigPanelControl(QObject):
    configUpdated = pyqtSignal(ModelConfig)

    def __init__(self,
                 updateConfigButton: QPushButton,
                 deviceNumberSpinBox: QSpinBox,
                 bufferSizeSpinBox: QSpinBox,
                 inputChannelComboBox: QComboBox,
                 ADCRangeComboBox: QComboBox,
                 windowTimeDoubleSpinBox: QDoubleSpinBox,
                 sampleRateSpinBox: QSpinBox,
                 frameRateSpinBox: QSpinBox,
                 retryTriggerSpinBox: QSpinBox,
                 triggerSelectionComboBox: QComboBox,
                 postProcessorListWidget: QListWidget,
                 postProcessorOrderUpButton: QPushButton,
                 postProcessorOrderDownButton: QPushButton,
                 ) -> None:
        super().__init__()

        self.updateConfigButton = updateConfigButton
        self.deviceNumberSpinBox = deviceNumberSpinBox
        self.bufferSizeSpinBox = bufferSizeSpinBox
        self.inputChannelComboBox = inputChannelComboBox
        self.ADCRangeComboBox = ADCRangeComboBox
        self.windowTimeDoubleSpinBox = windowTimeDoubleSpinBox
        self.sampleRateSpinBox = sampleRateSpinBox
        self.frameRateSpinBox = frameRateSpinBox
        self.retryTriggerSpinBox = retryTriggerSpinBox
        self.triggerSelectionComboBox = triggerSelectionComboBox

        self.postProcessorListWidget = postProcessorListWidget
        self.postProcessorOrderUpButton = postProcessorOrderUpButton
        self.postProcessorOrderDownButton = postProcessorOrderDownButton

        self.cachedProcessorList = []

        self._connectSignals()
        self.updateCalculatedFields()

    def updateConfig(self):
        try:
            config = ModelConfig(
                dataWorker=DataWorkerConfig(
                    deviceNumber=self._deviceNumber(),
                    bufferSize=self._bufferSize(),
                    Gain=self._ADCRange(),
                    ADChannel=self._inputChannel(),
                    ADSampleRate=self._sampleRate(),
                ),
                processor=ProcessorConfig(
                    timeoutMs=self._timeOutMs(),
                    triggerRetryNum=self._triggerRetryNum(),
                    trigger=self._triggerType(),
                    # FIXME: Model and View sticking together so ugly!
                    allPluginProcessor=self._processors(),
                )
            )
            self.configUpdated.emit(config)
            logger.debug("Try to update configuration by panel.")
        except ConfigError as e:
            showError("ConfigError", str(e))

    def respondToModelConfig(self, config: ModelConfig):
        self._deviceNumber(config.dataWorker.deviceNumber)

        if config.processor.allPluginProcessor is not None:
            pList = config.processor.allPluginProcessor
        else:
            pList = []
        self._syncProcessorList(pList)

    def updateCalculatedFields(self):
        self._updateTimeRange()

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _connectSignals(self):
        self.updateConfigButton.clicked.connect(self.updateConfig)
        self.bufferSizeSpinBox.valueChanged.connect(self._updateTimeRange)
        self.sampleRateSpinBox.valueChanged.connect(self._updateTimeRange)
        self.postProcessorOrderUpButton.clicked.connect(
            self._moveSelectedProcessorUp)
        self.postProcessorOrderDownButton.clicked.connect(
            self._moveSelectedProcessorDown)

    def _processors(self):
        def findItemFromText(itemText: str, pList: typing.List[ProcessorType]):
            for p in pList:
                if p.displayName() == itemText:
                    return p
            raise Exception()
        # FIXME: Super ugly!!! Lift this logic out to controller.
        lw = self.postProcessorListWidget

        allPluginProcessor = []
        for i in range(lw.count()):
            itemText = lw.item(i).text()
            allPluginProcessor.append(
                findItemFromText(itemText, self.cachedProcessorList)
            )
        return allPluginProcessor

    def _syncProcessorList(self, pList: typing.List[ProcessorType]):
        # Sync saved processor list.
        self.cachedProcessorList = pList

        # Sync display.
        allNames = [p.displayName() for p in pList]
        lw = self.postProcessorListWidget
        for name in allNames:
            if not lw.findItems(name, PyQt5.QtCore.Qt.MatchFlag.MatchExactly):
                lw.addItem(name)
        for i in range(lw.count()):
            item = lw.item(i)
            if item is not None:
                itemText = item.text()
                if itemText not in allNames:
                    lw.takeItem(i)

    def _firstSelectedIndex(self):
        s = self.postProcessorListWidget.selectedIndexes()
        if len(s) > 0:
            return s[0]
        return None

    def _moveSelectedProcessorUp(self):
        lw = self.postProcessorListWidget
        currentRow = lw.currentRow()
        currentItem = lw.takeItem(currentRow)
        lw.insertItem(currentRow - 1, currentItem)
        logger.info("Moved processor up.")

    def _moveSelectedProcessorDown(self):
        lw = self.postProcessorListWidget
        currentRow = lw.currentRow()
        currentItem = lw.takeItem(currentRow)
        lw.insertItem(currentRow+1, currentItem)
        logger.info("Moved processor down.")

    def _deviceNumber(self, val: int = None):
        if val is not None:
            self.deviceNumberSpinBox.setValue(val)
        return self.deviceNumberSpinBox.value()

    def _inputChannel(self):
        text = self.inputChannelComboBox.currentText()
        try:
            return _INPUT_CHANNEL_MAP[text]
        except KeyError:
            raise ConfigError(f"Invalid Input Channel {text}.")

    def _ADCRange(self):
        text = self.ADCRangeComboBox.currentText()
        try:
            return _ADC_RANGE_MAP[text]
        except KeyError:
            raise ConfigError(f"Invalid ADC Range {text}.")

    def _bufferSize(self):
        return self.bufferSizeSpinBox.value()

    def _sampleRate(self):
        return self.sampleRateSpinBox.value()

    def _updateTimeRange(self):
        timeRangeMs = 1 / self._sampleRate() * self._bufferSize() * 1000 / 2
        self.windowTimeDoubleSpinBox.setValue(timeRangeMs)

    def _timeOutMs(self):
        return 1000 / self.frameRateSpinBox.value()

    def _triggerRetryNum(self):
        return self.retryTriggerSpinBox.value()

    def _triggerType(self):
        return _TRIGGER_MAP[self.triggerSelectionComboBox.currentText()]
