from PyQt5.QtCore import QObject, QThread, pyqtSignal
from attr import dataclass

from model.worker import DataWorkerConfig, MPSDataWorker, PostProcessWorker, ProcessorConfig
import logging
from model.defaults import *


logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    dataWorker: DataWorkerConfig = None
    processor: ProcessorConfig = None


class OscilloscopeModel(QObject):
    """MPS Oscilloscope's model."""
    dataReady = pyqtSignal(list)
    reportConfigToModel = pyqtSignal(ModelConfig)

    # Internal signals:
    _configDataWorker = pyqtSignal(DataWorkerConfig)
    _configProcessor = pyqtSignal(ProcessorConfig)

    def __init__(self):
        super().__init__()

        self.config = ModelConfig(
            dataWorker=DataWorkerConfig(
                deviceNumber=DEVICE_NUMBER,
                bufferSize=BUFFER_SIZE,
                MPSParameter=PARAMETER
            ),
            processor=ProcessorConfig(
                triggerVolt=0, timeoutMs=1000 / 60, triggerRetryNum=5)
        )

        self.dataWorker = MPSDataWorker(self.config.dataWorker)
        self.dataWorkerThread = self._moveToThread(self.dataWorker)

        sharedState = self.dataWorker.sharedState

        self.processor = PostProcessWorker(self.config.processor, sharedState)
        self.processorThread = self._moveToThread(self.processor)

        self._connectSignals()
        logger.info("Model inited.")

    def _connectSignals(self):
        self.dataWorkerThread.started.connect(self.dataWorker.start)
        self.processorThread.started.connect(self.processor.start)

        # Signal from workers.
        self.processor.dataReady.connect(
            lambda data: self.dataReady.emit(data))
        self.dataWorker.configUpdated.connect(self._dataWorkerConfigUpdated)
        self.processor.configUpdated.connect(self._processorConfigUpdated)

        # To workers.
        self._configDataWorker.connect(self.dataWorker.updateConfig)
        self._configProcessor.connect(self.processor.updateConfig)

    def _moveToThread(self, object: QObject) -> QThread:
        thread = QThread()
        object.moveToThread(thread)
        return thread

    def _changeTrigger(self):
        self.updateConfig(ModelConfig(
            processor=ProcessorConfig(triggerVolt=0.1)))

    def updateConfig(self, config: ModelConfig):
        if config.dataWorker is not None:
            self._configDataWorker.emit(config.dataWorker)
        if config.processor is not None:
            self._configProcessor.emit(config.processor)

    def _dataWorkerConfigUpdated(self, dataWorkerConfig: DataWorkerConfig):
        self.config.dataWorker = dataWorkerConfig
        self.reportConfigToModel.emit(self.config)

    def _processorConfigUpdated(self, processorConfig: ProcessorConfig):
        self.config.processor = processorConfig
        self.reportConfigToModel.emit(self.config)

    def start(self):
        self.dataWorkerThread.start()
        self.processorThread.start()

        self.reportConfigToModel.emit(self.config)
        logger.info("Worker threads started.")
