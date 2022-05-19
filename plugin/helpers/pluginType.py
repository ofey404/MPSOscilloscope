from abc import ABC, abstractmethod
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget

from plugin.helpers.metadata import PluginMetaData


class PluginConfigType(ABC):
    def getData(self) -> QWidget:
        raise NotImplementedError()

    def setData(self, data) -> QWidget:
        raise NotImplementedError()


class PanelType(QObject):
    def getWidget(self) -> QWidget:
        raise NotImplementedError()

    def getSignalUiUpdated(self) -> pyqtSignal(PluginConfigType):
        raise NotImplementedError()


class ProcessorType(ABC):
    ...


class PluginType(QObject):
    def getMetadata(self) -> PluginMetaData:
        raise NotImplementedError()

    def getPanel(self) -> PanelType:
        raise NotImplementedError()

    def getProcessor(self) -> ProcessorType:
        raise NotImplementedError()

    def getConfigureSignal(self) -> pyqtSignal(PluginConfigType):
        raise NotImplementedError()

