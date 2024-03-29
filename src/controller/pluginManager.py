import logging
from typing import List
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget
from dataclasses import dataclass
from importlib import import_module

from plugin.helpers.pluginType import PluginType

logger = logging.getLogger(__name__)


@dataclass(init=False)
class PluginStatus:
    allPlugins: List[PluginType] = None
    enabled: List[bool] = None
    controlTab: List[QWidget] = None
    orderedPostProcessor: List[PluginType] = None

    def __init__(self, moduleList) -> None:
        self.allPlugins = [m.init() for m in moduleList]
        self.enabled = [True for _ in self.allPlugins]
        self.controlTab = [None for _ in self.allPlugins]
        self.orderedPostProcessor = [
            p.getProcessor() for p in self.allPlugins if p.getProcessor() is not None]


class PluginManager(QObject):
    """Load package from python environment."""
    pluginUpdated = pyqtSignal(PluginStatus)

    def __init__(self, allPluginName: List[str]):
        super().__init__()
        allPluginModule = [import_module(name) for name in allPluginName]
        self.status = PluginStatus(allPluginModule)
        logger.info(f"Load {len(self.status.allPlugins)} plugins.")

    def configurePluginStatus(self, status: PluginStatus):
        self.status = status
        self.updatePlugin()

    def updatePlugin(self):
        self.pluginUpdated.emit(self.status)
