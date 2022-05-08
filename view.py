import matplotlib
import numpy as np
from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from PyQt5.QtWidgets import QMainWindow, QWidget

from ui.mainwindow import Ui_MainWindow as MainWindow
from model.worker import BUFFER_SIZE
import logging

matplotlib.use("Qt5Agg")


logger = logging.getLogger(__name__)


class CustomFigCanvas(FigureCanvas, TimedAnimation):
    def __init__(self):
        print('Matplotlib Version:', matplotlib.__version__)

        # The data
        self.xlim = BUFFER_SIZE // 2
        self.n = np.linspace(0, BUFFER_SIZE - 1, BUFFER_SIZE)
        self.y = (self.n * 0.0) + 50
        self.trigger = 0

        # The window
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)

        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('raw data')
        self.dataLine = Line2D([], [], color='blue')
        self.triggerLine = Line2D([], [], color='red')

        self.ax1.add_line(self.dataLine)
        self.ax1.add_line(self.triggerLine)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(-1, 1)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=50, blit=True)
        logger.info("View inited.")

    def new_frame_seq(self):
        return iter(range(self.n.size + 20))

    def _init_draw(self):
        pass

    def addData(self, value):
        self.y = value

    def adjustTrigger(self, volt):
        self.trigger = volt

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
        self.triggerLine.set_data([0, BUFFER_SIZE], [self.trigger, self.trigger])
        self._drawn_artists = [self.dataLine, self.triggerLine]
        for l in self._drawn_artists:
            l.set_animated(True)


class OscilloscopeUi(QMainWindow):
    """MPS Oscilloscope's view (GUI)."""

    def __init__(self) -> None:
        """View initializer."""
        super().__init__()
        self.mainwindow = MainWindow()
        self.mainwindow.setupUi(self)

        self.canvas = CustomFigCanvas()

        # containing_layout = placeholder.parent().layout()
        # containing_layout.replaceWidget(placeholder, self.canvas)
        self._replaceWidget(self.mainwindow.plotPlaceHolder, self.canvas)

    def _replaceWidget(self, placeholder: QWidget, new: QWidget):
        containing_layout = placeholder.parent().layout()
        containing_layout.replaceWidget(placeholder, new)

    def setDisplayWaveform(self, data):
        pass

    def displayWaveform(self):
        """Get display's waveform"""
        pass

    def clearDisplay(self):
        pass
