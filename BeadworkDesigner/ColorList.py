import logging

from PySide6.QtCore import QAbstractProxyModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QColorDialog, QListView, QMenu

logger = logging.getLogger(__name__)

class BeadworkToColorListProxyModel(QAbstractProxyModel):
    def __init__(self, parent = None):
        super().__init__(parent) 

        self._colors = {}
        self._colors_index = []

        logger.info("BeadworkToColorListProxyModel initialized.")

    def setSourceModel(self, sourceModel):
        super().setSourceModel(sourceModel)  

        self._sourceModel = sourceModel
        
        self.evaluateModelForUniqueColors()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._colors_index[index.row()]
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor(self._colors_index[index.row()])
        else:
            return None

    def rowCount(self, parent):
        return len(self._colors_index)
    
    def columnCount(self, parent):
        return 1
    
    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column)
    
    # not sure why this is needed, but it is
    # I believe this behavior defines it as a list model -
    # a single parent index is returned for all rows
    def parent(self, index):
        return QModelIndex()

    def mapFromSource(self, sourceIndex):
        color = self.sourceModel().data(sourceIndex, Qt.ItemDataRole.DisplayRole)
        logger.debug(f"Mapping from source color: {color}, index: {sourceIndex}")
        proxyIndex = self.createIndex(self._colors_index.index(color), 0) # returns the location in the colors_index list
        logger.debug(f"Mapped to proxy index: {proxyIndex}")
        return proxyIndex

    def mapToSource(self, proxyIndex):
        color = self.data(proxyIndex, Qt.ItemDataRole.DisplayRole)
        logger.debug(f"Mapping to source color: {color}, index: {proxyIndex}")
        r, c = self._colors[color][0] # we only return the first index of the color
        sourceIndex = self.sourceModel().index(r, c) 
        logger.debug(f"Mapped to source index: {sourceIndex}")
        return sourceIndex
    
    def mapToAllSourceIndexes(self, proxyIndex):
        color = self.data(proxyIndex, Qt.ItemDataRole.DisplayRole)
        return self.allIndexesForColor(color, proxyIndex)
    
    def allIndexesForColor(self, color, proxyIndex=None):
        try:
            logger.debug(f"Mapping to source color: {color}, index: {proxyIndex}")
            indexes = self._colors[color]
            logger.debug(f"Mapped to source indexes: {indexes}")
            sourceIndexes = map(lambda index: self.sourceModel().index(index[0], index[1]),
                                indexes)
            return list(sourceIndexes)
        except KeyError:    # just in case the color is not valid
            return None   
        
    def changeAllInstancesOfColor(self, initColor, newColor):
        indexes = self.allIndexesForColor(initColor)
        logger.info(f"Changing all instances of {initColor} to {newColor}.")
        for index in indexes:
            self.sourceModel().setData(index, newColor, Qt.ItemDataRole.EditRole)

    # runs through model and creates a dictionary of unique colors
    def evaluateModelForUniqueColors(self):
        self._colors = {} # reinitialize whenever we call this to prevent carryovers
        for row in range(self.sourceModel().rowCount(None)):
            for column in range(self.sourceModel().columnCount(None)):
                color = self.sourceModel().data(self._sourceModel.index(row, column), Qt.ItemDataRole.DisplayRole)
                if color not in self._colors:
                    self._colors[color] = [(row, column)]
                else:
                    self._colors[color].append((row, column))
        self._colors_index = list(self._colors)
        self._colors_index.sort()

    ### SLOTS
    def updateList(self, topLeft, bottomRight):
        logger.debug(f"Data changed: {topLeft}, {bottomRight}.")
        self.evaluateModelForUniqueColors()
        self.dataChanged.emit(self.mapFromSource(topLeft), self.mapFromSource(bottomRight))

# TODO: will need to create a new menu similar to https://forum.qt.io/topic/92366/how-to-use-right-click-instead-of-left-click-for-the-on_listview_clicked-slot-from-qlistview/2
# then connect the self.customContextMenuRequested signal to the slot that creates and shows it
# the signal sends a QPoint (relative to the widget itself), which can be used to get the index of the item that was clicked
# will have to first set setContextMenuPolicy(Qt::CustomContextMenu)
class ColorList(QListView):
    def __init__(self):
        super().__init__()

        self.triggeredIndex = None # index of the item that was right-clicked

        self.colorDialog = QColorDialog() # used to select the new color
        self.colorDialog.colorSelected.connect(lambda c: self.triggerChangeAll(c.name().upper()))

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.customContextMenu)

        self.selectAllAction = QAction("Select All", self) # TODO: implement

        self.changeAllAction = QAction("Change All Occurrences", self)
        self.changeAllAction.triggered.connect(self.openColorDialog)

        logger.info("ColorList initialized.")

    def customContextMenu(self, point):
        self.triggeredIndex = self.indexAt(point)
        logger.debug(f"Triggered ColorList custom context menu at {self.triggeredIndex}.")

        if self.triggeredIndex.isValid():
            menu = QMenu(self)
            menu.addAction(self.selectAllAction)
            menu.addAction(self.changeAllAction)
            menu.exec(self.mapToGlobal(point))

    def openColorDialog(self):
        self.colorDialog.show()

    def triggerChangeAll(self, newColor):
        self.model().changeAllInstancesOfColor(self.triggeredIndex.data(Qt.ItemDataRole.DisplayRole), newColor)

    def updateSelected(self, sourceIndex):
        proxyIndex = self.model().mapFromSource(sourceIndex)
        self.setCurrentIndex(proxyIndex)
        self.scrollTo(proxyIndex)