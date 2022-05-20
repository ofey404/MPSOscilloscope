import time
from collections import deque
from typing import List
from PyQt5.QtCore import pyqtSignal
from plugin.helpers.pluginType import ProcessorType
from dataclasses import dataclass


@dataclass
class BasicAnalysisData:
    vTop: float = None
    vBase: float = None
    vAmplitude: float = None
    vMax: float = None
    vMin: float = None
    vPeakToPeak: float = None

    deadTimePercent: float = None
    frameRate: float = None


_RECORD_SIZE = 10


class BasicAnalysisProcessor(ProcessorType):
    dataUpdated = pyqtSignal(BasicAnalysisData)

    def __init__(self):
        super().__init__()
        self.processTimeRecord = deque(
            [time.time()] * _RECORD_SIZE, maxlen=_RECORD_SIZE)

    def process(self, data: List[float]) -> List[float]:
        # TODO: we can do one-pass.

        vMax = max(data)
        vMin = min(data)
        vPeakToPeak = vMax - vMin

        max40Threshold = vMin + 0.6 * vPeakToPeak
        min40Threshold = vMin + 0.4 * vPeakToPeak
        allTop = [d for d in data if d > max40Threshold]
        allBase = [d for d in data if d < min40Threshold]

        vTop = sum(allTop)/len(allTop)
        vBase = sum(allBase)/len(allBase)
        vAmplitude = vTop - vBase

        currentTime = time.time()
        frameRate = _RECORD_SIZE / \
            (self.processTimeRecord[0] -
             self.processTimeRecord[-1] + 0.00000001)
        self.dataUpdated.emit(
            BasicAnalysisData(
                vTop=vTop,
                vBase=vBase,
                vAmplitude=vAmplitude,
                vMax=vMax,
                vMin=vMin,
                vPeakToPeak=vPeakToPeak,
                frameRate=frameRate,
            )
        )
        self.processTimeRecord.appendleft(currentTime)
        return data

    def displayName(self) -> str:
        return "Basic Analysis Processor"
