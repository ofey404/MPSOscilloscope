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

        model.dataReady.connect(view.updateData)
        model.configUpdated.connect(view.updateByModelConfig)
        view.newModelConfig.connect(model.updateConfig)
