
from PyQt5.QtCore import pyqtSignal

from plugin.helpers.metadata import PluginMetaData
from plugin.helpers.pluginType import PanelType, PluginType, ProcessorType

from .panel import BasicAnalysisPanel
from .processor import BasicAnalysisProcessor, BasicAnalysisData


_METADATA = PluginMetaData(
    id="BasicAnalysis",
    display_name="Basic Analysis Plugin",
    description="""Show waveform metrics and oscilloscope status.
eg: Peak-to-Peak, V_top, and dead time.
""",
    tab_title="Basic Analysis",
)


class BasicAnalysisPlugin(PluginType):
    configSignal = pyqtSignal(BasicAnalysisData)

    def __init__(self):
        super().__init__()
        self.panel = BasicAnalysisPanel()
        self.processor = BasicAnalysisProcessor()
        self.data = BasicAnalysisData()

        self._connectSignals()

    def getMetadata(self) -> PluginMetaData:
        return _METADATA

    def getPanel(self) -> PanelType:
        return self.panel

    def getProcessor(self) -> ProcessorType:
        return self.processor

    def getConfigureSignal(self) -> pyqtSignal(BasicAnalysisData):
        return self.configSignal

    def _connectSignals(self):
        self.processor.dataUpdated.connect(self.panel.updateByData)
