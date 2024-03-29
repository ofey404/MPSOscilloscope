import logging
from view.display import OscilloscopeDisplay
from view.utils import ScrollBarStepConverter
from PyQt5.QtWidgets import QScrollBar, QDoubleSpinBox, QPushButton

logger = logging.getLogger(__name__)

class DisplayZoomControl:
    def __init__(self,
                 display: OscilloscopeDisplay,
                 scrollBarX: QScrollBar,
                 scrollBarY: QScrollBar,
                 zoomSpinBoxX: QDoubleSpinBox,
                 zoomSpinBoxY: QDoubleSpinBox,
                 zoomInButtonX: QPushButton,
                 zoomInButtonY: QPushButton,
                 zoomOutButtonX: QPushButton,
                 zoomOutButtonY: QPushButton,
                 zoomResetButtonX: QPushButton,
                 zoomResetButtonY: QPushButton,
                 ) -> None:

        self.display = display
        self.scrollBarX = scrollBarX
        self.scrollBarY = scrollBarY
        self.scrollBarConverter = ScrollBarStepConverter()
        self.zoomSpinBoxX = zoomSpinBoxX
        self.zoomSpinBoxY = zoomSpinBoxY
        self.zoomInButtonX = zoomInButtonX
        self.zoomInButtonY = zoomInButtonY
        self.zoomOutButtonX = zoomOutButtonX
        self.zoomOutButtonY = zoomOutButtonY
        self.zoomResetButtonX = zoomResetButtonX
        self.zoomResetButtonY = zoomResetButtonY

        self.repaintAllScrollBar()
        self._connectSignals()

    def repaintAllScrollBar(self):
        def rawRepaint(bar, lim, maxLim, value):
            pageStep = lim[1] - lim[0]
            bar.setMinimum(maxLim[0])
            bar.setMaximum(maxLim[1]-pageStep)
            bar.setPageStep(pageStep)
            bar.setValue(value)

        def convertToFixedIntAndPaint(bar, lim, maxLim):
            lim, maxLim = self.scrollBarConverter.limFloatToInt(lim, maxLim)
            rawRepaint(
                bar, lim, maxLim, value=lim[0]
            )

        convertToFixedIntAndPaint(
            bar=self.scrollBarX,
            lim=self.display.xlim(),
            maxLim=self.display.config.timeLimMs(),
        )

        convertToFixedIntAndPaint(
            bar=self.scrollBarY,
            lim=self.display.ylim(),
            maxLim=self.display.config.voltageLim,
        )

        logger.debug("All scrollbar repainted.")


    def recalculateDefaultZoomStep(self):
        xlim, ylim = self.display.config.timeLimMs(), self.display.config.voltageLim
        self.zoomSpinBoxX.setValue((xlim[1] - xlim[0]) / 10)
        self.zoomSpinBoxY.setValue((ylim[1] - ylim[0]) / 10)
        logger.debug("recalculateDefaultZoomStep")

    # ============================================================
    #                  Internal Methods
    # ============================================================

    def _connectSignals(self):
        self.zoomInButtonY.clicked.connect(self._zoomInYBySpinBox)
        self.zoomOutButtonY.clicked.connect(self._zoomOutYBySpinBox)
        self.zoomResetButtonY.clicked.connect(self._resetZoomY)
        self.zoomInButtonX.clicked.connect(self._zoomInXBySpinBox)
        self.zoomOutButtonX.clicked.connect(self._zoomOutXBySpinBox)
        self.zoomResetButtonX.clicked.connect(self._resetZoomX)

        # Display follow the scroll bar.
        # FIXME: Use `valueChanged` may cause serious performance issue.
        #        Since it repaint the display each step during slide.
        self.scrollBarX.valueChanged.connect(self._scrollToIntX)
        self.scrollBarY.valueChanged.connect(self._scrollToIntY)

    def _resetZoomY(self):
        self.display.resetZoomY()
        self.repaintAllScrollBar()

    def _resetZoomX(self):
        self.display.resetZoomX()
        self.repaintAllScrollBar()

    def _scrollToIntY(self, i):
        intY = self.scrollBarConverter.intStepValueToFloat(
            i, self.display.config.voltageLim)
        self.display.scrollToY(intY)

    def _scrollToIntX(self, i):
        intX = self.scrollBarConverter.intStepValueToFloat(
            i, self.display.config.timeLimMs())
        self.display.scrollToX(intX)

    def _zoomInYBySpinBox(self):
        self._zoomYBySpinBox(zoomIn=True)

    def _zoomOutYBySpinBox(self):
        self._zoomYBySpinBox(zoomIn=False)

    def _zoomInXBySpinBox(self):
        self._zoomXBySpinBox(zoomIn=True)

    def _zoomOutXBySpinBox(self):
        self._zoomXBySpinBox(zoomIn=False)

    def _zoomYBySpinBox(self, zoomIn: bool):
        value = self.zoomSpinBoxY.value()
        if not zoomIn:
            value = - value
        self.display.zoomY(value)
        self.repaintAllScrollBar()

    def _zoomXBySpinBox(self, zoomIn: bool):
        value = self.zoomSpinBoxX.value()
        if not zoomIn:
            value = - value
        self.display.zoomX(value)
        self.repaintAllScrollBar()
