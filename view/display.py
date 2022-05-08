import logging

import matplotlib
import numpy as np
from attr import dataclass
from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from model.worker import BUFFER_SIZE

matplotlib.use("Qt5Agg")
logger = logging.getLogger(__name__)


@dataclass
class DisplayConfig:
    drawTrigger: bool = None


class OscilloscopeDisplay(FigureCanvas, TimedAnimation):
    def __init__(self):
        logger.info(f"Matplotlib Version: {matplotlib.__version__}")

        # The data
        self.xlim = BUFFER_SIZE // 2
        self.n = np.linspace(0, BUFFER_SIZE - 1, BUFFER_SIZE)
        self.y = (self.n * 0.0) + 50
        self.trigger = 0
        self.nextTriggerIndicator = 0

        # The window
        self.fig, self.ax = self._init_fig()

        self.dataLine = Line2D([], [], color='blue')
        self.triggerLine = Line2D([], [], color='red')
        self.nextTriggerDashedLine = Line2D([], [], color='red', linestyle="--")

        self.ax.add_line(self.dataLine)
        self.ax.add_line(self.triggerLine)
        self.ax.add_line(self.nextTriggerDashedLine)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=50, blit=True)
        logger.info("View inited.")

    def updateData(self, value):
        self.y = value

    def adjustTrigger(self, volt):
        self.trigger = volt

    def adjustNextTriggerIndicator(self, volt):
        self.nextTriggerIndicator = volt

    def updateConfig(self, config: DisplayConfig):
        ...

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _init_fig(self):
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        ax.set_xlabel('time')
        ax.set_ylabel('raw data')
        ax.set_xlim(0, self.xlim - 1)
        ax.set_ylim(-1, 1)

        return fig, ax

    def new_frame_seq(self):
        return iter(range(self.n.size + 20))

    def _init_draw(self):
        pass

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass

    def _draw_frame(self, framedata):
        self.dataLine.set_data(
            self.n[0:len(self.y)], self.y)
        self.triggerLine.set_data(
            [0, BUFFER_SIZE], [self.trigger, self.trigger])
        self.nextTriggerDashedLine.set_data(
            [0, BUFFER_SIZE], [self.nextTriggerIndicator, self.nextTriggerIndicator])
        self._drawn_artists = [self.dataLine, self.triggerLine, self.nextTriggerDashedLine]
        for l in self._drawn_artists:
            l.set_animated(True)
