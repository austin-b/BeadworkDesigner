import logging

from PySide6.QtCore import QAbstractItemModel, QAbstractProxyModel, QModelIndex, QPersistentModelIndex, Qt
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

    # TODO: these are both implemented, am I forgetting another method that needs to be implemented?
    def rowCount(self, parent):
        return len(self._colors_index)
    
    def columnCount(self, parent):
        return 1
    
    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column)

    def mapFromSource(self, sourceIndex):
        color = self.sourceModel().data(sourceIndex, Qt.ItemDataRole.DisplayRole)
        logger.debug(f"Mapping from source color: {color}, index: {sourceIndex}")
        proxyIndex = self.createIndex(self._colors_index.index(color), 0) # returns the location in the colors_index list
        logger.debug(f"Mapping to proxy index: {proxyIndex}")
        return proxyIndex

        # if color in self._colors:
        # else: TODO: why would a color from the model not already be in here -- provided we hook up the signals properly?
        #     self.evaluateModelForUniqueColors()
        #     return self.createIndex(self._colors_index.index(color), 0)

    # TODO: implement and map from proxy of all selected colors to source
    # TODO: does this have to be implemented before the proxy model can be used?
    def mapToSource(self, proxyIndex):
        # print(f"proxy data: {proxyIndex.data()}")
        # color = proxyIndex.data(Qt.ItemDataRole.DisplayRole)

        # if color in self._colors:
            # return self.createIndex(self._colors[color][0][0], self._colors[color][0][1])
        res = self.sourceModel().match(self.sourceModel().index(0, 0), Qt.DisplayRole, proxyIndex.row(), flags=Qt.MatchExactly)
        if res:
            return res[0].sibling(res[0].row(), proxyIndex.column())
        return QModelIndex()

    # runs through model and recreates a dictionary of unique colors
    def evaluateModelForUniqueColors(self):
        for row in range(self.sourceModel().rowCount(None)):
            for column in range(self.sourceModel().columnCount(None)):
                color = self.sourceModel().data(self._sourceModel.index(row, column), Qt.ItemDataRole.DisplayRole)
                if color not in self._colors:
                    self._colors[color] = [(row, column)]
                else:
                    self._colors[color].append((row, column))
        logging.debug("self._colors", self._colors)
        self._colors_index = list(self._colors)
        self._colors_index.sort()
        print("self._colors_index", self._colors_index)     # NOTE: this has a list of colors
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(len(self._colors_index), 0))

# TODO: Implement this class
class ColorList(QListView):
    def __init__(self):
        super().__init__()

    # copied from BeadworkModel (replace self._data)
    #def uniqueColors(self):
    #    return list(set([color for row in self._data for color in row])).sort()