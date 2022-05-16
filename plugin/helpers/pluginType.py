from abc import ABC, abstractmethod
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget

from plugin.helpers.metadata import PluginMetaData
from utils import UnImplementedError


class PluginConfigType(ABC):
    def getData(self) -> QWidget:
        raise UnImplementedError()

    def setData(self, data) -> QWidget:
        raise UnImplementedError()


class PanelType(QObject):
    def getWidget(self) -> QWidget:
        raise UnImplementedError()

    def getSignalUiUpdated(self) -> pyqtSignal(PluginConfigType):
        raise UnImplementedError()


class ProcessorType(ABC):
    ...


class PluginType(QObject):
    def getMetadata(self) -> PluginMetaData:
        raise UnImplementedError()

    def getPanel(self) -> PanelType:
        raise UnImplementedError()

    def getProcessor(self) -> ProcessorType:
        raise UnImplementedError()

    def getConfigureSignal(self) -> pyqtSignal(PluginConfigType):
        raise UnImplementedError()
