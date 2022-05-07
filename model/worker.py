from ctypes import c_ushort
from dataclasses import dataclass

from mps060602 import MPS060602, ADChannelMode, MPS060602Para, PGAAmpRate
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from numpy import block

from .utils import Pool, LeakQueue


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
        self.queue = LeakQueue(maxsize=queueSize, onKick=self.pool.retire)


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


def _initWorkerGlobalState():
    global GLOBAL_STATE
    GLOBAL_STATE = WorkerSharedState()


class MPSDataWorker(QObject):
    dataReady = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def start(self):
        # https://stackoverflow.com/questions/68163578/stopping-an-infinite-loop-in-a-worker-thread-in-pyqt5-the-simplest-way
        self.poller = QTimer()
        self.poller.timeout.connect(self.dataIn)
        self.poller.start(0)

    def stop(self):
        print("stopped!")

    def dataIn(self):
        print("dataIn!")
        block = GLOBAL_STATE.pool.alloc()

        # TODO: read data to block.buffer
        GLOBAL_CARD._data_into_buffer(block.buffer)  # Mock.
        GLOBAL_STATE.queue.put(block)

    def readData(self):
        data = [0, 1]
        self.dataReady.emit(data)

    def updateConfig(self, config):
        print("Config updated.")


class PostProcessWorker(QObject):
    dataReady = pyqtSignal(list)

    def __init__(self, frameRate: int = 24):
        super().__init__()

        self.timeoutMs = 1000 / frameRate

    def start(self):
        self.poller = QTimer()
        self.poller.timeout.connect(self.process)
        self.poller.start(self.timeoutMs)

    def process(self):
        print("Processor working.")
        block = GLOBAL_STATE.queue.get()

        # Do copy manually, since PyQt object is never auto copied in signals.
        volt = [GLOBAL_CARD.to_volt(dataPoint) for dataPoint in block.buffer]
        self.dataReady.emit(volt)

        # Return block to memory pool.
        GLOBAL_STATE.pool.retire(block)

    def stop(self):
        print("stopped!")

    def updateConfig(self, config):
        print("Processor config updated.")
