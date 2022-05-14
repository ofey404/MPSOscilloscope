import logging
from model.model import ModelConfig
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton, QDoubleSpinBox

from model.worker import DataWorkerConfig, MPSDataWorker, ProcessorConfig
import mps060602
from view.utils import showError


logger = logging.getLogger(__name__)


class ConfigError(Exception):
    pass


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
                 frameRateComboBox: QComboBox,
                 retryTriggerComboBox: QComboBox,
                 ) -> None:
        super().__init__()

        self.updateConfigButton = updateConfigButton
        self.deviceNumberSpinBox = deviceNumberSpinBox
        self.bufferSizeSpinBox = bufferSizeSpinBox
        self.inputChannelComboBox = inputChannelComboBox
        self.ADCRangeComboBox = ADCRangeComboBox
        self.windowTimeDoubleSpinBox = windowTimeDoubleSpinBox
        self.sampleRateSpinBox = sampleRateSpinBox
        self.frameRateComboBox = frameRateComboBox
        self.retryTriggerComboBox = retryTriggerComboBox

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
                processor=ProcessorConfig()
            )
            self.configUpdated.emit(config)
            logger.debug("Try to update configuration by panel.")
        except ConfigError as e:
            showError(str(e))

    def updateCalculatedFields(self):
        self._updateTimeRange()

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _connectSignals(self):
        self.updateConfigButton.clicked.connect(self.updateConfig)
        self.bufferSizeSpinBox.valueChanged.connect(self._updateTimeRange)
        self.sampleRateSpinBox.valueChanged.connect(self._updateTimeRange)

    def _deviceNumber(self):
        return self.deviceNumberSpinBox.value()

    def _inputChannel(self):
        text = self.inputChannelComboBox.currentText()
        if text == "In 1":
            return mps060602.ADChannelMode.in1
        if text == "In 2":
            return mps060602.ADChannelMode.in2
        if text == "In 1 & 2":
            return mps060602.ADChannelMode.in1_and_2
        raise ConfigError(f"Invalid Input Channel {text}.")

    def _ADCRange(self):
        text = self.ADCRangeComboBox.currentText()
        if text == "10 V":
            return mps060602.PGAAmpRate.range_10V
        if text == "5 V":
            return mps060602.PGAAmpRate.range_5V
        if text == "2 V":
            return mps060602.PGAAmpRate.range_2V
        if text == "1 V":
            return mps060602.PGAAmpRate.range_1V
        raise ConfigError(f"Invalid ADC Range {text}.")

    def _bufferSize(self):
        return self.bufferSizeSpinBox.value()

    def _sampleRate(self):
        return self.sampleRateSpinBox.value()

    def _updateTimeRange(self):
        timeRangeMs = 1 / self._sampleRate() * self._bufferSize() * 1000 / 2
        self.windowTimeDoubleSpinBox.setValue(timeRangeMs)
