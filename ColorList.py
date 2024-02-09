from PySide6.QtCore import QAbstractProxyModel
from PySide6.QtWidgets import QListView

# TODO: Implement this class to provide an interface between the
# BeadworkModel and the ColorList view in the MainWindow
class ColorListModel(QAbstractProxyModel):
    def __init__(self, parent = None):
        super().__init__(parent)       

# TODO: Implement this class
class ColorList(QListView):
    def __init__(self):
        super().__init__()

    # copied from BeadworkModel (replace self._data)
    #def uniqueColors(self):
    #    return list(set([color for row in self._data for color in row])).sort()