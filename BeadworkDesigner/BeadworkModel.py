import logging
from math import ceil

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QTransposeProxyModel

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
        return "#FFFFFF"
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
        else:
            logger.info("Data given to BeadworkModel, loading given project.")
            self._data = data

        logger.info(f"BeadworkModel {self} created.")

    def data(self, index, role):
        logger.debug(f"Getting data: {self._data[index.row()][index.column()]} for role {role}.")

        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.BackgroundRole:
            return QtGui.QColor(self._data[index.row()][index.column()])
        
        if role == Qt.ItemDataRole.DecorationRole:
            return QtGui.QColor(self._data[index.row()][index.column()])
        
        # Size hint is passed but does not seem to affect the view.
        if role == Qt.ItemDataRole.SizeHintRole:
            return QtCore.QSize(22, 12)
        
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            logger.debug(f"Setting data to {value} at {index.row()}, {index.column()}.")
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            logger.debug(f"Data changed at {index.row()}, {index.column()}.")
            return True
        return False  
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            headerData = None
            if orientation == Qt.Orientation.Horizontal: 
                if (self.columnCount(None) % 2 != 0) and (section == ceil(self.columnCount(None) / 2) - 1):
                    headerData = "||"
                elif ((section + 1) % 5 == 0):
                    headerData = "|"

            if orientation == Qt.Orientation.Vertical:
                if (self.rowCount(None) % 2 != 0) and (section == ceil(self.rowCount(None) / 2) - 1):
                    headerData = "||"
                elif ((section + 1) % 5 == 0):
                    headerData = "|"
            
            logger.debug(f"returning header data {headerData if headerData else ''} for {orientation} {section}")
            return headerData
        
    def rowCount(self, index=None):
        # length of outer list
        return len(self._data)
    
    def columnCount(self, index=None):
        # only works if all rows are an equal length
        return len(self._data[0])   
     
    # from https://doc.qt.io/qtforpython-6/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.QAbstractItemModel.insertRows:
    #   inserts count rows into the model before the given row
    #   If row is 0, the rows are prepended to any existing rows in the parent.
    #   If row is rowCount() , the rows are appended to any existing rows in the parent.
    def insertRow(self, row, count=1, parent=None):
        if row == 0:
            logger.debug(f"Prepending {count} row(s) at beginning of model.")
            self.beginInsertRows(QtCore.QModelIndex(), row, row+(count-1))
            for i in range(count):
                self._data.insert(i, [color(random=self._debug) for _ in range(self.columnCount())])
            self.endInsertRows()
            logger.debug(f"{count} new row(s) at index 0.")
        elif row == self.rowCount():
            logger.debug(f"Appending {count} row(s) at end of model.")
            self.beginInsertRows(QtCore.QModelIndex(), row, row+(count-1))
            for i in range(count):
                self._data.insert(row+i, [color(random=self._debug) for _ in range(self.columnCount())])
            self.endInsertRows()
            logger.debug(f"{count} new row(s) at index {row}.")
        else:
            logger.debug(f"Inserting {count} row(s) before {row}.")
            self.beginInsertRows(QtCore.QModelIndex(), row, row+(count-1))
            for i in range(count):
                self._data.insert(row+i, [color(random=self._debug) for _ in range(self.columnCount())])
            self.endInsertRows()
            logger.debug(f"{count} new row(s) at index {row}.")
    
    def removeRow(self, row, count=1, parent=None):
        rowsRemoved = []
        logger.debug(f"Removing row at {row}.")
        if row == self.rowCount(): # if row index is at end of model, continue to remove the last row
            self.beginRemoveRows(QtCore.QModelIndex(), row-count, row-1)
            for i in range(count):
                rowsRemoved.append(self._data.pop(row-(i+1)))
        else:       # otherwise, remove the row at the given index
            self.beginRemoveRows(QtCore.QModelIndex(), row, row+(count-1))
            try:    # try to remove the row, and if it doesn't exist, log the error
                for _ in range(count):
                    rowsRemoved.append(self._data.pop(row))
            except IndexError:
                logger.error(f"Index out of range: {row}")
        self.endRemoveRows()
        logger.debug(f"Removed row at {row}.")
        return rowsRemoved

    # TODO: repeat refactor above
    def insertColumn(self, column, index):
        logger.debug(f"Inserting column at {index.column()}.")
        self.beginInsertColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            self._data[row].insert(index.column()+1, color(random=self._debug))
        self.endInsertColumns()
        logger.debug(f"New column at {index.column()+1}.")
    
    # TODO: implement ability to give index like insertColumn
    def removeColumn(self, column, index):
        logger.debug(f"Removing column at {column}.")
        self.beginRemoveColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            del self._data[row][column]
        self.endRemoveColumns()
        logger.debug(f"Removed column at {column}.")

    def importData(self, data, debug=False):    # debug flag will fix issues importing data from a debug model to a non-debug existing model
        self._data = data
        self._debug = debug
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount(None), self.columnCount(None)))
        logger.debug(f"Data imported to BeadworkModel.")

    def exportData(self):
        logger.debug(f"Data exported from BeadworkModel.")
        return self._data

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

    def insertRows(self, row, count, index):
        logger.debug("Calling insertColumns from BeadworkTransposeModel.")
        self.sourceModel().insertColumns(row, count, index)

    def insertColumn(self, column, count):
        logger.debug("Calling insertRow from BeadworkTransposeModel.")
        self.sourceModel().insertRow(column, count)

    def insertColumns(self, column, count, index):
        logger.debug("Calling insertRows from BeadworkTransposeModel.")
        self.sourceModel().insertRows(column, count, index)

    def removeRow(self, row, index):
        logger.debug("Calling removeColumn from BeadworkTransposeModel.")
        self.sourceModel().removeColumn(row, index)

    def removeRows(self, row, count, index):
        logger.debug("Calling removeColumns from BeadworkTransposeModel.")
        self.sourceModel().removeColumns(row, count, index)
    
    def removeColumn(self, column, index):
        logger.debug("Calling removeRow from BeadworkTransposeModel.")
        self.sourceModel().removeRow(column, index)

    def removeColumns(self, column, count, index):
        logger.debug("Calling removeRows from BeadworkTransposeModel.")
        self.sourceModel().removeRows(column, count, index)
