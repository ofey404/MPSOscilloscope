from dataclasses import dataclass
from PyQt5.QtWidgets import QMessageBox


@dataclass
class ScrollBarStepConverter:
    """Scroll bar only accept integer as step.
       A helper for scaling on axis.
    """
    maxStep: int = 1000

    def limFloatToInt(self, lim, maxLim):
        maxIntLim = (0, self.maxStep)
        fStep = (maxLim[1] - maxLim[0]) / self.maxStep
        intLim = [
            int((lim[0] - maxLim[0]) / fStep),
            int((lim[1] - maxLim[0]) / fStep),
        ]
        return intLim, maxIntLim

    def intStepValueToFloat(self, intStepValue, maxlim):
        maxRange = maxlim[1] - maxlim[0]
        return (intStepValue / self.maxStep) * maxRange + maxlim[0]

def showError(info: str):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText(info)
    msg.setWindowTitle("Error")
    msg.exec_()
