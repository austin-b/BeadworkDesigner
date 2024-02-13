from PySide6.QtCore import QAbstractItemModel, QAbstractProxyModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtWidgets import QListView

class BeadworkToColorListProxyModel(QAbstractProxyModel):
    def __init__(self, parent = None):
        super().__init__(parent) 

        self._colors = {}
        self._colors_index = []

    # TODO: implement and build the colors dictionary
    def setSourceModel(self, sourceModel):
        super().setSourceModel(sourceModel)  
        
        self.evaluateModelForUniqueColors()

    # TODO: implement and map from source to proxy
    # - create a sorted dictionary in setSourceModel
    # - for each sourceIndex, check if it's in the colors dictionary
    # - if it is, return the index of the color in the list
    # - if it isn't, add it to the list and return the index of the color in the list
    def mapFromSource(self, sourceIndex):
        super().mapFromSource(sourceIndex)

        color = self.sourceModel().data(sourceIndex, Qt.ItemDataRole.DisplayRole)


        if color in self._colors:
            return self.createIndex(self._colors_index.index(color), 0)
        else:
            self.evaluateModelForUniqueColors()
            return self.createIndex(self._colors_index.index(color), 0)

    # TODO: implement and map from proxy of all selected colors to source
    def mapToSource(self, proxyIndex: QModelIndex | QPersistentModelIndex) -> QModelIndex:
        return super().mapToSource(proxyIndex) 

    # runs through model and recreates a dictionary of unique colors
    def evaluateModelForUniqueColors(self):
        for row in range(self.sourceModel().rowCount(None)):
            for column in range(self.sourceModel().columnCount(None)):
                color = self.sourceModel().data(self.sourceModel().index(row, column), Qt.ItemDataRole.DisplayRole)
                if color not in self._colors:
                    self._colors[color] = (row, column)
        self._colors_index = list(self._colors.keys()).sort()
        print("self._colors_index", self._colors_index)     # TODO: prints None, why?
        # self.dataChanged.emit(self.index(0, 0), self.index(len(self.colors), 0)) why?

# TODO: Implement this class
class ColorList(QListView):
    def __init__(self):
        super().__init__()

    # copied from BeadworkModel (replace self._data)
    #def uniqueColors(self):
    #    return list(set([color for row in self._data for color in row])).sort()