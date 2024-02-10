from PySide6.QtCore import QAbstractItemModel, QAbstractProxyModel, QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import QListView

class BeadworkToColorListProxyModel(QAbstractProxyModel):
    def __init__(self, parent = None):
        super().__init__(parent) 

        self.colors = {}

    # TODO: implement and build the colors dictionary
    def setSourceModel(self, sourceModel):
        super().setSourceModel(sourceModel)  

    # TODO: implement and map from source to proxy
    def mapFromSource(self, sourceIndex: QModelIndex | QPersistentModelIndex) -> QModelIndex:
        return super().mapFromSource(sourceIndex)

    # TODO: implement and map from proxy of all selected colors to source
    def mapToSource(self, proxyIndex: QModelIndex | QPersistentModelIndex) -> QModelIndex:
        return super().mapToSource(proxyIndex)    

# TODO: Implement this class
class ColorList(QListView):
    def __init__(self):
        super().__init__()

    # copied from BeadworkModel (replace self._data)
    #def uniqueColors(self):
    #    return list(set([color for row in self._data for color in row])).sort()