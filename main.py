from PyQt5.QtWidgets import QApplication
import logging

from model import OscilloscopeModel
from view import OscilloscopeUi


logger = logging.getLogger(__name__)


class OscilloscopeCtrl:
    """MPS Oscilloscope's controller class."""

    def __init__(self, model: OscilloscopeModel, view: OscilloscopeUi):
        self.model = model
        self.view = view

        self._connectSignals()
        model.start()

        logger.info("Controller inited.")

    def _connectSignals(self):
        model, view = self.model, self.view

        model.dataReady.connect(view.canvas.addData)

        model.configUpdated.connect(
            lambda config: view.canvas.adjustTrigger(config.processor.triggerVolt)
        )
        view.mainwindow.actionDisplay.triggered.connect(model._changeTrigger)


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
