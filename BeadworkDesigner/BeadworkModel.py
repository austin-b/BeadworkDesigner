import logging

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QTransposeProxyModel

#####################
#
# TODO: create methods for saving and loading to file
#
#####################

### FOR DEBUGGING ###
def generate_random_color():
    import random
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))
def color(random=False):
    if random:
        color = generate_random_color()
        logger.debug(f"picked random color: {color}")
        return color
    else:
        "#000000"
#####################
        
logger = logging.getLogger(__name__)

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
            logging.debug(f"getting data: {self._data[index.row()][index.column()]} for role {role}")
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.BackgroundRole:
            logging.debug(f"getting data: {self._data[index.row()][index.column()]} for role {role}")
            return QtGui.QColor(self._data[index.row()][index.column()])
        
        if role == Qt.ItemDataRole.DecorationRole:
            logging.debug(f"getting data: {self._data[index.row()][index.column()]} for role {role}")
            return QtGui.QColor(self._data[index.row()][index.column()])
        
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            logging.debug(f"setting data: {value} at {index.row()}, {index.column()}")
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
        self._data.insert(index.row()+1, [color(random=self._debug) for _ in range(self.columnCount(index))])
        self.endInsertRows()
        logging.debug(f"inserted row at {index.row()+1}")
    
    def insertColumn(self, column, index):
        self.beginInsertColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            self._data[row].insert(index.column()+1, color(random=self._debug))
        self.endInsertColumns()
        logging.debug(f"inserted column at {index.column()+1}")
    
    # TODO: implement ability to give index like insertRow
    def removeRow(self, row, index):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
        logging.debug(f"removed row at {row}")
    
    # TODO: implement ability to give index like insertColumn
    def removeColumn(self, column, index):
        self.beginRemoveColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            del self._data[row][column]
        self.endRemoveColumns()
        logging.debug(f"removed column at {column}")

class BeadworkTransposeModel(QTransposeProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def rowCount(self, parent):
        return self.sourceModel().columnCount(parent)
    
    def columnCount(self, parent):
        return self.sourceModel().rowCount(parent)
    
    def insertRow(self, row, index):
        self.sourceModel().insertColumn(row, index)

    def insertColumn(self, column, index):
        self.sourceModel().insertRow(column, index)

    def removeRow(self, row, index):
        self.sourceModel().removeColumn(row, index)
    
    def removeColumn(self, column, index):
        self.sourceModel().removeRow(column, index)
