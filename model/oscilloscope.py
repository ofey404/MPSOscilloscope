import time
import typing
from dataclasses import dataclass
from itertools import cycle

from mps060602 import MPS060602, ADChannelMode, MPS060602Para, PGAAmpRate
from PyQt5.QtCore import (QMutex, QMutexLocker, QObject, QReadWriteLock,
                          QThread, QTimer, pyqtSignal, QReadLocker)


class WorkerConfig:
    """Shared state between Model and Worker."""

    def __init__(self):
        self.parameter = MPS060602Para(
            ADChannel=ADChannelMode.in1,
            ADSampleRate=10000,
            Gain=PGAAmpRate.range_10V,
        )
        self.deviceNumber = 0
        self.bufferSize = 2048

        self.settingChanged = False


class MPSDataAquireWorker(QObject):
    dataReady = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.config = WorkerConfig()
        self.card = MPS060602(
            device_number=self.config.deviceNumber,
            para=self.config.parameter,
            buffer_size=self.config.bufferSize
        )

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
    def __init__(self, frameRate: int = 24):
        super().__init__()

        self.timeoutMs = 1000 / frameRate

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
        self.dataWorker = MPSDataAquireWorker()
        self.dataWorkerThread = self._moveToThread(self.dataWorker)

        self.processor = PostProcessWorker(frameRate=60)
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
