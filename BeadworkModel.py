from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt

### FOR DEBUGGING ###
def generate_random_color():
    import random
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))
def color(random=False):
    if random:
        generate_random_color()
    else:
        "#FFFFFF"
#####################

class BeadworkModel(QtCore.QAbstractTableModel):
    def __init__(self, data = None, debug=False):
        super().__init__()

        self._debug = debug
        
        if self._debug:
            # generate random hex colors in array
            self._data = [[generate_random_color() for _ in range(5)] for _ in range(7)]
        else:
            self._data = [['#FFFFFF' for _ in range(5)] for _ in range(7)]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.BackgroundRole:
            return QtGui.QColor(self._data[index.row()][index.column()])
        
        if role == Qt.ItemDataRole.DecorationRole:
            return QtGui.QColor(self._data[index.row()][index.column()])
        
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False  
        
    def rowCount(self, index):
        # length of outer list
        return len(self._data)
    
    def columnCount(self, index):
        # only works if all rows are an equal length
        return len(self._data[0])   
     
    def insertRow(self, row, index):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._data.insert(row, [color(random=self.debug) for _ in range(self.columnCount(index))]) # TODO: alter this to account for index -- currently only adds to end
        self.endInsertRows()
    
    def insertColumn(self, column, index):
        self.beginInsertColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            self._data[row].insert(column, color(random=self.debug))    # TODO: alter this to account for index -- currently only adds to end
        self.endInsertColumns()
    
    def removeRow(self, row, index):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
    
    def removeColumn(self, column, index):
        self.beginRemoveColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            del self._data[row][column]
        self.endRemoveColumns()