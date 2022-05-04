import time

import numpy as np
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class Worker(QObject):
    dataSignal = pyqtSignal(float)

    def __init__(self):
        super().__init__()

    def run(self):
        # Simulate some data
        n = np.linspace(0, 499, 500)
        y = 50 + 25*(np.sin(n / 8.3)) + 10 * \
            (np.sin(n / 7.5)) - 5*(np.sin(n / 1.5))
        i = 0

        while(True):
            if(i > 499):
                i = 0
            time.sleep(0.1)
            self.dataSignal.emit(y[i])  # <- Here you emit a signal!
            i += 1


class OscilloscopeModel:
    """MPS Oscilloscope's model."""

    def __init__(self):
        self.worker = Worker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

    def startWorker(self):
        self.thread.start()
