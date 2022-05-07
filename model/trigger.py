from abc import ABC, abstractmethod
import typing


class Trigger(ABC):
    @abstractmethod
    def triggeredIndex(self, waveformVolt: typing.Iterable[float]) -> "int | None":
        """Get triggered index of waveform.

        Args:
            waveform (typing.Iterable[float]): Target waveform.

        Returns:
            int | None: First index of triggered data. If not triggered, return None.
        """
        pass


class EdgeTrigger(Trigger):
    def __init__(self,
                 volt: float = 0,
                 upEdge: bool = True,
                 ) -> None:
        self.volt = volt

        upEdgeCriterion = lambda data, lastData: data > self.volt and lastData < self.volt
        downEdgeCriterion = lambda data, lastData: data < self.volt and lastData > self.volt
        self.criterion = upEdgeCriterion if upEdge else downEdgeCriterion


    def triggeredIndex(self, waveformVolt: typing.Iterable[float]) -> "int | None":
        lastData = waveformVolt[0]
        for i, data in enumerate(waveformVolt):
            if self.criterion(data, lastData):
                return i
            lastData = data
        return None
