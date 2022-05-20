from typing import List
from PyQt5.QtCore import pyqtSignal
from plugin.helpers.pluginType import ProcessorType
from dataclasses import dataclass


@dataclass
class BasicAnalysisData:
    vTop: float = None


class BasicAnalysisProcessor(ProcessorType):
    dataUpdated = pyqtSignal(BasicAnalysisData)

    def process(self, data: List[float]) -> List[float]:
        self.dataUpdated.emit(
            BasicAnalysisData(
                vTop=max(data)
            )
        )
        return data
