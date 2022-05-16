from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QWidget

from plugin.helpers.metadata import PluginMetaData


class PanelType(ABC):
    @abstractmethod
    def getWidget(self) -> QWidget:
        ...

class ProcessorType(ABC):
    ...

class PluginType(ABC):
    @abstractmethod
    def getMetadata(self) -> PluginMetaData:
        ...

    @abstractmethod
    def getPanel(self) -> PanelType:
        ...

    @abstractmethod
    def getProcessor(self) -> ProcessorType:
        ...
