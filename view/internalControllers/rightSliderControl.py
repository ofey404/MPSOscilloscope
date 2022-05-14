from tkinter import W
from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import QSlider, QComboBox, QLabel, QPushButton, QSpinBox
from dataclasses import dataclass

from view.display import OscilloscopeDisplay


@dataclass
class TriggerControlInfo:
    titles = [
        "Trigger / V",
        "/",
    ]
    sliderPercentage = 0.5
    firstVisit: bool = True

    def _onFirstVisited(self, control: "RightSliderControl"):
        if not control.display.config.triggerLineVisible:
            control.display.toggleTriggerLine()

    def _onStoppedForTimeout(self, control: "RightSliderControl"):
        triggerVolt = control._currentSliderVolt()
        control.display.updateTrigger(volt=triggerVolt)
        control.allValueSpinBox[0].setValue(triggerVolt)
        control.triggerSelected.emit(triggerVolt)

    def _onSliderValueChanged(self, control: "RightSliderControl"):
        self.sliderPercentage = control._sliderPercentage()

        control.display.updateNextTriggerIndicator(
            control._currentSliderVolt())

    def _onToggleSliderVisibility(self, control: "RightSliderControl"):
        control.display.toggleTriggerLine()


@dataclass
class CursorControlInfo:
    indexThisCursor: int = 0
    titles = [
        "Cursor 1 (Solid line) / V ",
        "Cursor 2 (Dashed line) / V",
    ]
    sliderPercentage = 0.5
    firstVisit = True

    def _onFirstVisited(self, control: "RightSliderControl"):
        if not control.display.config.cursorVisible[self.indexThisCursor]:
            control.display.toggleCursorLine(self.indexThisCursor)

    def _onStoppedForTimeout(self, control: "RightSliderControl"):
        pass

    def _onSliderValueChanged(self, control: "RightSliderControl"):
        self.sliderPercentage = control._sliderPercentage()

        cursorVolt = control._currentSliderVolt()
        control.allValueSpinBox[self.indexThisCursor].setValue(cursorVolt)
        control.display.updateCursor(
            self.indexThisCursor, control._currentSliderVolt())

    def _onToggleSliderVisibility(self, control: "RightSliderControl"):
        control.display.toggleCursorLine(self.indexThisCursor)


@dataclass
class VerticalCursorControlInfo:
    indexThisCursor: int = 0
    titles = [
        "Cursor 1 (Solid line) / ms ",
        "Cursor 2 (Dashed line) / ms",
    ]
    sliderPercentage = 0.5
    firstVisit = True

    def _onFirstVisited(self, control: "RightSliderControl"):
        if not control.display.config.verticalCursorVisible[self.indexThisCursor]:
            control.display.toggleVerticalCursorLine(self.indexThisCursor)
        control.display.config.verticalCursorTime = [control.display.config.timeLimMs()[1] / 2, ] * 2

    def _onStoppedForTimeout(self, control: "RightSliderControl"):
        pass

    def _onSliderValueChanged(self, control: "RightSliderControl"):
        self.sliderPercentage = control._sliderPercentage()

        cursorMs = control._currentSliderTimeMs()
        control.allValueSpinBox[self.indexThisCursor].setValue(cursorMs)
        control.display.updateVerticalCursor(
            self.indexThisCursor, cursorMs)

    def _onToggleSliderVisibility(self, control: "RightSliderControl"):
        control.display.toggleVerticalCursorLine(self.indexThisCursor)


@dataclass
class RightSliderControlConfig:
    # Same order as in the sliderSelector.
    controlInfoList = [
        TriggerControlInfo(),
        CursorControlInfo(indexThisCursor=0),
        CursorControlInfo(indexThisCursor=1),
        VerticalCursorControlInfo(indexThisCursor=0),
        VerticalCursorControlInfo(indexThisCursor=1),
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

        if self.currentController.firstVisit:
            self.currentController._onFirstVisited(self)
            self.currentController.firstVisit = False

        c = self.currentController
        for i, title in enumerate(self.allValueTitle):
            title.setText(c.titles[i])
        sliderValue = (self.slider.minimum() +
                       (self.slider.maximum() - self.slider.minimum()) * c.sliderPercentage)
        self.slider.setValue(sliderValue)

    def _onStoppedForTimeout(self, _):
        self.currentController._onStoppedForTimeout(self)

    def _onSliderValueChanged(self, _):
        self.currentController._onSliderValueChanged(self)

    def _onToggleSliderVisibility(self):
        self.currentController._onToggleSliderVisibility(self)

    def _sliderPercentage(self):
        return self.slider.value() / (self.slider.maximum() - self.slider.minimum())

    def _currentSliderVolt(self):
        low, high = self.display.ylim()
        return low + self._sliderPercentage() * (high - low)

    def _currentSliderTimeMs(self):
        low, high = self.display.xlim()
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
