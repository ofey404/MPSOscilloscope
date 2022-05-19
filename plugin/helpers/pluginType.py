from abc import ABC, abstractmethod
from typing import List
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget

from plugin.helpers.metadata import PluginMetaData


class PanelType(QObject):
    def getWidget(self) -> QWidget:
        raise NotImplementedError()


class ProcessorType(QObject):
    def process(self, data: List[float]) -> List[float]:
        raise NotImplementedError()


class PluginType(QObject):
    def getMetadata(self) -> PluginMetaData:
        raise NotImplementedError()

    def getPanel(self) -> PanelType:
        raise NotImplementedError()

    def getProcessor(self) -> ProcessorType:
        raise NotImplementedError()
