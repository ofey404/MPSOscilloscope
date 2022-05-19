from plugin.helpers.metadata import PluginMetaData
from plugin.helpers.pluginType import PluginType
from .plugin import BasicAnalysisPlugin


metadata = PluginMetaData(
    id="BasicAnalysis",
    display_name="Basic Analysis Plugin",
    description="""Show waveform metrics and oscilloscope status.
eg: Peak-to-Peak, V_top, and dead time.
""",
    tab_title="Basic Analysis",
)


def init() -> PluginType:
    return BasicAnalysisPlugin()
