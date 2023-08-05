from __future__ import print_function, absolute_import, unicode_literals

from abc import abstractmethod
import sys
import re
import os
import os.path
import math
from traceback import print_exception

from PyQt5.QtWidgets import *
from PyQt5.QtGui import (
    QColor, 
    QPalette, 
    QFontMetrics, 
    QImage, 
    QPainter, 
    QDesktopServices, 
    QTransform, 
    QFont, 
    QPen, 
    QCursor, 
    QVector2D,
)
from PyQt5.QtCore import (
    Qt, 
    QSize, 
    QUrl, 
    QObject, 
    pyqtSignal, 
    QRectF, 
    QPointF,
)
from PyQt5.QtCore import *


BP = os.path.dirname(os.path.abspath(__file__))


class WekaVisualizer(QWidget):
    defaultPalette = [
        QColor(255, 30, 0, 100),
        QColor(61, 28, 227, 100),
        QColor(255, 205, 0, 100),
        QColor(0, 232, 61, 100),
        QColor(240, 63, 40, 100),
        QColor(65, 45, 166, 100),
        QColor(240, 200, 40, 100),
        QColor(30, 179, 69, 100)
    ]

    def __init__(self):
        super().__init__()

        self._plotPalette = {}

        self.globalLayout         = QHBoxLayout()
        self.controlLayout        = QVBoxLayout()
        self.dynamicControlLayout = QVBoxLayout()
        self.plotLayout           = QVBoxLayout()
        self.plot                 = StarPlot()

        self.colorDialog = QColorDialog()
        self.colorDialog.setOption(QColorDialog.ShowAlphaChannel, True)

        self.activeSwatch = None

        self.selectionStatBars = []

        self.initUI()

    def initUI(self):
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle(self.tr("WEKA Visualizer"))

        loadButton = QPushButton(self.tr("Load ARFF"))
        loadButton.clicked.connect(self.showInputFileDialog)

        self.controlLayout.addWidget(loadButton)
        self.controlLayout.addLayout(self.dynamicControlLayout)
        self.controlLayout.addStretch(1)

        self.plotLayout.addWidget(self.plot)

        self.globalLayout.addLayout(self.controlLayout, 1)
        self.globalLayout.addLayout(self.plotLayout, 5)

        self.setLayout(self.globalLayout)

        self.show()

    def addControlArea(self):
        # clear layout first
        for i in reversed(range(self.dynamicControlLayout.count())):
            self.dynamicControlLayout.itemAt(i).widget().setParent(None)

        self._addPlotControls()
        self._addPlotSelectionStats()
        self._addOptions()

    def _addPlotControls(self):
        # classes selector
        groupClasses = QGroupBox(self.tr("Classes"))
        classesVBox = QVBoxLayout()
        groupClasses.setLayout(classesVBox)

        self._plotPalette.clear()

        for i, c in enumerate(self.plot.relation.allClasses):
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignLeft)

            checkBox = QCheckBox()
            checkBox.dataClassLabel = c
            checkBox.setObjectName("class" + str(i))
            checkBox.setChecked(True)
            checkBox.stateChanged.connect(self.toggleClassState)
            hbox.addWidget(checkBox)

            swatch = QPushButton()
            swatch.dataClassLabel = c
            swatch.setObjectName("swatch_class" + str(i))
            swatch.setFocusPolicy(Qt.NoFocus)
            swatch.setFixedSize(QSize(30, 30))
            swatch.clicked.connect(self.selectClassColor)
            color = self.defaultPalette[i % len(self.defaultPalette)]
            self._plotPalette[c] = color
            self._setSwatchColor(swatch, color)
            hbox.addWidget(swatch)

            label = QLabel(c)
            label.dataClassLabel = c
            label.setTextFormat(Qt.PlainText)
            label.setObjectName("label_class" + str(i))
            label.setBuddy(swatch)
            hbox.addWidget(label)

            classesVBox.addLayout(hbox)

        self.plot.setPlotPalette(self._plotPalette)
        self.dynamicControlLayout.addWidget(groupClasses)

    def _setSwatchColor(self, swatch, color):
        pal = swatch.palette()
        pal.setColor(QPalette.Button, color)
        swatch.setPalette(pal)
        swatch.setStyleSheet("background-color: rgba({}, {},{},{}); border: 1px solid lightgray; border-radius: 2px".format(
            color.red(), color.green(), color.blue(), color.alpha()
        ))

    def toggleClassState(self, state):
        s = self.sender()
        p = s.parent()
        name = s.objectName()
        state = (state != Qt.Unchecked)
        p.findChild(QWidget, "swatch_" + name).setEnabled(state)
        p.findChild(QWidget, "label_" + name).setEnabled(state)

        if state:
            #self.plot.relation.setClassFilter(self.plot.relation.activeClasses | {s.dataClassLabel})
            self.plot.filterClasses(self.plot.activeClasses  | {s.dataClassLabel})
        else:
            #self.plot.relation.setClassFilter(self.plot.relation.activeClasses - {s.dataClassLabel})
            self.plot.filterClasses(self.plot.activeClasses  - {s.dataClassLabel})

    def _addPlotSelectionStats(self):
        self.selectionStatBars.clear()

        groupStats = QGroupBox(self.tr("Selection by Class"))
        statsVBox = QVBoxLayout()
        groupStats.setLayout(statsVBox)

        for c in self.plot.relation.allClasses:
            bar = QProgressBar()
            bar.dataClassLabel = c
            bar.setTextVisible(True)
            bar.setValue(0)
            self.selectionStatBars.append(bar)

            label = QLabel(c)
            label.setBuddy(bar)

            vbox = QVBoxLayout()
            vbox.addWidget(label)
            vbox.addWidget(bar)
            statsVBox.addLayout(vbox)

        self.plot.selectionChanged.connect(self.updateSelectionStats)
        self.updateSelectionStats()
        self.dynamicControlLayout.addWidget(groupStats)

    def updateSelectionStats(self):
        highlightsPerClass = {}
        for s in self.plot.highlightedRings:
            highlightsPerClass[s.dataClassLabel] = highlightsPerClass.get(s.dataClassLabel, 0) + 1

        for b in self.selectionStatBars:
            num = self.plot.relation.numDatasetsForClass(b.dataClassLabel)
            if 0 != num:
                b.setValue(highlightsPerClass.get(b.dataClassLabel, 0) / num * 100)
            color = self._plotPalette[b.dataClassLabel]
            pal = b.palette()
            pal.setColor(QPalette.Highlight, color)
            b.setPalette(pal)
            margin = QFontMetrics(b.font()).width("100%") + 5
            # thank you Windows, for letting me re-style the full progress bar instead of just using the palette color!!
            b.setStyleSheet("QProgressBar {{ text-align: right; border: 1px solid lightgray;"
                            "background:none; border-radius: 2px; margin-right: {}px; }}"
                            "QProgressBar::chunk {{ background-color: rgba({}, {}, {}, {});  }}".format(
                margin, color.red(), color.green(), color.blue(), color.alpha()))

    def _addOptions(self):
        groupOpts = QGroupBox(self.tr("Options"))
        optsVBox = QVBoxLayout()
        groupOpts.setLayout(optsVBox)

        # feature scaling
        scaleHBox = QHBoxLayout()
        scaleHBox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        scaleOpt = QCheckBox()
        scaleOpt.setChecked(True)
        scaleOpt.stateChanged.connect(self.toggleScaleMode)
        scaleLabel = QLabel(self.tr("&Scale features"))
        scaleLabel.setBuddy(scaleOpt)
        scaleHBox.addWidget(scaleOpt)
        scaleHBox.addWidget(scaleLabel)
        optsVBox.addLayout(scaleHBox)

        self.dynamicControlLayout.addWidget(groupOpts)

        # save button
        saveButton = QPushButton(self.tr("Save image"))
        saveButton.clicked.connect(self.saveImage)
        self.dynamicControlLayout.addWidget(saveButton)

    def toggleScaleMode(self, state):
        self.plot.relation.setScaleMode(Relation.ScaleModeLocal if state != Qt.Unchecked else Relation.ScaleModeGlobal)

    def selectClassColor(self):
        s = self.sender()
        self.activeSwatch = s
        self.colorDialog.setCurrentColor(s.palette().color(QPalette.Button))
        self.colorDialog.open(self.setNewClassColor)

    def setNewClassColor(self):
        color = self.sender().currentColor()
        if self.activeSwatch is not None:
            self._setSwatchColor(self.activeSwatch, color)

            className = self.activeSwatch.dataClassLabel
            self._plotPalette[className] = color
            self.plot.setPlotPalette(self._plotPalette)

    def saveImage(self):
        fileName = QFileDialog.getSaveFileName(self, self.tr("Select save location"),
                                               "", self.tr("Images (*.png *.jpg *.bmp *.xpm)"))
        if "" != fileName[0] and os.path.isdir(os.path.dirname(fileName[0])):
            imgSize = QSize(self.plot.scene().width() * 4, self.plot.scene().height() * 4)
            img = QImage(imgSize, QImage.Format_ARGB32)
            img.fill(Qt.transparent)
            painter = QPainter(img)
            self.plot.render(painter)
            img.save(fileName[0])
            del painter
            QDesktopServices.openUrl(QUrl("file:///" + fileName[0], QUrl.TolerantMode))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showInputFileDialog(self):
        fileName = QFileDialog.getOpenFileName(self, self.tr("Select WEKA ARFF file"),
                                               "", self.tr("WEKA Files (*.arff)"))
        if "" != fileName[0] and os.path.isfile(fileName[0]):
            try:
                rel = RelationFactory.loadFromFile(fileName[0])
                if len(rel.fieldNames) == 0:
                    raise Exception("No fields")
            except:
                QMessageBox.critical(self, self.tr("Input file error"),
                                     self.tr("The specified input file is either not a valid WEKA ARFF file or "
                                             "does not contain any NUMERIC columns"), QMessageBox.Ok)
                return

            self.plot.setRelation(rel)
            self.addControlArea()
            self.plot.updateWidget()


