from plugin.helpers.pluginType import PluginType
from .plugin import FFTPlugin


def init() -> PluginType:
    return FFTPlugin()

