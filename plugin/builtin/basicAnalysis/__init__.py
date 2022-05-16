from PyQt5.QtWidgets import QWidget
from plugin.helpers.metadata import PluginMetaData
from plugin.helpers.pluginType import PanelType, PluginType, ProcessorType

from .ui.basicAnalysis import Ui_Form as BasicAnalysis


metadata = PluginMetaData(
    id="BasicAnalysis",
    display_name="Basic Analysis Plugin",
    description="""Show waveform metrics and oscilloscope status.
eg: Peak-to-Peak, V_top, and dead time.
""",
    tab_title="Basic Analysis",
)


class BasicAnalysisPlugin(PluginType):

    def __init__(self):
        prototype = BasicAnalysis()
        self.panel: BasicAnalysis = QWidget()
        prototype.setupUi(self.panel)

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


def init() -> PluginType:
    return BasicAnalysisPlugin()
