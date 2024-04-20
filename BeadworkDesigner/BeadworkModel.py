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
    """A model for the beadwork, internally represented as a 2D list of hex colors."""

    def __init__(self, data = None, debug=False, defaultHeight=7, defaultWidth=5):
        """Initializes the BeadworkModel. If debug is True, generates random colors for all beads.

        Args:
            data (list): The data to load into the model. Defaults to None.
            debug (bool): Flag to generate random colors for debugging. Defaults to False.
            defaultHeight (int): The default height (rows) of the model. Defaults to 7.
            defaultWidth (int): The default width (columns) of the model. Defaults to 5.
        """
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
        """Returns the data at the given index for the given role.

        Args:
            index (QIndex): index of the data.
            role (Qt.ItemDataRole.DisplayRole,
                  Qt.ItemDataRole.BackgroundRole,
                  Qt.ItemDataRole.DecorationRole,
                  Qt.ItemDataRole.SizeHintRole): type of data to retrieve.

        Returns:
            Qt.ItemDataRole.DisplayRole -> str: color, in hex, of the bead.
            Qt.ItemDataRole.BackgroundRole -> QColor: color of the bead.
            Qt.ItemDataRole.DecorationRole -> QColor: color of the bead.
            Qt.ItemDataRole.SizeHintRole -> QSize: size hint for the bead.
        """
        #logger.debug(f"Getting data: {self._data[index.row()][index.column()]} for role {role}.")

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
        """Sets the data at the given index to the given value for the given role.

        Args:
            index (QIndex): index of the data.
            value (str): color, in hex, of the bead.
            role (Qt.ItemDataRole.EditRole): type of data to set.
        """
        if role == Qt.ItemDataRole.EditRole:
            logger.debug(f"Setting data to {value} at {index.row()}, {index.column()}.")
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            logger.debug(f"Data changed at {index.row()}, {index.column()}.")
            return True
        return False  
    
    def headerData(self, section, orientation, role):
        """Returns the header data for the given section, orientation, and role.

        Args:
            section (int): the section of the header.
            orientation (Qt.Orientation.Horizontal, 
                         Qt.Orientation.Vertical): the orientation of the header.
            role (Qt.ItemDataRole.DisplayRole): the role of the header data.
        """
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
            
            #logger.debug(f"returning header data {headerData if headerData else ''} for {orientation} {section}")
            return headerData
        
    def rowCount(self, index=None):
        """Returns the number of rows in the model."""
        # length of outer list
        return len(self._data)
    
    def columnCount(self, index=None):
        """Returns the number of columns in the model."""
        # only works if all rows are an equal length
        return len(self._data[0])   
     
    # from https://doc.qt.io/qtforpython-6/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.QAbstractItemModel.insertRows:
    #   inserts count rows into the model before the given row
    #   If row is 0, the rows are prepended to any existing rows in the parent.
    #   If row is rowCount() , the rows are appended to any existing rows in the parent.
    def insertRow(self, row, count=1, parent=None):
        """Inserts a row at the given index.
        
        Args:
            row (int): The index of the row to insert.
            count (int, optional): The number of rows to insert. Defaults to 1.
            parent (QModelIndex, optional): The parent index. Defaults to None.
        """
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
        """Removes a row at the given index.
        
        Args:
            row (int): The index of the row to remove.
            count (int, optional): The number of rows to remove. Defaults to 1.
            parent (QModelIndex, optional): The parent index. Defaults to None.
        """
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

    def insertColumn(self, column, count=1, parent=None):
        """Inserts a column at the given index.

        Args:
            column (int): The index of the column to insert.
            count (int, optional): The number of columns to insert. Defaults to 1.
            parent (QModelIndex, optional): The parent index. Defaults to None.
        """
        if column == 0:
            logger.debug(f"Prepending {count} column(s) at beginning of model.")
            self.beginInsertColumns(QtCore.QModelIndex(), column, column+(count-1))
            for i in range(count):
                for row in range(self.rowCount()):
                    self._data[row].insert(i, color(random=self._debug))
            self.endInsertColumns()
            logger.debug(f"{count} new column(s) at index 0.")
        elif column == self.columnCount():
            logger.debug(f"Appending {count} column(s) at end of model.")
            self.beginInsertColumns(QtCore.QModelIndex(), column, column+(count-1))
            for i in range(count):
                for row in range(self.rowCount()):
                    self._data[row].append(color(random=self._debug))
            self.endInsertColumns()
            logger.debug(f"{count} new column(s) at index {column}.")
        else:
            logger.debug(f"Inserting {count} column(s) before {column}.")
            self.beginInsertColumns(QtCore.QModelIndex(), column, column+(count-1))
            for i in range(count):
                for row in range(self.rowCount()):
                    self._data[row].insert(column+i, color(random=self._debug))
            self.endInsertColumns()
            logger.debug(f"{count} new column(s) at index {column}.")
    
    def removeColumn(self, column, count=1, parent=None):
        """Removes a column at the given index.

        Args:
            column (int): The index of the column to remove.
            count (int, optional): The number of columns to remove. Defaults to 1.
            parent (QModelIndex, optional): The parent index. Defaults to None.
        """
        columnsRemoved = {}
        logger.debug(f"Removing column at {column}.")
        if column == self.columnCount(): # if column index is at end of model, continue to remove the last column
            self.beginRemoveColumns(QtCore.QModelIndex(), column-count, column-1)
            for i in range(count):
                for row in range(self.rowCount()):
                    try:
                        columnsRemoved[row] += [self._data[row].pop(column-(i+1))]
                    except KeyError:    # if the key doesn't exist, create it
                        columnsRemoved[row] = []
                        columnsRemoved[row] += [self._data[row].pop(column-(i+1))]
        else:       # otherwise, remove the column at the given index
            self.beginRemoveColumns(QtCore.QModelIndex(), column, column+(count-1))
            try:    # try to remove the column, and if it doesn't exist, log the error
                for i in range(count):
                    for row in range(self.rowCount()):
                        try:
                            columnsRemoved[row] += [self._data[row].pop(column)]
                        except KeyError:   # if the key doesn't exist, create it
                            columnsRemoved[row] = []
                            columnsRemoved[row] += [self._data[row].pop(column)]            
            except IndexError: # if the index is out of range, log the error
                logger.error(f"Index out of range: {column}")
        self.endRemoveColumns()
        logger.debug(f"Removed column at {column}.")
        return columnsRemoved
    
    def importData(self, data, debug=False):    # debug flag will fix issues importing data from a debug model to a non-debug existing model
        """Imports data into the BeadworkModel.

        Args:
            data (list): a 2D list of hex colors.
            debug (bool, optional): If set, will generate random colors for beads. Defaults to False.
        """
        self._data = data
        self._debug = debug
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount(None), self.columnCount(None)))
        logger.debug(f"Data imported to BeadworkModel.")

    def exportData(self):
        """Exports data from the BeadworkModel.

        Returns:
            list: a 2D list of hex colors.
        """
        logger.debug(f"Data exported from BeadworkModel.")
        return self._data