# override excepthook to correctly show tracebacks in PyCharm
def excepthook(extype, value, traceback):
    print_exception(extype, value, traceback)
    exit(1)

sys.excepthook = excepthook

def run_qt_window():
    app = QApplication(sys.argv)
    vis = WekaVisualizer()
    sys.exit(app.exec_())

class RelationFactory(object):
    @staticmethod
    def loadFromFile(fileName):
        """Load information about a dataset from a file and return a object which have all the necessary properties to generate the predictions.

           :param fileName: The dataset file name.
        """
        rel = Relation()

        with open(fileName, "r") as f:
            lines = f.readlines()

            try:
                relName = ""
                fieldNames   = []
                fieldTypes   = []
                dataPart     = False
                datasets     = []
                classColName = None
                skipCols     = []
                skipCounter  = 0
                for l in lines:
                    l = l.strip()
                    if "" == l or "%" == l[0]:
                        continue

                    if "@" == l[0]:
                        if not dataPart:
                            fields = re.split("\s+", l.strip())
                            if "@RELATION" == fields[0].upper():
                                relName = fields[1]
                            elif "@ATTRIBUTE" == fields[0].upper():
                                if "NUMERIC" == fields[2].upper() or "REAL" == fields[2].upper():
                                    fieldTypes.append(float)
                                    fieldNames.append(fields[1])
                                else:
                                    classColName = fields[1]
                                    skipCols.append(skipCounter)
                                skipCounter += 1
                            elif "@DATA" == fields[0].upper():
                                if len(fieldNames) != 0:
                                    if classColName is None:
                                        # class column is numeric, but we need a string
                                        classColName = fieldNames[-1]
                                        fieldTypes[-1] = str
                                    else:
                                        skipCols.pop()  # last column is class column, don't skip it
                                        fieldNames.append(classColName)
                                        fieldTypes.append(str)
                                    dataPart = True
                                    rel.relName = relName
                                    rel.fieldNames = fieldNames
                    elif dataPart:
                        fieldsTmp = re.split(",", l.strip())
                        fields = []
                        for i, f_ in enumerate(fieldsTmp):
                            if i not in skipCols:
                                fields.append(f_)

                        for i, t in enumerate(fieldTypes):
                            fields[i] = t(fields[i])

                        if len(fields) > 1:
                            rel.allClasses.add(fields[-1])
                            datasets.append(fields)
                rel.datasets = datasets
                rel.numDatasets = len(datasets)
                rel.activeClasses = set(rel.allClasses)
            except:
                raise Exception("ARFF parsing error!")

        return rel


