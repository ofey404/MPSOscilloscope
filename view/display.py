import logging

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


class OscilloscopeDisplay(FigureCanvas, TimedAnimation):
    def __init__(self, config: DisplayConfig):
        logger.info(f"Matplotlib Version: {matplotlib.__version__}")

        self.config = config

        # 2 times longer than minimal data length passed by trigger.
        self.n = np.linspace(
            0, self.config.timeLimMs[1] * 2, self.config.dataPointCount * 2 + 1)

        self.y = (self.n * 0.0) + 50
        self.trigger = 0
        self.nextTriggerIndicator = 0

        # The window
        self.fig, self.ax = self._init_fig()

        self.dataLine = Line2D([], [], color='blue')
        self.triggerLine = Line2D([], [], color='red')
        self.nextTriggerDashedLine = Line2D(
            [], [], color='red', linestyle="--")

        self.ax.add_line(self.dataLine)
        self.ax.add_line(self.triggerLine)
        self.ax.add_line(self.nextTriggerDashedLine)

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
        self.trigger = volt

    def updateNextTriggerIndicator(self, volt):
        self.nextTriggerIndicator = volt

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
        self.triggerLine.set_data(
            self.xlim(), [self.trigger] * 2)
        self.nextTriggerDashedLine.set_data(
            self.xlim(), [self.nextTriggerIndicator] * 2)

        self._drawn_artists = [self.dataLine,
                               self.triggerLine, self.nextTriggerDashedLine]
        for l in self._drawn_artists:
            l.set_animated(True)
