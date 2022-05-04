# This Python file uses the following encoding: utf-8
import sys
import time
import threading
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget
from view import OscilloscopeUi


class DataAcquisitionWorker(QObject):
    updated = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        ...


class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(float)

class OscilloscopeModel:
    """MPS Oscilloscope's model."""

    def __init__(self):
        pass

    def dataSendLoop(self, addData_callbackFunc):
        # Setup the signal-slot mechanism.
        mySrc = Communicate()
        mySrc.data_signal.connect(addData_callbackFunc)

        # Simulate some data
        n = np.linspace(0, 499, 500)
        y = 50 + 25*(np.sin(n / 8.3)) + 10*(np.sin(n / 7.5)) - 5*(np.sin(n / 1.5))
        i = 0

        while(True):
            if(i > 499):
                i = 0
            time.sleep(0.1)
            mySrc.data_signal.emit(y[i])  # <- Here you emit a signal!
            i += 1

 

class OscilloscopeCtrl:
    """MPS Oscilloscope's controller class."""

    def __init__(self, model: OscilloscopeModel, view: OscilloscopeUi):
        self.model = model
        self.view = view

        self._connectSignals()
        self._initWorkers()

    def _connectSignals(self):
        self.view.mainwindow.actionDisplay.triggered.connect(lambda: self.view.switchToPage(1))


    def _initWorkers(self):
        myDataLoop = threading.Thread(name='myDataLoop', target=self.model.dataSendLoop, daemon=True, args=(self.view.canvas.addData,))
        myDataLoop.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = OscilloscopeUi()
    view.show()
    model = OscilloscopeModel()
    OscilloscopeCtrl(model, view)
    sys.exit(app.exec_())
