import logging
from types import ModuleType
from typing import List
from PyQt5.QtCore import pyqtSignal
from dataclasses import dataclass
from importlib import import_module

from plugin.helpers.pluginType import PluginType

logger = logging.getLogger(__name__)

@dataclass
class PluginStatus:
    allPlugins: List[PluginType] = None


class PluginManager:
    """Load package from python environment."""
    pluginUpdated = pyqtSignal(PluginStatus)

    def __init__(self, allPluginName: List[str]):
        self.status = PluginStatus()
        allPluginModule = [import_module(name) for name in allPluginName]
        self.status.allPlugins = [m.init() for m in allPluginModule]
        logger.info(f"Load {len(self.status.allPlugins)} plugins.")

    def configurePluginStatus(self, status: PluginStatus):
        ...
