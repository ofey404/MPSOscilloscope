from plugin.helpers.pluginType import PluginType
from .plugin import linearInterpolationPlugin


def init() -> PluginType:
    return linearInterpolationPlugin()

