# This Python file uses the following encoding: utf-8
import sys
from tkinter.tix import WINDOW
import typing
from PyQt5 import QtCore
from PySide2.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow

from mainwindow import Ui_MainWindow


class OscilloscopeUi(QMainWindow):
    """MPS Oscilloscope's view (GUI)"""

    def __init__(self) -> None:
        super().__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OscilloscopeUi()
    window.show()
    sys.exit(app.exec_())
