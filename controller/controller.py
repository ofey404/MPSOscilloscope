import logging

from model import OscilloscopeModel
from view import OscilloscopeUi

from controller.pluginManager import PluginManager
from view.utils import showError

logger = logging.getLogger(__name__)


class OscilloscopeCtrl:
    """MPS Oscilloscope's controller class."""

    def __init__(self, model: OscilloscopeModel, view: OscilloscopeUi, pluginManager: PluginManager):
        self.model = model
        self.view = view
        self.pluginManager = pluginManager

        if self.model.dataWorker.card == None:
            showError("Card is unplugged.",
                      "Please connect MPS060602 to USB port,\nthen restart the application.")
            exit(1)

        self._connectSignals()
        model.start()
        logger.info("Controller inited.")

    def _connectSignals(self):
        model, view, pluginManager = self.model, self.view, self.pluginManager

        model.dataReady.connect(view.updateData)
        model.reportConfigToModel.connect(view.updateByModelConfig)

        view.newModelConfig.connect(model.updateConfig)
        view.togglePlugins.connect(pluginManager.togglePlugins)

        pluginManager.pluginUpdated.connect(model.updateByPluginManager)
        pluginManager.pluginUpdated.connect(view.updateByPluginManager)