class Relation(QObject):
    dataChanged = pyqtSignal()

    ScaleModeGlobal = 0
    ScaleModeLocal  = 2

    def __init__(self):
        super().__init__()

        self.relName            = ""
        self.__fieldNames       = []
        self.__fieldNamesAll    = []
        self.__datasets         = []
        self.__datasetsAll      = []
        self.__datasetsPerClass = {}
        self.allClasses         = set()
        self.activeClasses      = set()
        self.numDatasets        = 0

        self.__scaled_datasets = None
        self.__scale_mode       = self.ScaleModeLocal

        self.__minVals = None
        self.__maxVals = None

        self.__axisDomains = None

    @property
    def fieldNames(self):
        """
        Getter for field names. DO NOT use direct list access operations on the returned list as it will
        mess up data filtering. Use the setter to replace the full list instead.
        """
        return self.__fieldNames

    @fieldNames.setter
    def fieldNames(self, names):
        self.__fieldNamesAll = names
        self.__fieldNames = list(names)
        self.dataChanged.emit()

    @property
    def datasets(self):
        return self.__datasets

    @datasets.setter
    def datasets(self, datasets):
        """
        Getter for fdatasets. DO NOT use direct list access operations on the returned list as it will
        mess up data filtering. Use the setter to replace the full list instead.
        """
        self.__datasetsAll = datasets
        self.__datasets = list(datasets)
        self.__axisDomains = None
        for ds in self.__datasetsAll:
            self.__datasetsPerClass[ds[-1]] = self.__datasetsPerClass.get(ds[-1], 0) + 1
        self.dataChanged.emit()

    @property
    def axisDomains(self):
        if self.__axisDomains is None:
            if self.__scale_mode == self.ScaleModeLocal:
                self.__axisDomains = list(zip(self.minVals(), self.maxVals()))
            else:
                self.__axisDomains = [(min(self.minVals()), max(self.maxVals()))] * (len(self.fieldNames) - 1)

        return self.__axisDomains

    def numDatasetsForClass(self, cls):
        return self.__datasetsPerClass.get(cls, 0)

    def minVals(self):
        if self.__minVals is None:
            self.__calcMinMaxVals()
        return self.__minVals

    def maxVals(self):
        if self.__maxVals is None:
            self.__calcMinMaxVals()
        return self.__maxVals

    def __calcMinMaxVals(self):
        minVals = [float("inf")] * (len(self.fieldNames) - 1)
        maxVals = [float("-inf")] * (len(self.fieldNames) - 1)
        for ds in self.datasets:
            for i, d in enumerate(ds[:-1]):
                if type(d) != float:
                    continue

                minVals[i] = min(minVals[i], d)
                maxVals[i] = max(maxVals[i], d)

        if minVals[0] < float("inf"):
            self.__minVals = minVals
            self.__maxVals = maxVals

    def resetFilters(self):
        if len(self.__fieldNames) != len(self.__fieldNamesAll):
            self.__fieldNames = list(self.__fieldNames)

        if len(self.__datasets) != len(self.__datasetsAll):
            self.__datasets = list(self.__datasets)

        self.activeClasses = set(self.allClasses)
        self.__scaled_datasets = None

        self.dataChanged.emit()

    def setClassFilter(self, includeClasses):
        """
        Filter data by given class names.
        This method is kept here for preservation, but is basically obsolete. Filtering is done by toggling the
        visibility state of the drawn graphics items.

        @param includeClasses: class names to filter by
        """
        self.__datasets = [d for d in self.__datasetsAll if d[-1] in includeClasses]
        self.__scaled_datasets = None
        self.activeClasses = includeClasses
        self.dataChanged.emit()

    def setScaleMode(self, mode):
        """
        Set axis normalization/scaling mode
        @param mode: mode, L{ScaleModeLocal} or L{ScaleModeGlobal}
        """
        if mode != self.__scale_mode and mode in (self.ScaleModeGlobal, self.ScaleModeLocal):
            self.__scale_mode = mode
            self.__scaled_datasets = None
            self.__axisDomains = None
            self.dataChanged.emit()

    def getScaledDatasets(self, minOffset=.1, maxOffset=.1):
        if self.__scaled_datasets is None:
            self.__scaled_datasets = []

            if self.__scale_mode == self.ScaleModeGlobal:
                minVals = [min(self.minVals())] * (len(self.fieldNames) - 1)
                maxVals = [max(self.maxVals())] * (len(self.fieldNames) - 1)
            else:
                minVals = self.minVals()
                maxVals = self.maxVals()

            minVals = [x - maxVals[i] * minOffset for i, x in enumerate(minVals)]
            maxVals = [x + x * maxOffset for x in maxVals]

            for ds in self.datasets:
                self.__scaled_datasets.append([(x - minVals[i]) / (maxVals[i] - minVals[i]) if type(x) == float else x for i, x in enumerate(ds)])

        return self.__scaled_datasets

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

