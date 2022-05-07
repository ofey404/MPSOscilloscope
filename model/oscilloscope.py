import time
from dataclasses import dataclass, field

from mps060602 import MPS060602, ADChannelMode, MPS060602Para, PGAAmpRate
from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal

from .utils import Pool, LeakQueue


@dataclass
class DataBlock:
    buffer: list = field(default_factory=list)


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


class ModelSharedState:
    def __init__(self, config: WorkerConfig) -> None:
        self.config = config
        self.pool = Pool(20, DataBlock)
        self.queue = LeakQueue(maxsize=19, onKick=self.pool.retire)


class MPSDataWorker(QObject):
    dataReady = pyqtSignal(list)

    def __init__(self, state: ModelSharedState):
        super().__init__()

        self.config = state.config
        self.card = MPS060602(
            device_number=self.config.deviceNumber,
            para=self.config.parameter,
            buffer_size=self.config.bufferSize
        )
        self.pool = state.pool
        self.queue = state.queue

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
        block = self.pool.alloc()

        # TODO: read data to block.buffer
        block.buffer = [time.time()]

        self.queue.put(block)

    def readData(self):
        data = [0, 1]
        self.dataReady.emit(data)

    def updateConfig(self, config):
        print("Config updated.")


class PostProcessWorker(QObject):
    dataReady = pyqtSignal(list)

    def __init__(self, state: ModelSharedState, frameRate: int = 24):
        super().__init__()

        self.timeoutMs = 1000 / frameRate
        self.queue = state.queue
        self.pool = state.pool

    def start(self):
        self.poller = QTimer()
        self.poller.timeout.connect(self.process)
        self.poller.start(self.timeoutMs)

    def process(self):
        print("Processor working.")
        block = self.queue.get()

        # Do copy manually, since PyQt object is never auto copied in signals.
        self.dataReady.emit(block.buffer.copy())

        # Return block to memory pool.
        self.pool.retire(block)

    def stop(self):
        print("stopped!")

    def updateConfig(self, config):
        print("Processor config updated.")


class OscilloscopeModel(QObject):
    """MPS Oscilloscope's model."""
    updateConfig = pyqtSignal(WorkerConfig)
    dataReady = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        sharedState = ModelSharedState(
            config=WorkerConfig()
        )
        self.dataWorker = MPSDataWorker(sharedState)
        self.dataWorkerThread = self._moveToThread(self.dataWorker)

        self.processor = PostProcessWorker(sharedState, frameRate=60)
        self.processorThread = self._moveToThread(self.processor)

        self._connectSignals()

    def _connectSignals(self):
        self.dataWorkerThread.started.connect(self.dataWorker.start)
        self.processorThread.started.connect(self.processor.start)

        # Signal from workers.
        self.processor.dataReady.connect(self._dataReady)

        # To workers.
        self.updateConfig.connect(self.dataWorker.updateConfig)
        self.updateConfig.connect(self.processor.updateConfig)

    def _moveToThread(self, object: QObject) -> QThread:
        thread = QThread()
        object.moveToThread(thread)
        return thread

    def _dataReady(self, data):
        self.dataReady.emit(data)

    def startWorker(self):
        self.dataWorkerThread.start()
        self.processorThread.start()
