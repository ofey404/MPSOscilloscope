from plugin.helpers.pluginType import PluginType
from .plugin import BasicAnalysisPlugin


def init() -> PluginType:
    return BasicAnalysisPlugin()
