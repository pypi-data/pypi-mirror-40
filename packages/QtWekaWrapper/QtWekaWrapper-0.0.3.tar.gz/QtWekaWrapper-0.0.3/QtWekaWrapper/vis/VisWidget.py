
from PyQt5.QtCore import pyqtSignal, QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter
from data import Relation
from abc import abstractmethod


class VisWidget(QGraphicsView):
    plotPaletteChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.relation = None
        self.plotPalette = None
        self.setRenderHint(QPainter.Antialiasing)

    def setRelation(self, rel: Relation):
        """
        Initialize widget with L{data.Relation}
        @param rel: data to be visualized
        """
        self.relation = rel
        self.relation.dataChanged.connect(self.updateWidget)

    def setPlotPalette(self, paletteDict):
        """
        Set color palette for lines and points.

        @param paletteDict: dict with class names as keys and L{QColor} objects as values
        """
        self.plotPalette = paletteDict
        self.plotPaletteChanged.emit()

    def resizeEvent(self, event):
        if self.scene():
            s = event.size()
            self.scene().setSceneRect(QRectF(QPointF(0, 0), QPointF(s.width(), s.height())))
        super().resizeEvent(event)

    @abstractmethod
    def updateWidget(self):
        """
        Called when a new relation has been loaded.
        Implement this method in your subclasses.
        """
        pass
