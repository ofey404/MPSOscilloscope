from tkinter import W
from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import QSlider, QComboBox, QLabel, QPushButton, QSpinBox
from dataclasses import dataclass

from view.display import OscilloscopeDisplay


@dataclass
class TriggerControlInfo:
    title1: str = "Trigger / V"
    title2: str = "/"
    sliderValue: int = 50

    def onStoppedForTimeout(self, control: "RightSliderControl"):
        triggerVolt = control._currentSliderVolt()
        control.display.updateTrigger(volt=triggerVolt)
        control.valueSpinBox1.setValue(triggerVolt)
        control.triggerSelected.emit(triggerVolt)

    def _onSliderValueChanged(self, control: "RightSliderControl"):
        self.sliderValue = control.slider.value()

        control.display.updateNextTriggerIndicator(
            control._currentSliderVolt())

    def _onToggleSliderVisibility(self, control: "RightSliderControl"):
        control.display.toggleTriggerLine()


@dataclass
class CursorControlInfo:
    indexThisCursor: int = 0
    title1: str = "Cursor 1 (Solid line) / V "
    title2: str = "Cursor 2 (Dashed line) / V"
    sliderValue: int = 50

    def onStoppedForTimeout(self, control: "RightSliderControl"):
        pass

    def _onSliderValueChanged(self, control: "RightSliderControl"):
        self.sliderValue = control.slider.value()

        cursorVolt = control._currentSliderVolt()
        control.allValueSpinBox[self.indexThisCursor].setValue(cursorVolt)
        control.display.updateCursor(self.indexThisCursor, control._currentSliderVolt())

    def _onToggleSliderVisibility(self, control: "RightSliderControl"):
        control.display.toggleCursorLine(self.indexThisCursor)


@dataclass
class RightSliderControlConfig:
    # Same order as in the sliderSelector.
    controlInfoList = [
        TriggerControlInfo(),
        CursorControlInfo(indexThisCursor=0),
        CursorControlInfo(indexThisCursor=1),
    ]


class RightSliderControl(QObject):
    triggerSelected = pyqtSignal(float)
    sliderPercentChanged = pyqtSignal(float)

    def __init__(self,
                 display: OscilloscopeDisplay,
                 slider: QSlider,
                 sliderSelector: QComboBox,
                 sliderVisibilityToggler: QPushButton,
                 valueSpinBox1: QSpinBox,
                 valueTitle1: QLabel,
                 valueSpinBox2: QSpinBox,
                 valueTitle2: QLabel,
                 ) -> None:
        super().__init__()
        self.config = RightSliderControlConfig()
        self.controlInfoList = self.config.controlInfoList

        self.display = display
        self.slider = slider
        self.sliderSelector = sliderSelector
        self.sliderVisibilityToggler = sliderVisibilityToggler
        self.allValueSpinBox = [valueSpinBox1, valueSpinBox2]
        self.allValueTitle = [valueTitle1, valueTitle2]
        self.valueSpinBox1 = valueSpinBox1
        self.valueTitle1 = valueTitle1
        self.valueSpinBox2 = valueSpinBox2
        self.valueTitle2 = valueTitle2

        self.delayedSliderWrapper = DelayedSliderWrapper(slider)
        self._connectSignals()
        self._setControllerTo(0)

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _connectSignals(self):
        self.delayedSliderWrapper.stoppedForTimeout.connect(
            self._onStoppedForTimeout)
        self.slider.valueChanged.connect(
            self._onSliderValueChanged
        )
        self.sliderVisibilityToggler.clicked.connect(
            self._onToggleSliderVisibility)
        self.sliderSelector.currentIndexChanged.connect(
            self._onSliderSelected
        )

    def _onSliderSelected(self, index):
        self._setControllerTo(index)

    def _setControllerTo(self, index):
        self.currentController = self.controlInfoList[index]

        c = self.currentController
        self.valueTitle1.setText(c.title1)
        self.valueTitle2.setText(c.title2)
        self.slider.setValue(c.sliderValue)

    def _onStoppedForTimeout(self, _):
        self.currentController.onStoppedForTimeout(self)

    def _onSliderValueChanged(self, _):
        self.currentController._onSliderValueChanged(self)

    def _onToggleSliderVisibility(self):
        self.currentController._onToggleSliderVisibility(self)

    def _sliderPercentage(self):
        return self.slider.value() / (self.slider.maximum() - self.slider.minimum())

    def _currentSliderVolt(self):
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
