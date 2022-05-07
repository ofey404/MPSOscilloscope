from PyQt5.QtWidgets import QApplication
import logging

from model import OscilloscopeModel
from view import OscilloscopeUi


class OscilloscopeCtrl:
    """MPS Oscilloscope's controller class."""

    def __init__(self, model: OscilloscopeModel, view: OscilloscopeUi):
        self.model = model
        self.view = view

        self._connectSignals()
        model.startWorker()

    def _connectSignals(self):
        self.view.mainwindow.actionDisplay.triggered.connect(lambda: self.model.readData.emit())

        self.model.dataReady.connect(self.view.canvas.addData)
        # self.model.worker.dataReady.connect(self.view.canvas.addData)

def main(argv):
    logging.basicConfig(level=logging.INFO)

    app = QApplication(argv)
    view = OscilloscopeUi()
    view.show()
    model = OscilloscopeModel()
    OscilloscopeCtrl(model, view)
    sys.exit(app.exec_())



if __name__ == "__main__":
    import sys
    main(sys.argv)
