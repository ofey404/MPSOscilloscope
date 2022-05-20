from typing import List
from PyQt5.QtCore import pyqtSignal
from plugin.helpers.pluginType import ProcessorType
from dataclasses import dataclass


@dataclass
class FFTData:
    ...


class FFTProcessor(ProcessorType):
    dataUpdated = pyqtSignal(FFTData)

    def process(self, data: List[float]) -> List[float]:
        # self.dataUpdated.emit(FFTData())
        return data

    def displayName(self) -> str:
        return "FFT Processor"