class StarPlot(VisWidget):
    """
    Radial star plot with multiple axes.
    """

    canvasAreaChanged = pyqtSignal()
    axisChanged = pyqtSignal()
    selectionChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__bgColor = QColor(255, 255, 255)
        self.scene().setBackgroundBrush(self.__bgColor)

        self.labelFont = QFont('Decorative', 8)

        self.class1Color = Qt.red
        self.class2Color = Qt.blue
        self.class1Pen   = QPen(self.class1Color)
        self.class2Pen   = QPen(self.class2Color)

        self.axes       = []
        self.axisAngles = []
        self.axisLabels = []
        self.lineGroups = []

        self.highlightedItems = set()
        self.highlightedRings = set()
        self.activeClasses    = set()

        # timer for delayed plot update on resize events
        self.resizeUpdateDelay = 150
        self.__resizeDelayTimer = QTimer(self)
        self.__resizeDelayTimer.timeout.connect(self.canvasAreaChanged.emit)

        self.selectionUpdateDelay = 200
        self.__selectionUpdateTimer = QTimer(self)
        self.__selectionUpdateTimer.timeout.connect(self.selectionChanged.emit)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.rubberBandChanged.connect(self.selectData)
        self.setCacheMode(QGraphicsView.CacheBackground)

        self.colorDialog = QColorDialog()

    @property
    def bgColor(self):
        """Get the background color.
        """
        return self.__bgColor

    @bgColor.setter
    def bgColor(self, color):
        """Set the bg color.
        """
        self.__bgColor = color
        self.scene().setBackgroundBrush(self.__bgColor)

    def getClassColor(self, cls):
        if self.plotPalette is None or cls not in self.plotPalette:
            return QColor()

        return self.plotPalette[cls]

    def setRelation(self, rel: Relation):
        super().setRelation(rel)
        self.activeClasses = self.relation.activeClasses

    def updateWidget(self):
        self.setUpdatesEnabled(False)

        if self.relation is None:
            return

        # save axis rotations, but only if we don't have a new dataset with a different number of axes
        self.axisAngles.clear()
        if len(self.axes) == len(self.relation.fieldNames) - 1:
            for a in self.axes:
                self.axisAngles.append(a.rotation())

        self.lineGroups.clear()
        self.highlightedItems.clear()
        self.highlightedRings.clear()
        self.axisLabels.clear()
        self.axes.clear()
        self.scene().clear()

        self.addAxes()
        self.addPoints()

        if self.axisAngles:
            self.reparentLines()

        self.setUpdatesEnabled(False)

    def addAxes(self):
        """Add a new axis to the graph.
        """
        numDims = len(self.relation.fieldNames) - 1
        angle = 360 / numDims
        axisDomains = self.relation.axisDomains
        for i in range(numDims):
            axis = PlotAxis(self)
            self.scene().addItem(axis)
            if self.axisAngles and i < len(self.axisAngles):
                axis.setRotation(self.axisAngles[i])
            else:
                axis.setRotation(angle * i)
            self.axes.append(axis)

            domain = axisDomains[i]
            text = PlotAxisLabel("{}\n[{:.2f},{:.2f}]".format(self.relation.fieldNames[i], domain[0], domain[1]))
            text.setFont(self.labelFont)
            self.axisLabels.append(text)
            text.setParentItem(axis)

    def addPoints(self):
        """Add a number of points to the graph.
        """
        numDims = len(self.relation.fieldNames) - 1
        datasets = self.relation.getScaledDatasets()
        for ds in datasets:
            points = []
            lines = []
            for i in range(numDims):
                p = PlotPoint(self, ds[i], ds[-1])
                p.setParentItem(self.axes[i])
                points.append(p)

                if 0 < i:
                    lines.append(PlotLine(self, points[i - 1], p))
                if i == numDims - 1:
                    lines.append(PlotLine(self, p, points[0]))

            group = self.scene().createItemGroup(lines)
            group.dataClassLabel = points[0].cls
            self.lineGroups.append(group)

    def reparentLines(self):
        for lg in self.lineGroups:
            lines = lg.childItems()
            lines = list(sorted(lines, key=lambda x: x.p1.parentItem().rotation()))

            numDims = len(lines)
            for i, l in enumerate(lines):
                l.p2 = lines[i + 1 if i + 1 < numDims else 0].p1

    def filterClasses(self, classes):
        """
        Filter classes without reloading the dataset.
        L{StarPlot.activeClasses} contains all currently active classes.

        @param classes class names to filter by
        """
        items = self.scene().items()
        for i in items:
            if type(i) == PlotLine or type(i) == PlotPoint:
                i.setVisible(i.cls in classes)

        self.activeClasses = classes

    def mouseDoubleClickEvent(self, event):
        self.colorDialog.setCurrentColor(self.bgColor)
        self.colorDialog.open(self._setBackgroundColor)

    def _setBackgroundColor(self):
        self.bgColor = self.sender().currentColor()

    def resizeEvent(self, event):
        self.setUpdatesEnabled(False)
        super().resizeEvent(event)
        # center scene in viewport
        r = self.rect()
        t = QTransform()
        t.translate(-r.width() / 2, -r.height() / 2)
        r = QRectF(QPointF(r.x(), r.y()) * t, QSizeF(r.width(), r.height()))
        self.setSceneRect(r)
        self.__resizeDelayTimer.start(self.resizeUpdateDelay)
        self.setUpdatesEnabled(True)

    def selectData(self, rubberBandRect, fromScenePoint, toScenePoint):
        """Use the coordinates to color the selected part of the graph. 
        """
        if fromScenePoint == toScenePoint:
            return

        if QApplication.keyboardModifiers() != Qt.ShiftModifier and QApplication.keyboardModifiers() != Qt.ControlModifier:
            # unselect all currently selected items
            for h in self.highlightedItems:
                h.highlighted = False
            self.highlightedItems.clear()
            self.highlightedRings.clear()

        sel = self.items(rubberBandRect)
        for s in sel:
            if type(s) == PlotLine:
                parent = s.parentItem()
                siblings = parent.childItems()

                if QApplication.keyboardModifiers() == Qt.ControlModifier:
                    for sib in siblings:
                        if sib in self.highlightedItems:
                            sib.highlighted = False
                            self.highlightedItems.remove(sib)
                    if parent in self.highlightedRings:
                        self.highlightedRings.remove(parent)
                else:
                    for sib in siblings:
                        sib.highlighted = True
                        self.highlightedItems.add(sib)
                    self.highlightedRings.add(parent)

        self.__selectionUpdateTimer.start(self.selectionUpdateDelay)

    def sizeHint(self):
        return QSize(1000, 1000)

    def minimumSizeHint(self):
        return QSize(400, 400)


