from PyQt5.QtWidgets import QWidget
from plugin.helpers.metadata import PluginMetaData
from plugin.helpers.pluginType import PanelType, PluginConfigType, PluginType, ProcessorType
from PyQt5.QtCore import pyqtSignal, QObject
from .panel import BasicAnalysisPanel


metadata = PluginMetaData(
    id="BasicAnalysis",
    display_name="Basic Analysis Plugin",
    description="""Show waveform metrics and oscilloscope status.
eg: Peak-to-Peak, V_top, and dead time.
""",
    tab_title="Basic Analysis",
)


class BasicAnalysisConfig(PluginConfigType):
    def getData(self) -> QWidget:
        ...

    def setData(self, data) -> QWidget:
        ...


class BasicAnalysisPlugin(PluginType):
    configSignal = pyqtSignal(BasicAnalysisConfig)

    def __init__(self):
        super().__init__()
        self.panel = BasicAnalysisPanel()

    def getMetadata(self) -> PluginMetaData:
        return PluginMetaData(
            id="BasicAnalysis",
            display_name="Basic Analysis Plugin",
            description="""Show waveform metrics and oscilloscope status.
eg: Peak-to-Peak, V_top, and dead time.
""",
            tab_title="Basic Analysis",
        )

    def getPanel(self) -> PanelType:
        return self.panel

    def getProcessor(self) -> ProcessorType:
        ...

    def getConfigureSignal(self) -> pyqtSignal(PluginConfigType):
        return self.configSignal


def init() -> PluginType:
    return BasicAnalysisPlugin()
