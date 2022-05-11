from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import QSlider

from view.display import OscilloscopeDisplay


class RightSliderControl(QObject):
    triggerMovedAndStoppedForDelay = pyqtSignal(float)
    sliderPercentChanged = pyqtSignal(float)

    def __init__(self,
                 display: OscilloscopeDisplay,
                 slider: QSlider,
                 ) -> None:
        super().__init__()
        self.display = display
        self.slider = slider
        self.delayedSliderWrapper = DelayedSliderWrapper(slider)
        self._connectSignals()

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _connectSignals(self):
        self.delayedSliderWrapper.stoppedForTimeout.connect(
            self._reportTriggerStopped)
        self.slider.valueChanged.connect(
            self._reportSliderMove
        )

    def _reportTriggerStopped(self, _):
        self._reportSliderPercentage(self.triggerMovedAndStoppedForDelay)

    def _reportSliderMove(self, _):
        self._reportSliderPercentage(self.sliderPercentChanged)

    def _reportSliderPercentage(self, signal: pyqtSignal):
        signal.emit(
            self.slider.value() / (self.slider.maximum() - self.slider.minimum())
        )


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