class PlotAxis(QGraphicsObject):
    ItemAxisLenHasChanged = 0x9901

    def __init__(self, view):
        super().__init__()
        self.view = view

        self.p1 = QPoint(0, 0)
        self.p2 = QPoint(0, 0)

        self.paddingHoriz = 30
        self.paddingVert  = 60 + QFontMetrics(self.view.labelFont).height() * 2
        self.__canvasW = view.rect().size().width() - self.paddingHoriz
        self.__canvasH = view.rect().size().height() - self.paddingVert

        self.axesColor = QColor(150, 150, 150)
        self.axesWidth = 1
        self.axesWidthHighl = 3
        self.axisGrabbed = False
        self.axesPen = QPen(self.axesColor, self.axesWidth)

        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.__canvasMaxDim = 0
        self.__boundingRect = None

        # save original rotation during axis reordering
        self.__origRotation = self.rotation()
        self.__dragActive = False

        self.axisAnimation = QPropertyAnimation(self, b"relativeRotation")
        self.axisAnimation.setDuration(600)
        self.axisAnimation.setEasingCurve(QEasingCurve.InOutQuad)
        self.__relRotationStartValue = 0

        self.view.canvasAreaChanged.connect(self.updateCanvasGeometry)

    def initRelativeRotation(self):
        """
        When animating rotation using the L{relativeRotation}, call this method before
        starting the animation. Otherwise relative angles will be added up resulting in a much
        larger rotation than intended.
        """
        self.__relRotationStartValue = self.rotation()

    @pyqtProperty(float)
    def relativeRotation(self):
        """
        Q_PROPERTY for animating relative rotations. Fix the initial rotation first using
        L{initRelativeRotation()} before starting the animation.

        @return: current rotation
        """
        return self.rotation()

    @relativeRotation.setter
    def relativeRotation(self, rot):
        """
        Q_PROPERTY for animating relative rotations. Fix the initial rotation first using
        L{initRelativeRotation()} before starting the animation.
        """
        self.setRotation((self.__relRotationStartValue + rot) % 360)

    def hoverEnterEvent(self, event):
        self.axesPen.setWidth(self.axesWidthHighl)
        self.setCursor(Qt.PointingHandCursor)
        self.update()

    def hoverLeaveEvent(self, event):
        self.axesPen.setWidth(self.axesWidth)
        self.setCursor(Qt.ArrowCursor)
        self.update()

    def mousePressEvent(self, event):
        self.axisGrabbed = True
        self.setCursor(Qt.ClosedHandCursor)

        if not self.__dragActive:
            self.__origRotation = self.rotation()
            self.__dragActive = True

    def mouseMoveEvent(self, event):
        if self.__dragActive:
            mousePos = self.view.mapToScene(self.view.mapFromGlobal(QCursor.pos()))
            vec1 = QVector2D(mousePos)
            vec1.normalize()
            trans = QTransform()
            trans.rotate(self.rotation())
            vec2 = QVector2D(self.p2 * trans)
            vec2.normalize()
            angle = math.acos(max(-1, min(1, QVector2D.dotProduct(vec1, vec2)))) * 180 / math.pi

            # clockwise rotation
            if vec1.y() * vec2.x() < vec1.x() * vec2.y():
                angle *= -1

            angle = (self.rotation() + angle) % 360
            self.setRotation(angle)

    def mouseReleaseEvent(self, event):
        self.axisGrabbed = False
        self.setCursor(Qt.PointingHandCursor)

        if self.__dragActive:
            relRotation = (self.rotation() - self.__origRotation) % 360
            clockwise = (relRotation <= 180)
            angleModifier = 360 - self.__origRotation
            relOwnAngle = (self.rotation() + angleModifier) % 360
            angleDiff = 360 / len(self.view.axes)
            numSteps = 0
            for a in self.view.axes:
                if a == self:
                    continue

                r = a.rotation()
                relAngle = (r + angleModifier) % 360
                if clockwise and relAngle - relOwnAngle < 0:
                    a.axisAnimation.setStartValue(0)
                    a.axisAnimation.setEndValue(-angleDiff)
                    a.initRelativeRotation()
                    a.axisAnimation.start()
                    numSteps += 1
                elif not clockwise and relAngle - relOwnAngle > 0:
                    a.axisAnimation.setStartValue(0)
                    a.axisAnimation.setEndValue(angleDiff)
                    a.initRelativeRotation()
                    a.axisAnimation.start()
                    numSteps -= 1

            newRot = (self.__origRotation + (numSteps * angleDiff)) % 360
            relRotation = newRot - self.rotation()
            # make sure we don't rotate a full circle when crossing 0°
            if relRotation < -180:
                relRotation %= 360

            self.axisAnimation.setStartValue(0)
            self.axisAnimation.setEndValue(relRotation)
            self.initRelativeRotation()
            self.axisAnimation.start()
            self.__origRotation = newRot

            # redraw all lines between points of neighboring axes
            self.view.reparentLines()
        self.__dragActive = False

    def updateCanvasGeometry(self):
        self.view.setUpdatesEnabled(False)
        self.__canvasW = self.view.rect().size().width() - self.paddingHoriz
        self.__canvasH = self.view.rect().size().height() - self.paddingVert
        self.__canvasMaxDim = min(self.__canvasW, self.__canvasH)
        lw = max(self.axesWidth, self.axesWidthHighl) / 2 + 4
        self.__boundingRect = QRectF(QPoint(0 - lw, 0 - lw), QPoint(self.__canvasMaxDim / 2 + lw, lw))
        self.itemChange(self.ItemAxisLenHasChanged, None)
        self.view.setUpdatesEnabled(True)

    def itemChange(self, change, variant):
        if change == self.ItemAxisLenHasChanged or \
                (change == QGraphicsItem.ItemRotationHasChanged and self.view.relation.numDatasets < 200):
            self.view.axisChanged.emit()
        return super().itemChange(change, variant)

    def paint(self, qp: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget=None):
        qp.setPen(self.axesPen)
        self.p2 = QPoint(min(self.__canvasW, self.__canvasH) / 2, 0)
        qp.drawLine(self.p1, self.p2)

    def boundingRect(self):
        if self.__boundingRect is None:
            self.updateCanvasGeometry()
        return self.__boundingRect


