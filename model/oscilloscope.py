import time
import typing
from dataclasses import dataclass, field
from itertools import cycle

from mps060602 import MPS060602, ADChannelMode, MPS060602Para, PGAAmpRate
from PyQt5.QtCore import (QMutex, QMutexLocker, QObject, QReadWriteLock,
                          QThread, QTimer, pyqtSignal, QReadLocker)


@dataclass
class DataBlock:
    buffer: list = field(default_factory=list)
    mutex: QMutex = QMutex()


class BlockPool:
    def __init__(self, size: int):
        self.available = [DataBlock() for _ in range(size)]

    def release(self, block: DataBlock):
        if block.mutex.tryLock():
            self.available.append(block)
            block.mutex.unlock()
            return
        raise Exception("Shouldn't return locked block!")

    def alloc(self):
        if self.available:
            return self.available.pop()
        raise Exception("Block pool should not expire!")


@dataclass
class WorkerConfig:
    deviceNumber: int = 0
    bufferSize: int = 2048
    settingChanged: bool = False
    parameter: MPS060602Para = MPS060602Para(
        ADChannel=ADChannelMode.in1,
        ADSampleRate=10000,
        Gain=PGAAmpRate.range_10V,
    )

@dataclass
class Billboard:
    block: DataBlock = None
    mutex: QMutex = QMutex()    

@dataclass()
class ModelSharedState:
    config: WorkerConfig
    pool: BlockPool

    # DataWorker post latest data to the board,
    # while postprocess worker check and visualize it.
    board: Billboard


class MPSDataWorker(QObject):
    dataReady = pyqtSignal(list)

    def __init__(self, state: ModelSharedState):
        super().__init__()

        self.config = WorkerConfig()
        self.card = MPS060602(
            device_number=self.config.deviceNumber,
            para=self.config.parameter,
            buffer_size=self.config.bufferSize
        )
        self.state = state

    def start(self):
        # https://stackoverflow.com/questions/68163578/stopping-an-infinite-loop-in-a-worker-thread-in-pyqt5-the-simplest-way
        self.poller = QTimer()
        self.poller.timeout.connect(self.dataIn)
        self.poller.start(0)

        self.card.start()

    def stop(self):
        print("stopped!")

    def dataIn(self):
        print("dataIn!")

    def readData(self):
        data = [0, 1]
        self.dataReady.emit(data)

    def updateConfig(self, config):
        print("Config updated.")


class PostProcessWorker(QObject):
    def __init__(self, state: ModelSharedState, frameRate: int = 24):
        super().__init__()

        self.timeoutMs = 1000 / frameRate
        self.state = state

    def start(self):
        self.poller = QTimer()
        self.poller.timeout.connect(self.process)
        self.poller.start(self.timeoutMs)

    def process(self):
        print("Processor working.")

    def stop(self):
        print("stopped!")

    def updateConfig(self, config):
        print("Processor config updated.")


class OscilloscopeModel(QObject):
    """MPS Oscilloscope's model."""
    updateConfig = pyqtSignal(WorkerConfig)

    def __init__(self):
        super().__init__()
        sharedState = ModelSharedState(
            config=WorkerConfig(),
            pool=BlockPool(20),
            board=Billboard()
        )
        self.dataWorker = MPSDataWorker(sharedState)
        self.dataWorkerThread = self._moveToThread(self.dataWorker)

        self.processor = PostProcessWorker(sharedState, frameRate=60)
        self.processorThread = self._moveToThread(self.processor)

        self._connectSignals()

    def _connectSignals(self):
        self.dataWorkerThread.started.connect(self.dataWorker.start)
        self.processorThread.started.connect(self.processor.start)

        self.updateConfig.connect(self.dataWorker.updateConfig)
        self.updateConfig.connect(self.processor.updateConfig)

    def _moveToThread(self, object: QObject) -> QThread:
        thread = QThread()
        object.moveToThread(thread)
        return thread

    def startWorker(self):
        self.dataWorkerThread.start()
        self.processorThread.start()