class BeadworkTransposeModel(QTransposeProxyModel):
    """A proxy model to transpose the beadwork model - i.e., rows become columns and columns become rows.

    Must call setSourceModel() with a BeadworkModel input to use this model.
    """

    def __init__(self, parent=None):
        """Initializes the BeadworkTransposeModel.
        
        Args:
            parent (QObject, optional): The parent object. Defaults to None.
        """
        super().__init__(parent)

        logger.info(f"BeadworkTransposeModel {self} created.")

    def rowCount(self, parent):
        """Returns the number of rows in the model."""
        return self.sourceModel().columnCount(parent)
    
    def columnCount(self, parent):
        """Returns the number of columns in the model."""
        return self.sourceModel().rowCount(parent)
    
    def insertRow(self, row, count=1):
        """Inserts a row at the given index."""
        logger.debug("Calling insertColumn from BeadworkTransposeModel.")
        self.sourceModel().insertColumn(row, count)

    def insertColumn(self, column, count=1):
        """Inserts a column at the given index."""
        logger.debug("Calling insertRow from BeadworkTransposeModel.")
        self.sourceModel().insertRow(column, count)

    def removeRow(self, row, count=1):
        """Removes a row at the given index."""
        logger.debug("Calling removeColumn from BeadworkTransposeModel.")
        self.sourceModel().removeColumn(row, count)
    
    def removeColumn(self, column, count=1):
        """Removes a column at the given index."""
        logger.debug("Calling removeRow from BeadworkTransposeModel.")
        self.sourceModel().removeRow(column, count)
