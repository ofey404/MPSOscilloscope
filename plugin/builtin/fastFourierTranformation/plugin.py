from plugin.helpers.pluginType import PanelType, PluginType, ProcessorType
from plugin.helpers.metadata import PluginMetaData
from .panel import FFTPanel, FFTData
from .processor import FFTProcessor


_METADATA = PluginMetaData(
    id="FastFourierTransformation",
    display_name="FFT Plugin",
    description="""Do FFT.""",
    tab_title="FFT",
)


class FFTPlugin(PluginType):

    def __init__(self):
        super().__init__()

        self.panel = FFTPanel()
        self.processor = FFTProcessor()
        self.data = FFTData()

        self._connectSignals()

    def getMetadata(self) -> PluginMetaData:
        return _METADATA

    def getPanel(self) -> PanelType:
        return self.panel

    def getProcessor(self) -> ProcessorType:
        return self.processor

    def _connectSignals(self):
        ...
