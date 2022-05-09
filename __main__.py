import logging

from PyQt5.QtWidgets import QApplication

from controller import OscilloscopeCtrl
from model import OscilloscopeModel
from view import OscilloscopeUi

logger = logging.getLogger(__name__)


def main(argv):
    logging.basicConfig(level=logging.INFO)
    app = QApplication(argv)

    # Init MVC.
    view = OscilloscopeUi()
    view.show()
    view._temporaryUiFix()

    model = OscilloscopeModel()
    OscilloscopeCtrl(model, view)

    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    main(sys.argv)
