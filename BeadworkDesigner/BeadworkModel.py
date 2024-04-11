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
            
            logger.debug(f"returning header data {headerData if headerData else ''} for {orientation} {section}")
            return headerData
        
    def rowCount(self, index):
        """Returns the number of rows in the model."""
        # length of outer list
        return len(self._data)
    
    def columnCount(self, index):
        """Returns the number of columns in the model."""
        # only works if all rows are an equal length
        return len(self._data[0])   
     
    def insertRow(self, row, index):
        """Inserts a row at the given index.

        Args:
            row (int): the row to insert. 
            index (QIndex): the index to insert the row at.
        """
        logger.debug(f"Inserting row at {index.row()}.")
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self._data.insert(index.row()+1, [color(random=self._debug) for _ in range(self.columnCount(index))])
        self.endInsertRows()
        logger.debug(f"New row at {index.row()+1}.")

    def insertRows(self, row, count, index):
        """Inserts count rows at the given index.

        Args:
            row (int): the row to insert. 
            count (int): the number of rows to insert.
            index (QIndex): the index to insert the rows at.
        """
        logger.debug(f"Inserting row at {index.row()}.")
        self.beginInsertRows(QtCore.QModelIndex(), row, row+count)
        for x in range(count):
            self._data.insert(index.row()+x, [color(random=self._debug) for _ in range(self.columnCount(index))])
        self.endInsertRows()
        logger.debug(f"New row at {index.row()+1}.")
    
    def insertColumn(self, column, index):
        """Inserts a column at the given index.

        Args:
            column (int): the column to insert. 
            index (QIndex): the index to insert the column at.
        """
        logger.debug(f"Inserting column at {index.column()}.")
        self.beginInsertColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            self._data[row].insert(index.column()+1, color(random=self._debug))
        self.endInsertColumns()
        logger.debug(f"New column at {index.column()+1}.")

    def insertColumns(self, column, count, index):
        """Inserts count columns at the given index.

        Args:
            column (int): the column to insert. 
            count (int): the number of columns to insert.
            index (QIndex): the index to insert the columns at.
        """
        logger.debug(f"Inserting column at {index.column()}.")
        self.beginInsertColumns(QtCore.QModelIndex(), column, column+count)
        for x in range(count):
            for row in range(self.rowCount(index)):
                self._data[row].insert(index.column()+x, color(random=self._debug))
        self.endInsertColumns()
        logger.debug(f"New column at {index.column()+1}.")
    
    # TODO: implement ability to give index like insertRow
    def removeRow(self, row, index):
        """Removes a row at the given index.

        Args:
            row (int): the row to remove. 
            index (QIndex): the index to remove the row at.
        """
        logger.debug(f"Removing row at {row}.")
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
        logger.debug(f"Removed row at {row}.")

    def removeRows(self, row, count, index):
        """Removes count rows at the given index.

        Args:
            row (int): the row to remove. 
            count (int): the number of rows to remove.
            index (QIndex): the index to remove the rows at.
        """
        logger.debug(f"Removing rows {row-count} to {row}.")
        self.beginRemoveRows(QtCore.QModelIndex(), row-count, row)
        for x in range(count):
            del self._data[row-(x+1)]
            logger.debug(f"Removed row {row-(x+1)}.")
        self.endRemoveRows()
        logger.debug(f"Removed rows {row-count} to {row}.")
    
    # TODO: implement ability to give index like insertColumn
    def removeColumn(self, column, index):
        """Removes a column at the given index.

        Args:
            column (int): the column to remove. 
            index (QIndex): the index to remove the column at.
        """
        logger.debug(f"Removing column at {column}.")
        self.beginRemoveColumns(QtCore.QModelIndex(), column, column)
        for row in range(self.rowCount(index)):
            del self._data[row][column]
        self.endRemoveColumns()
        logger.debug(f"Removed column at {column}.")

    def removeColumns(self, column, count, index):
        """Removes count columns at the given index.

        Args:
            column (int): the column to remove. 
            count (int): the number of columns to remove.
            index (QIndex): the index to remove the columns at.
        """
        logger.debug(f"Removing columns {column-count} to {column}.")
        self.beginRemoveColumns(QtCore.QModelIndex(), column-count, column)
        for x in range(count):
            for row in range(self.rowCount(index)):
                del self._data[row][column-(x+1)]
            logger.debug(f"Removed column {column-(x+1)}.")
        self.endRemoveColumns()
        logger.debug(f"Removed columns {column-count} to {column}.")

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
    
    def insertRow(self, row, index):
        """Inserts a row at the given index."""
        logger.debug("Calling insertColumn from BeadworkTransposeModel.")
        self.sourceModel().insertColumn(row, index)

    def insertRows(self, row, count, index):
        """Inserts count rows at the given index."""
        logger.debug("Calling insertColumns from BeadworkTransposeModel.")
        self.sourceModel().insertColumns(row, count, index)

    def insertColumn(self, column, index):
        """Inserts a column at the given index."""
        logger.debug("Calling insertRow from BeadworkTransposeModel.")
        self.sourceModel().insertRow(column, index)

    def insertColumns(self, column, count, index):
        """Inserts count columns at the given index."""
        logger.debug("Calling insertRows from BeadworkTransposeModel.")
        self.sourceModel().insertRows(column, count, index)

    def removeRow(self, row, index):
        """Removes a row at the given index."""
        logger.debug("Calling removeColumn from BeadworkTransposeModel.")
        self.sourceModel().removeColumn(row, index)

    def removeRows(self, row, count, index):
        """Removes count rows at the given index."""
        logger.debug("Calling removeColumns from BeadworkTransposeModel.")
        self.sourceModel().removeColumns(row, count, index)
    
    def removeColumn(self, column, index):
        """Removes a column at the given index."""
        logger.debug("Calling removeRow from BeadworkTransposeModel.")
        self.sourceModel().removeRow(column, index)

    def removeColumns(self, column, count, index):
        """Removes count columns at the given index."""
        logger.debug("Calling removeRows from BeadworkTransposeModel.")
        self.sourceModel().removeRows(column, count, index)
