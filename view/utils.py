from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import QSlider
from dataclasses import dataclass


class DelayedSliderWrapper(QObject):
    """Emit an extra signal after timeout,
       when the slider first move then stopped.
    """
    stoppedForTimeout = pyqtSignal(int)

    def __init__(self, slider: QSlider, timeoutMs: int = 100):
        super().__init__()
        self.slider = slider
        self.timer = QTimer()
        self.moving = False
        self._connectSignals()
        self.lastSliderValue = self.slider.value()
        self.timer.start(timeoutMs)

    def _connectSignals(self):
        self.timer.timeout.connect(self._checkSliderStopped)

    def _checkSliderStopped(self):
        if self.moving:
            if self.lastSliderValue == self.slider.value():
                self.moving = False
                self.stoppedForTimeout.emit(self.lastSliderValue)
        else:
            if self.lastSliderValue != self.slider.value():
                self.moving = True
        self.lastSliderValue = self.slider.value()


@dataclass
class ScrollBarStepConverter:
    """Scroll bar only accept integer as step.
       A helper for scaling on axis.
    """
    maxStep: int = 1000

    def limFloatToInt(self, lim, maxLim):
        maxIntLim = (0, self.maxStep)
        fStep = (maxLim[1] - maxLim[0]) / self.maxStep
        intLim = [
            int((lim[0] - maxLim[0]) / fStep),
            int((lim[1] - maxLim[0]) / fStep),
        ]
        return intLim, maxIntLim

    def intStepValueToFloat(self, intStepValue, maxlim):
        maxRange = maxlim[1] - maxlim[0]
        return (intStepValue / self.maxStep) * maxRange + maxlim[0]
