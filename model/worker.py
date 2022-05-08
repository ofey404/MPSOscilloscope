from ctypes import c_ushort
import logging
import typing
from dataclasses import dataclass

from .trigger import EdgeTrigger

from mps060602 import MPS060602, ADChannelMode, MPS060602Para, PGAAmpRate
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from .utils import Pool, LeakQueue

logger = logging.getLogger(__name__)

DEVICE_NUMBER = 0

PARAMETER = MPS060602Para(
    ADChannel=ADChannelMode.in1,
    ADSampleRate=10000,
    Gain=PGAAmpRate.range_10V,
)

BUFFER_SIZE: int = 2048


@dataclass
class DataBlock:
    buffer = (c_ushort * BUFFER_SIZE)()


class WorkerSharedState:
    def __init__(self, queueSize=20, workerNumber=1) -> None:
        self.pool = Pool(queueSize+workerNumber, DataBlock)
        self.leakQueue = LeakQueue(maxsize=queueSize, onKick=self.pool.retire)


# Global States.
GLOBAL_CARD: MPS060602 = None
GLOBAL_STATE: WorkerSharedState = None


def initWorkerGlobalInfo():
    _initGlobalCard()
    _initWorkerGlobalState()


def _initGlobalCard():
    global GLOBAL_CARD
    GLOBAL_CARD = MPS060602(
        device_number=DEVICE_NUMBER,
        para=PARAMETER,
        buffer_size=BUFFER_SIZE
    )
    GLOBAL_CARD.start()
    logger.info("MPS060602 card started.")


def _initWorkerGlobalState():
    global GLOBAL_STATE
    GLOBAL_STATE = WorkerSharedState()


@dataclass
class DataWorkerConfig:
    pass


class MPSDataWorker(QObject):
    configUpdated = pyqtSignal(DataWorkerConfig)

    def __init__(self):
        super().__init__()

    def start(self):
        # https://stackoverflow.com/questions/68163578/stopping-an-infinite-loop-in-a-worker-thread-in-pyqt5-the-simplest-way
        self.poller = QTimer()
        self.poller.timeout.connect(self.dataIn)
        self.poller.start(0)
        logger.info(f"Data worker started.")

    def stop(self):
        print("stopped!")

    def dataIn(self):
        block = GLOBAL_STATE.pool.alloc()

        GLOBAL_CARD._data_into_buffer(block.buffer)
        GLOBAL_STATE.leakQueue.put(block)

    def _configure(self, config: DataWorkerConfig):
        ...

    def updateConfig(self, config: DataWorkerConfig):
        """DataWorker must be paused while updating card info."""
        print("Config updated.")
        self._configure(config)
        self.configUpdated.emit()


@dataclass
class ProcessorConfig:
    triggerVolt: float = None


class PostProcessWorker(QObject):
    dataReady = pyqtSignal(list)
    configUpdated = pyqtSignal(ProcessorConfig)

    def __init__(self, frameRate: int = 24):
        super().__init__()
        self.config = ProcessorConfig(triggerVolt=0)

        self.timeoutMs = 1000 / frameRate
        self._configure(self.config)

    def start(self):
        self.poller = QTimer()
        self.poller.timeout.connect(self.process)
        self.poller.start(self.timeoutMs)
        logger.info(f"Post process worker started.")

    def process(self):
        while True:
            volt = self._getVoltDataFromQueue()
            index = self.trigger.triggeredIndex(volt)
            if (index is None) or (index > BUFFER_SIZE / 2):
                continue
            break

        self.dataReady.emit(volt[index:])

    def _getVoltDataFromQueue(self) -> typing.List[float]:
        block = GLOBAL_STATE.leakQueue.get()

        # Do copy manually, since PyQt object is never auto copied in signals.
        volt = [GLOBAL_CARD.to_volt(dataPoint) for dataPoint in block.buffer]
        # Return block to memory pool.
        GLOBAL_STATE.pool.retire(block)
        return volt

    def stop(self):
        print("stopped!")

    def _configure(self, config: ProcessorConfig):
        if config.triggerVolt is not None:
            self.config.triggerVolt = config.triggerVolt
            self.trigger = EdgeTrigger(volt=config.triggerVolt)

    def updateConfig(self, config: ProcessorConfig):
        self._configure(config)
        logger.info("Processor config updated.")
        self.configUpdated.emit(self.config)
