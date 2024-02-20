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
            logging.debug("Generating BeadworkModel with random colors.")
            self._data = [[generate_random_color() for _ in range(5)] for _ in range(7)]
        else:
            logging.debug("Generating BeadworkModel with blank fields.")
            self._data = [['#FFFFFF' for _ in range(5)] for _ in range(7)]

        logging.info("BeadworkModel created.")

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            logging.debug(f"Getting data: {self._data[index.row()][index.column()]} for role {role}.")
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.BackgroundRole:
            logging.debug(f"Getting data: {self._data[index.row()][index.column()]} for role {role}.")
            return QtGui.QColor(self._data[index.row()][index.column()])
        
        if role == Qt.ItemDataRole.DecorationRole:
            logging.debug(f"Getting data: {self._data[index.row()][index.column()]} for role {role}.")
            return QtGui.QColor(self._data[index.row()][index.column()])
        
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            logging.debug(f"Setting data to {value} at {index.row()}, {index.column()}.")
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            logging.debug(f"Data changed at {index.row()}, {index.column()}.")
            return True
        return False  
        
    def rowCount(self, index):
        # length of outer list
        return len(self._data)
    
    def columnCount(self, index):
        # only works if all rows are an equal length
        return len(self._data[0])   
     
    def insertRow(self, row, index):
        logging.debug(f"Inserting row at {index.row()}.")
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._data.insert(index.row()+1, [color(random=self._debug) for _ in range(self.columnCount(index))])
        self.endInsertRows()
        logging.debug(f"New row at {index.row()+1}.")
    
    def insertColumn(self, column, index):
        logging.debug(f"Inserting column at {index.column()}.")
        self.beginInsertColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            self._data[row].insert(index.column()+1, color(random=self._debug))
        self.endInsertColumns()
        logging.debug(f"New column at {index.column()+1}.")
    
    # TODO: implement ability to give index like insertRow
    def removeRow(self, row, index):
        logging.debug(f"Removing row at {index.row()}.")
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
        logging.debug(f"Removed row at {row}.")
    
    # TODO: implement ability to give index like insertColumn
    def removeColumn(self, column, index):
        logging.debug(f"Removing column at {index.column()}.")
        self.beginRemoveColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            del self._data[row][column]
        self.endRemoveColumns()
        logging.debug(f"Removed column at {column}.")

class BeadworkTransposeModel(QTransposeProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        logging.info("BeadworkTransposeModel created.")

    def rowCount(self, parent):
        return self.sourceModel().columnCount(parent)
    
    def columnCount(self, parent):
        return self.sourceModel().rowCount(parent)
    
    def insertRow(self, row, index):
        logging.debug("Calling insertColumn from BeadworkTransposeModel.")
        self.sourceModel().insertColumn(row, index)

    def insertColumn(self, column, index):
        logging.debug("Calling insertRow from BeadworkTransposeModel.")
        self.sourceModel().insertRow(column, index)

    def removeRow(self, row, index):
        logging.debug("Calling removeColumn from BeadworkTransposeModel.")
        self.sourceModel().removeColumn(row, index)
    
    def removeColumn(self, column, index):
        logging.debug("Calling removeRow from BeadworkTransposeModel.")
        self.sourceModel().removeRow(column, index)