class PlotAxisLabel(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def paint(self, qp: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget=None):
        p = self.parentItem()
        pRot = p.rotation()
        trans = QTransform()
        trans.rotate(-p.rotation())

        p2Scene = p.mapToScene(p.p2)
        if 0 <= pRot < 90:
            trans.translate(p2Scene.x() - self.boundingRect().width(), p2Scene.y())
        elif 90 <= pRot < 180:
            trans.translate(p2Scene.x(), p2Scene.y())
        elif 180 <= pRot < 270:
            trans.translate(p2Scene.x(), p2Scene.y() - self.boundingRect().height())
        elif 270 <= 360:
            trans.translate(p2Scene.x() - self.boundingRect().width(), p2Scene.y() - self.boundingRect().height())
        self.setTransform(trans)

        super().paint(qp, option, widget)


class PlotPoint(QGraphicsItem):
    def __init__(self, view, val, cls):
        super().__init__()
        self.val = val
        self.cls = cls
        self.view = view

        self.__axisLen = 0
        self.__boundingRect = None

        self._pen = None

        self.updateColor()
        view.plotPaletteChanged.connect(self.updateColor)
        view.axisChanged.connect(self.updateAxisLen)

    def updateColor(self):
        self._pen = QPen(self.view.getClassColor(self.cls))

    def updateAxisLen(self):
        self.__axisLen = self.parentItem().boundingRect().width()
        self.__boundingRect = QRectF(QPoint(self.val * self.__axisLen - 2, -2), QPoint(self.val * self.__axisLen + 2, 2))

    def paint(self, qp: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        qp.setPen(self._pen)
        qp.drawRect(self.boundingRect())

    def boundingRect(self):
        if self.__boundingRect is None:
            self.updateAxisLen()
        return self.__boundingRect


class PlotLine(QGraphicsLineItem):
    def __init__(self, view, p1, p2):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.cls = p1.cls
        self.view = view
        self.highlighted = False
        self.lineWidth = 1
        self.lineWidthHighl = 4
        self._pen = None
        self._penHighl = None

        self.updateColor()
        self.updateLine()
        view.plotPaletteChanged.connect(self.updateColor)
        view.axisChanged.connect(self.updateLine)

    def updateColor(self):
        color = self.view.getClassColor(self.cls)
        self._pen = QPen(color)
        self._pen.setWidth(self.lineWidth)
        colorHighl = QColor(color)
        colorHighl.setAlpha(255)
        self._penHighl = QPen(colorHighl)
        self._penHighl.setWidth(self.lineWidthHighl)

    def updateLine(self):
        p1 = self.p1.mapToScene(self.p1.boundingRect().center())
        p2 = self.p2.mapToScene(self.p2.boundingRect().center())
        self.setLine(QLineF(p1, p2))

    def paint(self, qp: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        self.setPen(self._pen if not self.highlighted else self._penHighl)
        super().paint(qp, option, widget)

