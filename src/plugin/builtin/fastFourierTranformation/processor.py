from typing import List
from PyQt5.QtCore import pyqtSignal
from plugin.helpers.pluginType import ProcessorType
import numpy as np

from dataclasses import dataclass


@dataclass
class FFTData:
    freq: List[float] = None
    real: List[float] = None
    img: List[float] = None


class FFTProcessor(ProcessorType):
    dataUpdated = pyqtSignal(FFTData)

    def process(self, data: List[float]) -> List[float]:
        sp = np.fft.fft(data)
        freq = np.fft.fftfreq(len(data))
        self.dataUpdated.emit(FFTData(
            freq=freq,
            real=sp,
        ))
        return data

    def displayName(self) -> str:
        return "FFT Processor"
