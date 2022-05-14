from model.model import ModelConfig
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QComboBox, QSpinBox, QPushButton

from model.worker import DataWorkerConfig, MPSDataWorker, ProcessorConfig
import mps060602


class ConfigPanelControl(QObject):
    configUpdated = pyqtSignal(ModelConfig)

    def __init__(self,
                 updateConfigButton: QPushButton,
                 deviceNumberSpinBox: QSpinBox,
                 bufferSizeComboBox: QComboBox,
                 inputChannelComboBox: QComboBox,
                 ADCRangeComboBox: QComboBox,
                 sampleRateComboBox: QComboBox,
                 frameRateComboBox: QComboBox,
                 retryTriggerComboBox: QComboBox,
                 ) -> None:
        super().__init__()

        self.updateConfigButton = updateConfigButton
        self.deviceNumberSpinBox = deviceNumberSpinBox
        self.bufferSizeComboBox = bufferSizeComboBox
        self.inputChannelComboBox = inputChannelComboBox
        self.ADCRangeComboBox = ADCRangeComboBox
        self.sampleRateComboBox = sampleRateComboBox
        self.frameRateComboBox = frameRateComboBox
        self.retryTriggerComboBox = retryTriggerComboBox

    def _connectSignals(self):
        self.updateConfigButton.clicked.connect(self.updateConfig)

    def updateConfig(self):
        config = ModelConfig(
            dataWorker=DataWorkerConfig(
                # MPSParameter=
                ),
            processor=ProcessorConfig()
        )
        self.configUpdated.emit(config)

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def getADCRange(self):
        return mps060602.PGAAmpRate.range_1V
