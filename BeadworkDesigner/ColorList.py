import logging

from PySide6.QtCore import QAbstractProxyModel, QModelIndex, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QListView

# TODO: This class does not work -- do not know why
# last error given when trying to run:
#   NotImplementedError: pure virtual method 'QAbstractProxyModel.parent' not implemented.
#
#
#   IDEA: Have the ProxyModel give a 1-1 mapping of the source model sorted by color,
#   then have the ColorList only display the unique colors
#
#   OTHER IDEA: Have the ProxyModel return the 1st index in the source model for each color,
#   but for later editting provide a custom method for returning all indexes of a color

logger = logging.getLogger(__name__)

class BeadworkToColorListProxyModel(QAbstractProxyModel):
    def __init__(self, parent = None):
        super().__init__(parent) 

        self._colors = {}
        self._colors_index = []

    # TODO: implement and build the colors dictionary
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

    # TODO: these are both implemented, am I forgetting another method that needs to be implemented?
    def rowCount(self, parent):
        return len(self._colors_index)
    
    def columnCount(self, parent):
        return 1
    
    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column)
    
    # not sure why this is needed, but it is
    # I believe this behavior defines it as a list model -
    # a signel parent index is returned for all rows
    def parent(self, index):
        return QModelIndex()

    def mapFromSource(self, sourceIndex):
        color = self.sourceModel().data(sourceIndex, Qt.ItemDataRole.DisplayRole)
        logger.debug(f"Mapping from source color: {color}, index: {sourceIndex}")
        # if color not in self._colors_index:
        #     self.evaluateModelForUniqueColors()
        proxyIndex = self.createIndex(self._colors_index.index(color), 0) # returns the location in the colors_index list
        logger.debug(f"Mapped to proxy index: {proxyIndex}")
        return proxyIndex

    # TODO: implement and map from proxy of all selected colors to source
    def mapToSource(self, proxyIndex):
        color = self.data(proxyIndex, Qt.ItemDataRole.DisplayRole)
        logger.debug(f"Mapping to source color: {color}, index: {proxyIndex}")
        r, c = self._colors[color][0] # we only return the first index of the color
        sourceIndex = self.sourceModel().index(r, c) 
        logger.debug(f"Mapped to source index: {sourceIndex}")
        return sourceIndex

    # runs through model and creates a dictionary of unique colors
    def evaluateModelForUniqueColors(self):
        for row in range(self.sourceModel().rowCount(None)):
            for column in range(self.sourceModel().columnCount(None)):
                color = self.sourceModel().data(self._sourceModel.index(row, column), Qt.ItemDataRole.DisplayRole)
                if color not in self._colors:
                    self._colors[color] = [(row, column)]
                else:
                    self._colors[color].append((row, column))
        self._colors_index = list(self._colors)
        self._colors_index.sort()
        # self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(len(self._colors_index)-1, 0))

    ### SLOTS
    def updateList(self, topLeft, bottomRight):
        logger.debug(f"Data changed: {topLeft}, {bottomRight}.")
        self.evaluateModelForUniqueColors()
        self.dataChanged.emit(self.mapFromSource(topLeft), self.mapFromSource(bottomRight))

# TODO: Implement this class
class ColorList(QListView):
    def __init__(self):
        super().__init__()
