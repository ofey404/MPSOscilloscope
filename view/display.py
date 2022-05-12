import logging
from tkinter import W

import matplotlib
import numpy as np
from attr import dataclass
from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from model.worker import AD_SAMPLE_RATE, BUFFER_SIZE

matplotlib.use("Qt5Agg")
logger = logging.getLogger(__name__)


@dataclass
class DisplayConfig:
    dataPointCount = BUFFER_SIZE // 2
    voltageLim = (-1, 1)
    dataStepTimeMs = 1 / AD_SAMPLE_RATE * 1000
    timeLimMs = (0, dataStepTimeMs * dataPointCount)

    triggerLineVisible = True
    trigger = 0
    nextTriggerIndicator = 0

    cursorVisible = [False, False]
    cursorVoltage = [0, 0]

    verticalCursorVisible = [False, False]
    verticalCursorTime = [timeLimMs[1] / 2, ] * 2


class VerticalLine(Line2D):
    def __init__(self, yLim, x=None, **kwargs) -> None:
        super().__init__([x, x], yLim, **kwargs)
        self.yLim = yLim
        if x is not None:
            self.x = x

    def set_x(self, x=None):
        if x is not None:
            self.x = x
        self.set_data([self.x, ] * 2, self.yLim)

    def set_invisible(self):
        self.set_data([], [])


class HorizontalLine(Line2D):
    def __init__(self, xLim, y=None, **kwargs) -> None:
        super().__init__(xLim, [y, y], **kwargs)
        self.xLim = xLim
        if y is not None:
            self.y = y

    def set_y(self, y=None):
        if y is not None:
            self.y = y
        self.set_data(self.xLim, [self.y, ] * 2)

    def set_invisible(self):
        self.set_data([], [])


class OscilloscopeDisplay(FigureCanvas, TimedAnimation):
    def __init__(self, config: DisplayConfig):
        logger.info(f"Matplotlib Version: {matplotlib.__version__}")

        self.config = config

        # 2 times longer than minimal data length passed by trigger.
        self.n = np.linspace(
            0, self.config.timeLimMs[1] * 2, self.config.dataPointCount * 2 + 1)
        self.y = (self.n * 0.0) + 50

        # The window
        self.fig, self.ax = self._init_fig()

        self.dataLine = HorizontalLine(
            xLim=self.config.timeLimMs, color='blue')
        self.ax.add_line(self.dataLine)

        self.triggerLine = HorizontalLine(
            xLim=self.config.timeLimMs, color='red')
        self.ax.add_line(self.triggerLine)

        self.nextTriggerDashedLine = HorizontalLine(
            xLim=self.config.timeLimMs, color='red', linestyle="--")
        self.ax.add_line(self.nextTriggerDashedLine)

        self.cursorLines = [
            HorizontalLine(
                xLim=self.config.timeLimMs, color='green'),
            HorizontalLine(
                xLim=self.config.timeLimMs, color='green', linestyle="--"),
        ]

        self.verticalCursorLines = [
            VerticalLine(yLim=self.config.voltageLim, color='green'),
            VerticalLine(yLim=self.config.voltageLim,
                         color='green', linestyle="--"),
        ]

        for line in [*self.cursorLines, *self.verticalCursorLines]:
            self.ax.add_line(line)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=50, blit=True)
        logger.info("View inited.")

    def xlim(self):
        return self.ax.get_xlim()

    def ylim(self):
        return self.ax.get_ylim()

    def updateData(self, value):
        self.y = value

    def updateTrigger(self, volt):
        self.config.trigger = volt

    def updateCursor(self, index, volt):
        self.config.cursorVoltage[index] = volt

    def updateVerticalCursor(self, index, timeMs):
        self.config.verticalCursorTime[index] = timeMs

    def updateNextTriggerIndicator(self, volt):
        self.config.nextTriggerIndicator = volt

    def updateConfig(self, config: DisplayConfig):
        self.config = config

    def zoomY(self, value):
        newLim = self._moveLim(
            lim=self.ax.get_ylim(),
            value=value,
            max=self.config.voltageLim,
        )
        self.ax.set_ylim(*newLim)
        self.draw()

        logger.info(
            f"Zoom in on Y axis by value {value}, new lim is {newLim}.")

    def zoomX(self, value):
        newLim = self._moveLim(
            lim=self.ax.get_xlim(),
            value=value,
            max=self.config.timeLimMs,
        )
        self.ax.set_xlim(*newLim)
        self.draw()

        logger.info(
            f"Zoom in on X axis by value {value}, new lim is {newLim}.")

    def scrollToY(self, newBottom):
        self.ax.set_ylim(
            self._moveLimTo(self.ylim(), newBottom)
        )
        self.draw()

    def scrollToX(self, newLeft):
        self.ax.set_xlim(
            self._moveLimTo(self.xlim(), newLeft)
        )
        self.draw()

    def toggleTriggerLine(self):
        self.config.triggerLineVisible = not self.config.triggerLineVisible

    def toggleCursorLine(self, index):
        self.config.cursorVisible[index] = not self.config.cursorVisible[index]

    def toggleVerticalCursorLine(self, index):
        self.config.verticalCursorVisible[index] = not self.config.verticalCursorVisible[index]

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _moveLimTo(self, lim, newLeft):
        return (newLeft, newLeft + lim[1] - lim[0])

    def _moveLim(self, lim, value, max):
        """If value > 0 zoom in else zoom out."""
        left, right = lim
        leftMax, rightMax = max
        newLeft = left + value
        newLeft = newLeft if newLeft >= leftMax else leftMax

        newRight = right - value
        newRight = newRight if newRight <= rightMax else rightMax

        return (newLeft, newRight)

    def _init_fig(self):
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        ax.set_xlabel('time (ms)')
        ax.set_ylabel('voltage')
        ax.set_xlim(*self.config.timeLimMs)
        ax.set_ylim(*self.config.voltageLim)

        return fig, ax

    def new_frame_seq(self):
        return iter(range(self.n.size + 20))

    def _init_draw(self):
        pass

    def _draw_frame(self, framedata):
        self.dataLine.set_data(
            self.n[0:len(self.y)], self.y)

        # Draw horizontal lines for trigger.
        if self.config.triggerLineVisible:
            self.triggerLine.set_y(self.config.trigger)
            self.nextTriggerDashedLine.set_y(self.config.nextTriggerIndicator)
        else:
            self.triggerLine.set_invisible()
            self.nextTriggerDashedLine.set_invisible()

        for i, cursorVisible in enumerate(self.config.cursorVisible):
            if cursorVisible:
                self.cursorLines[i].set_y(self.config.cursorVoltage[i])
            else:
                self.cursorLines[i].set_invisible()

        for i, verticalCursorVisible in enumerate(self.config.verticalCursorVisible):
            if verticalCursorVisible:
                self.verticalCursorLines[i].set_x(
                    self.config.verticalCursorTime[i])
            else:
                self.verticalCursorLines[i].set_invisible()

        self._drawn_artists = [
            self.dataLine,
            self.triggerLine,
            self.nextTriggerDashedLine,
            *self.cursorLines,
            *self.verticalCursorLines
        ]

        for l in self._drawn_artists:
            l.set_animated(True)
