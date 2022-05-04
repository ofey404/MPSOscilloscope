from PyQt5.QtWidgets import QApplication

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
        # self.model.worker.dataReady.connect(self.view.canvas.addData)

def testWorker():
    app = QApplication([])
    model = OscilloscopeModel()
    model.startWorker()
    sys.exit(app.exec_())

def main(argv):
    app = QApplication(argv)
    view = OscilloscopeUi()
    view.show()
    model = OscilloscopeModel()
    OscilloscopeCtrl(model, view)
    sys.exit(app.exec_())



if __name__ == "__main__":
    import sys
    main(sys.argv)
    # testWorker()
