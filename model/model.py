from PyQt5.QtCore import QObject, QThread, pyqtSignal
from attr import dataclass

from .worker import DataWorkerConfig, MPSDataWorker, PostProcessWorker, ProcessorConfig, initWorkerGlobalInfo
import logging


logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    dataWorker: DataWorkerConfig = None
    processor: ProcessorConfig = None


class OscilloscopeModel(QObject):
    """MPS Oscilloscope's model."""
    dataReady = pyqtSignal(list)
    configUpdated = pyqtSignal(ModelConfig)

    # Internal signals:
    _configDataWorker = pyqtSignal(DataWorkerConfig)
    _configProcessor = pyqtSignal(ProcessorConfig)

    def __init__(self):
        super().__init__()
        initWorkerGlobalInfo()

        self.config = ModelConfig(
            dataWorker=DataWorkerConfig(),
            processor=ProcessorConfig(triggerVolt=0)
        )

        self.dataWorker = MPSDataWorker()
        self.dataWorkerThread = self._moveToThread(self.dataWorker)

        self.processor = PostProcessWorker(frameRate=60)
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
        self.config.processor = ProcessorConfig(triggerVolt=0.1)
        self._configProcessor.emit(self.config.processor)

    def updateConfig(self, config: ModelConfig):
        if config.dataWorker is not None:
            self._configDataWorker.emit(config.dataWorker)
        if config.processor is not None:
            self._configProcessor.emit(config.processor)

    def _dataWorkerConfigUpdated(self, dataWorkerConfig: DataWorkerConfig):
        self.config.dataWorker = dataWorkerConfig
        self.configUpdated.emit(self.config)

    def _processorConfigUpdated(self, processorConfig: ProcessorConfig):
        self.config.processor = processorConfig
        self.configUpdated.emit(self.config)

    def start(self):
        self.dataWorkerThread.start()
        self.processorThread.start()
        logger.info("Worker threads started.")
