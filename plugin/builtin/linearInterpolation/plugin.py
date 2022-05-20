from plugin.builtin.linearInterpolation.processor import LinearInterpolationProcessor
from plugin.helpers.metadata import PluginMetaData
from plugin.helpers.pluginType import PanelType, PluginType, ProcessorType

_METADATA = PluginMetaData(
    id="LinearInterpolation",
    display_name="Linear Interpolation Plugin",
    description="""Do linear interpolation to the waveform.""",
    tab_title=None,
)


class linearInterpolationPlugin(PluginType):

    def __init__(self) -> None:
        super().__init__()
        self.processor = LinearInterpolationProcessor()

    def getMetadata(self) -> PluginMetaData:
        return _METADATA

    def getPanel(self) -> PanelType:
        """No panel"""
        return None

    def getProcessor(self) -> ProcessorType:
        return self.processor
