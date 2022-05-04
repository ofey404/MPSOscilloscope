import time
from dataclasses import dataclass
from mps060602 import MPS060602, ADChannelMode, MPS060602Para, PGAAmpRate
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QMutex, QTimer


class WorkerConfig:
    """Shared state between Model and Worker.
    Access with lock!
    """

    def __init__(self):
        self.mutex = QMutex()

        self.parameter = MPS060602Para(
            ADChannel=ADChannelMode.in1,
            ADSampleRate=10000,
            Gain=PGAAmpRate.range_10V,
        )
        self.deviceNumber = 0
        self.bufferSize = 2048

        self.settingChanged = False


class MPSWorker(QObject):
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
        time.sleep(1)

    def readData(self):
        data = [0, 1]
        self.dataReady.emit(data)

    def updateConfig(self, config):
        print("Config updated.")


class OscilloscopeModel(QObject):
    """MPS Oscilloscope's model."""
    updateConfig = pyqtSignal(WorkerConfig)
    readData = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.worker = MPSWorker()
        self.thread = QThread()

        self.worker.moveToThread(self.thread)
        self._connectSignals()

    def _connectSignals(self):
        self.thread.started.connect(self.worker.start)
        self.updateConfig.connect(self.worker.updateConfig)
        self.readData.connect(self.worker.readData)
        self.worker.dataReady.connect(self.processData)

    def startWorker(self):
        self.thread.start()

    def processData(self, data):
        print(f"processData={data}")
