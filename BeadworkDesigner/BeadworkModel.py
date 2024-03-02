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
    colorString = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    return colorString.upper()
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
    def __init__(self, data = None, debug=False, defaultHeight=7, defaultWidth=5):
        super().__init__()

        self._debug = debug
        
        if not data:
            logger.info("No data given to BeadworkModel, loading initial project.")
            if self._debug:
                # generate random hex colors in array
                logger.debug("Generating BeadworkModel with random colors.")
                self._data = [[generate_random_color() for _ in range(defaultWidth)] for _ in range(defaultHeight)]
            else:
                logger.debug("Generating BeadworkModel with blank fields.")
                self._data = [['#FFFFFF' for _ in range(defaultWidth)] for _ in range(defaultHeight)]

        logger.info(f"BeadworkModel {self} created.")

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            logger.debug(f"Getting data: {self._data[index.row()][index.column()]} for role {role}.")
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.BackgroundRole:
            logger.debug(f"Getting data: {self._data[index.row()][index.column()]} for role {role}.")
            return QtGui.QColor(self._data[index.row()][index.column()])
        
        if role == Qt.ItemDataRole.DecorationRole:
            logger.debug(f"Getting data: {self._data[index.row()][index.column()]} for role {role}.")
            return QtGui.QColor(self._data[index.row()][index.column()])
        
        # Size hint is passed but does not seem to affect the view.
        if role == Qt.ItemDataRole.SizeHintRole:
            logger.debug(f"Passing size hint.")
            return QtCore.QSize(22, 12)
        
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            logger.debug(f"Setting data to {value} at {index.row()}, {index.column()}.")
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            logger.debug(f"Data changed at {index.row()}, {index.column()}.")
            return True
        return False  
        
    def rowCount(self, index):
        # length of outer list
        return len(self._data)
    
    def columnCount(self, index):
        # only works if all rows are an equal length
        return len(self._data[0])   
     
    def insertRow(self, row, index):
        logger.debug(f"Inserting row at {index.row()}.")
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._data.insert(index.row()+1, [color(random=self._debug) for _ in range(self.columnCount(index))])
        self.endInsertRows()
        logger.debug(f"New row at {index.row()+1}.")
    
    def insertColumn(self, column, index):
        logger.debug(f"Inserting column at {index.column()}.")
        self.beginInsertColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            self._data[row].insert(index.column()+1, color(random=self._debug))
        self.endInsertColumns()
        logger.debug(f"New column at {index.column()+1}.")
    
    # TODO: implement ability to give index like insertRow
    def removeRow(self, row, index):
        logger.debug(f"Removing row at {index.row()}.")
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
        logger.debug(f"Removed row at {row}.")
    
    # TODO: implement ability to give index like insertColumn
    def removeColumn(self, column, index):
        logger.debug(f"Removing column at {index.column()}.")
        self.beginRemoveColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            del self._data[row][column]
        self.endRemoveColumns()
        logger.debug(f"Removed column at {column}.")

class BeadworkTransposeModel(QTransposeProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        logger.info(f"BeadworkTransposeModel {self} created.")

    def rowCount(self, parent):
        return self.sourceModel().columnCount(parent)
    
    def columnCount(self, parent):
        return self.sourceModel().rowCount(parent)
    
    def insertRow(self, row, index):
        logger.debug("Calling insertColumn from BeadworkTransposeModel.")
        self.sourceModel().insertColumn(row, index)

    def insertColumn(self, column, index):
        logger.debug("Calling insertRow from BeadworkTransposeModel.")
        self.sourceModel().insertRow(column, index)

    def removeRow(self, row, index):
        logger.debug("Calling removeColumn from BeadworkTransposeModel.")
        self.sourceModel().removeColumn(row, index)
    
    def removeColumn(self, column, index):
        logger.debug("Calling removeRow from BeadworkTransposeModel.")
        self.sourceModel().removeRow(column, index)
