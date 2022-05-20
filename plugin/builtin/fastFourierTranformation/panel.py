from view.utils import replaceWidget
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.figure import Figure
from .processor import FFTData
from PyQt5.QtWidgets import QWidget
from .ui.fft import Ui_Form as FFT
from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas


class FFTDisplay(FigureCanvas, TimedAnimation):
    def __init__(self):
        # The window
        self.fig, self.ax = self._init_fig()

        self.x = [0, 1]
        self.y = [0, 1]
        self.line = Line2D(self.x, self.y)
        self.ax.add_line(self.line)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=50, blit=True)

    def _init_fig(self):
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        ax.set_xlabel('time (ms)')
        ax.set_ylabel('voltage')

        return fig, ax

    def _init_draw(self):
        pass

    def new_frame_seq(self):
        return iter(range(len(self.x) + 20))

    def _draw_frame(self, framedata):
        self._drawn_artists = [
            self.line
        ]

        for l in self._drawn_artists:
            l.set_animated(True)


class FFTPanel:
    def __init__(self) -> None:
        self.uiForm = FFT()
        self.widget: FFT = QWidget()
        self.uiForm.setupUi(self.widget)
        self.display = FFTDisplay()
        replaceWidget(self.uiForm.FFTPlaceholder, self.display)

    def getWidget(self) -> QWidget:
        return self.widget

    def updateByData(self, data: FFTData):
        self.uiForm.vTopDoubleSpinBox.setValue(data.vTop)
