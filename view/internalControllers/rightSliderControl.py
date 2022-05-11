from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import QSlider, QComboBox, QLCDNumber, QPushButton

from view.display import OscilloscopeDisplay


class RightSliderControl(QObject):
    triggerSelected = pyqtSignal(float)
    sliderPercentChanged = pyqtSignal(float)

    def __init__(self,
                 display: OscilloscopeDisplay,
                 slider: QSlider,
                 sliderSelector: QComboBox,
                 sliderVoltageDisplay: QLCDNumber,
                 sliderVisibilityToggler: QPushButton,
                 ) -> None:
        super().__init__()
        self.display = display
        self.slider = slider
        self.sliderSelector = sliderSelector
        self.sliderVoltageDisplay = sliderVoltageDisplay
        self.sliderVisibilityToggler = sliderVisibilityToggler

        self.delayedSliderWrapper = DelayedSliderWrapper(slider)
        self._connectSignals()

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _connectSignals(self):
        self.delayedSliderWrapper.stoppedForTimeout.connect(
            self._requestModelTriggerChange)
        self.slider.valueChanged.connect(
            self._onSliderValueChanged
        )
        self.sliderVisibilityToggler.clicked.connect(self.display.toggleTriggerLine)

    def _requestModelTriggerChange(self, _):
        triggerVolt = self._triggerVolt()
        self.display.updateTrigger(volt=triggerVolt)
        self.sliderVoltageDisplay.display(triggerVolt)
        self.triggerSelected.emit(triggerVolt)

    def _onSliderValueChanged(self, _):
        self.display.updateNextTriggerIndicator(self._triggerVolt())

    def _sliderPercentage(self):
        return self.slider.value() / (self.slider.maximum() - self.slider.minimum())

    def _triggerVolt(self):
        low, high = self.display.ylim()
        return low + self._sliderPercentage() * (high - low)


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
