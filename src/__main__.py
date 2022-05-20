import logging

from PyQt5.QtWidgets import QApplication

from controller.controller import OscilloscopeCtrl
from controller.pluginManager import PluginManager
from model import OscilloscopeModel
from controller.utils import pluginListFromConfigFile
from view import OscilloscopeUi

logger = logging.getLogger(__name__)


def main(argv):
    logging.basicConfig(level=logging.INFO)
    app = QApplication(argv)

    # Init MVC.
    view = OscilloscopeUi()
    view.show()

    model = OscilloscopeModel()

    pluginManager = PluginManager(pluginListFromConfigFile())

    OscilloscopeCtrl(model, view, pluginManager)

    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    main(sys.argv)
