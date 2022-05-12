from ctypes import c_ushort
import logging
import typing
from dataclasses import dataclass

from model.trigger import EdgeTrigger

from mps060602 import MPS060602, ADChannelMode, MPS060602Para, PGAAmpRate
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from utils import Pool, LeakQueue


logger = logging.getLogger(__name__)


class DataBlock:
    def __init__(self, bufferSize) -> None:
        self.buffer = (c_ushort * bufferSize)()


@dataclass
class DataWorkerConfig:
    deviceNumber: int = None
    ADSampleRate: int = None
    bufferSize: int = None
    MPSParameter: MPS060602Para = None


class WorkerSharedState:
    def __init__(self, card: MPS060602, config: DataWorkerConfig, queueSize=20, workerNumber=1) -> None:
        self.card = card
        self.config = config

        def blockInitializer(): return DataBlock(self.config.bufferSize)
        self.pool = Pool(queueSize+workerNumber, blockInitializer)
        self.leakQueue = LeakQueue(maxsize=queueSize, onKick=self.pool.retire)


class MPSDataWorker(QObject):
    configUpdated = pyqtSignal(DataWorkerConfig)

    def __init__(self, config: DataWorkerConfig):
        super().__init__()
        self.config = config
        self.card = MPS060602(
            device_number=self.config.deviceNumber,
            para=self.config.MPSParameter,
            buffer_size=self.config.bufferSize,
        )
        self.sharedState = WorkerSharedState(
            card=self.card, config=self.config)

    def start(self):
        # https://stackoverflow.com/questions/68163578/stopping-an-infinite-loop-in-a-worker-thread-in-pyqt5-the-simplest-way
        self.poller = QTimer()
        self.poller.timeout.connect(self.dataIn)
        self.poller.start(0)
        self.card.start()
        logger.info(f"Data worker started.")

    def dataIn(self):
        block = self.sharedState.pool.alloc()

        self.card._data_into_buffer(block.buffer)
        self.sharedState.leakQueue.put(block)

    def _configure(self, config: DataWorkerConfig):
        ...

    def updateConfig(self, config: DataWorkerConfig):
        """DataWorker must be paused while updating card info."""
        logger.info("DataWorker config updated.")
        self._configure(config)
        self.configUpdated.emit()


@dataclass
class ProcessorConfig:
    triggerVolt: float = None
    timeoutMs: int = None
    triggerRetryNum: int = None


class PostProcessWorker(QObject):
    dataReady = pyqtSignal(list)
    configUpdated = pyqtSignal(ProcessorConfig)

    def __init__(self, config: ProcessorConfig, workerSharedState: WorkerSharedState):
        super().__init__()
        self.config = config
        self.sharedState = workerSharedState
        self._configure(self.config)

    def start(self):
        self.poller = QTimer()
        self.poller.timeout.connect(self.process)
        self.poller.start(self.config.timeoutMs)
        logger.info(f"Post process worker started.")

    def process(self):
        for _ in range(self.config.triggerRetryNum):
            volt = self._getVoltDataFromQueue()
            index = self.trigger.triggeredIndex(volt)
            if (index is None) or (index > self.sharedState.config.bufferSize / 2):
                continue
            self.dataReady.emit(volt[index:])
            return

        # Trigger failed, emit the whole waveform.
        self.dataReady.emit(volt)

    def _getVoltDataFromQueue(self) -> typing.List[float]:
        block = self.sharedState.leakQueue.get()

        # Do copy manually, since PyQt object is never auto copied in signals.
        volt = [self.sharedState.card.to_volt(
            dataPoint) for dataPoint in block.buffer]
        # Return block to memory pool.
        self.sharedState.pool.retire(block)
        return volt

    def _configure(self, config: ProcessorConfig):
        if config.triggerVolt is not None:
            self.config.triggerVolt = config.triggerVolt
            self.trigger = EdgeTrigger(volt=config.triggerVolt)
        if config.triggerRetryNum is not None:
            self.config.triggerRetryNum = config.triggerRetryNum
        if config.timeoutMs is not None:
            self.config.timeoutMs = config.timeoutMs
            try:
                self.poller
                self.poller.setInterval(self.config.timeoutMs)
            except AttributeError:
                pass

    def updateConfig(self, config: ProcessorConfig):
        self._configure(config)
        logger.info("Processor config updated.")
        self.configUpdated.emit(self.config)
