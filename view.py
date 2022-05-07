import matplotlib
import numpy as np
from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from PyQt5.QtWidgets import QMainWindow, QWidget

from ui.displayscreen import Ui_Form as DisplayScreen
from ui.mainwindow import Ui_MainWindow as MainWindow

matplotlib.use("Qt5Agg")


class CustomFigCanvas(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.addedData = []
        print('Matplotlib Version:', matplotlib.__version__)

        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        self.y = (self.n * 0.0) + 50

        # The window
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)

        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('raw data')
        self.line1 = Line2D([], [], color='blue')
        self.ax1.add_line(self.line1)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(0, 100)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=50, blit=True)

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1,]
        for l in lines:
            l.set_data([], [])

    def addData(self, value):
        # self.addedData.append(value)
        # print(f"data added, {value}")
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
        margin = 2
        while(len(self.addedData) > 0):
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0]
            del(self.addedData[0])

        self.line1.set_data(
            self.n[0:self.n.size - margin], self.y[0:self.n.size - margin])
        self._drawn_artists = [self.line1,]
        for l in self._drawn_artists:
            l.set_animated(True)


class OscilloscopeUi(QMainWindow):
    """MPS Oscilloscope's view (GUI)."""

    def __init__(self) -> None:
        """View initializer."""
        super().__init__()
        self.mainwindow = MainWindow()
        self.mainwindow.setupUi(self)

        page1 = QWidget()

        displayScreen = DisplayScreen()
        displayScreen.setupUi(page1)

        placeholder = displayScreen.plotPlaceHolder
        self.canvas = CustomFigCanvas()

        containing_layout = placeholder.parent().layout()
        containing_layout.replaceWidget(placeholder, self.canvas)

        self.mainwindow.display.addWidget(page1)
        self.mainwindow.display.setCurrentWidget(page1)

        page2 = QWidget()
        self.mainwindow.display.addWidget(page2)

    def switchToPage(self, index):
        self.mainwindow.display.setCurrentIndex(index)

    def setDisplayWaveform(self, data):
        pass

    def displayWaveform(self):
        """Get display's waveform"""
        pass

    def clearDisplay(self):
        pass
