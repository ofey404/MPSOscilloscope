from PyQt5.QtCore import QObject, QThread, pyqtSignal

from .worker import MPSDataWorker, PostProcessWorker, initWorkerGlobalInfo
import logging


logger = logging.getLogger(__name__)


class OscilloscopeModel(QObject):
    """MPS Oscilloscope's model."""
    updateConfig = pyqtSignal(int)
    dataReady = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        initWorkerGlobalInfo()

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
        logger.info("Worker threads started.")
