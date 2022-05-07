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
                 holdOffMs: int = 10
                 ) -> None:
        self.volt = volt
        self.upEdge = upEdge
        self.holdOff = holdOffMs

    def triggeredIndex(self, waveformVolt: typing.Iterable[float]) -> "int | None":
        return 0
