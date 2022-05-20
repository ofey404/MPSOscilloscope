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

        self.freq = [0, 1]
        self.real = [0, 1]

        self.realLine = Line2D(self.freq, self.real)
        self.ax.add_line(self.realLine)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=50, blit=True)

    def _init_fig(self):
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        ax.set_xlabel('Freq')
        ax.set_ylabel('Real')

        return fig, ax

    def updateData(self, data: FFTData):
        self.ax.set_ylim((min(data.real), max(data.real)))
        self.ax.set_xlim((min(data.freq), max(data.freq)))
        self.realLine.set_data(
            data.freq, data.real,
        )

    def _init_draw(self):
        pass

    def new_frame_seq(self):
        return iter(range(len(self.freq) + 20))

    def _draw_frame(self, framedata):
        self._drawn_artists = [
            self.realLine,
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
        self.display.updateData(data)
