# This Python file uses the following encoding: utf-8
from mainwindow import Ui_MainWindow as MainWindow
from displayscreen import Ui_Form as DisplayScreen
import sys
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
from matplotlib.lines import Line2D
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget
from matplotlib.animation import TimedAnimation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("Qt5Agg")


class DataAcquisitionWorker(QObject):
    updated = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        ...


class CustomFigCanvas(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.addedData = []
        print('Matplotlib Version:', matplotlib.__version__)

        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)
        self.y = (self.n * 0.0) + 50

        # The window
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)

        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('raw data')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='red', linewidth=2)
        self.line1_head = Line2D(
            [], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(0, 100)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=50, blit=True)

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])

    def addData(self, value):
        self.addedData.append(value)

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom, top)
        self.draw()

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
        self.line1_tail.set_data(np.append(
            self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]
        for l in self._drawn_artists:
            l.set_animated(True)


class OscilloscopeUi(QMainWindow):
    """MPS Oscilloscope's view (GUI)."""

    def __init__(self) -> None:
        """View initializer."""
        super().__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)

        page1 = QWidget()

        displayScreen = DisplayScreen()
        displayScreen.setupUi(page1)

        placeholder = displayScreen.plotPlaceHolder
        new_widget = CustomFigCanvas()

        containing_layout = placeholder.parent().layout()
        containing_layout.replaceWidget(placeholder, new_widget)

        self.ui.display.addWidget(page1)
        self.ui.display.setCurrentWidget(page1)

        page2 = QWidget()
        self.ui.display.addWidget(page2)

    def switchToPage(self, index):
        self.ui.display.setCurrentIndex(index)

    def setDisplayWaveform(self, data):
        pass

    def displayWaveform(self):
        """Get display's waveform"""
        pass

    def clearDisplay(self):
        pass



class OscilloscopeModel:
    """MPS Oscilloscope's model."""

    def __init__(self):
        pass

class OscilloscopeCtrl:
    """MPS Oscilloscope's controller class."""

    def __init__(self, model: OscilloscopeModel, view: OscilloscopeUi):
        self.model = model
        self.view = view

        self._connectSignals()

    def _connectSignals(self):
        self.view.ui.actionDisplay.triggered.connect(lambda: self.view.switchToPage(1))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = OscilloscopeUi()
    view.show()
    model = OscilloscopeModel()
    OscilloscopeCtrl(model, view)
    sys.exit(app.exec_())
