import logging

from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QUndoCommand

logger = logging.getLogger(__name__)

class CommandChangeColor(QUndoCommand):
    """Command to change the color of a bead in the BeadworkModel. 
    This command is used to implement undo/redo functionality."""

    def __init__(self, model, index, color, description=None):
        """Create a new CommandChangeColor object.

        Args:
            model (BeadworkModel): The model that contains the data to be changed.
            index (QModelIndex): The index of the data to be changed.
            color (str): The new color to be set (no leading '#').
            description (str, optional): The description of the command. Defaults to None.
        """
        super().__init__(description)

        self.model = model
        self.index = index

        self.oldColor = self.model.data(index, Qt.ItemDataRole.DisplayRole)
        self.newColor = f"#{color}"
        
    def redo(self):
        logger.debug(f"Changing color at {self.index} from {self.oldColor} to {self.newColor}")
        self.model.setData(self.index, self.newColor, Qt.ItemDataRole.EditRole)

    def undo(self):
        logger.debug(f"Undoing color change at {self.index} from {self.oldColor} to {self.newColor}")
        self.model.setData(self.index, self.oldColor, Qt.ItemDataRole.EditRole)

class CommandChangeMultipleColors(QUndoCommand):
    """Command to change the color of multiple beads in the BeadworkModel."""

    def __init__(self, model, indexes, color, description=None):
        """Create a new CommandChangeMultipleColors object.

        Args:
            model (BeadworkModel): The model that contains the data to be changed.
            indexes (list): A list of QModelIndex objects representing the data to be changed.
            color (str): The new color to be set (no leading '#').
            description (str, optional): The description of the command. Defaults to None.
        """
        super().__init__(description)

        self.model = model
        self.indexes = indexes
        self.color = f"#{color}"

        self.oldColors = {}
        for index in indexes:
            self.oldColors[index] = self.model.data(index, Qt.ItemDataRole.DisplayRole)
        
    def redo(self):
        for index in self.indexes:
            logger.debug(f"Changing color at {index} from {self.oldColors[index]} to {self.color}")
            self.model.setData(index, self.color, Qt.ItemDataRole.EditRole)

    def undo(self):
        for index in self.indexes:
            logger.debug(f"Undoing color change at {index} from {self.oldColors[index]} to {self.color}")
            self.model.setData(index, self.oldColors[index], Qt.ItemDataRole.EditRole)

class CommandInsertRow(QUndoCommand):
    """Command to insert a row into the BeadworkModel."""

    def __init__(self, model, view, row, rowCount=1, description=None):
        """Create a new CommandInsertRow object.

        Args:
            model (BeadworkModel): The model to insert the row into.
            view (BeadworkView): The view to repaint after the row is inserted.
            row (int): The row to insert the new row before.
            rowCount (int, optional): The number of rows to insert. Defaults to 1.
            description (str, optional): The description of the command. Defaults to None.
        """
        # from https://doc.qt.io/qtforpython-6/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.QAbstractItemModel.insertRows:
        #   inserts count rows into the model before the given row
        #   If row is 0, the rows are prepended to any existing rows in the parent.
        #   If row is rowCount() , the rows are appended to any existing rows in the parent.
        super().__init__(description)

        self.model = model
        self.view = view
        self.row = row
        self.count = rowCount

    def redo(self):
        self.model.insertRow(self.row, self.count)
        self.view.repaint()

    def undo(self):
        self.model.removeRow(self.row, self.count)
        self.view.repaint()

class CommandRemoveRow(QUndoCommand):
    """Command to remove a row from the BeadworkModel."""

    def __init__(self, model, view, row, rowCount=1, description=None):
        """Create a new CommandRemoveRow object.

        Args:
            model (BeadworkModel): The model to remove the row from.
            view (BeadworkView): The view to repaint after the row is removed.
            row (int): The row to remove.
            rowCount (int, optional): The number of rows to remove. Defaults to 1.
            description (str, optional): The description of the command. Defaults to None.
        """
        super().__init__(description)

        self.model = model
        self.view = view
        self.row = row

        self.count = rowCount

        self.rowCountBefore = self.model.rowCount(None)
        self.rowCountAfter = None

        self.rowData = []   # to store rows removed

    def redo(self):
        self.rowData = self.model.removeRow(self.row, self.count)
        self.rowCountAfter = self.model.rowCount(None)
        self.view.repaint()

    def undo(self):
        if self.row == self.rowCountBefore:
            self.model.insertRow(self.rowCountAfter, self.count)

            for i in range(self.count):
                for j in range(self.model.columnCount()):
                    self.model.setData(self.model.index(self.row + (i-1), j), self.rowData[i][j], Qt.ItemDataRole.EditRole)
        else:
            self.model.insertRow(self.row, self.count)

            for i in range(self.count):
                for j in range(self.model.columnCount()):
                    self.model.setData(self.model.index(self.row + i, j), self.rowData[i][j], Qt.ItemDataRole.EditRole)
        self.view.repaint()
      
class CommandInsertColumn(QUndoCommand):
    """Command to insert a column into the BeadworkModel."""

    def __init__(self, model, view, column, columnCount=1, description=None):
        """Create a new CommandInsertColumn object.

        Args:
            model (BeadworkModel): The model to insert the column into.
            view (BeadworkView): The view to repaint after the column is inserted.
            column (int): The column to insert the new column before.
            columnCount (int, optional): The number of columns to insert. Defaults to 1.
            description (str, optional): The description of the command. Defaults to None.
        """
        # from https://doc.qt.io/qtforpython-6/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.QAbstractItemModel.insertRows:
        #   inserts count rows into the model before the given row
        #   If row is 0, the rows are prepended to any existing rows in the parent.
        #   If row is rowCount() , the rows are appended to any existing rows in the parent.
        super().__init__(description)

        self.model = model
        self.view = view
        self.column = column
        self.count = columnCount

    def redo(self):
        self.model.insertColumn(self.column, self.count)
        self.view.repaint()

    def undo(self):
        # TODO: only for testing, refactor when removeColumn is fixed
        self.model.removeColumn(self.column, self.count)
        self.view.repaint()

class CommandRemoveColumn(QUndoCommand):
    """Command to remove a column from the BeadworkModel."""

    def __init__(self, model, view, column, columnCount=1, description=None):
        """Create a new CommandRemoveColumn object.

        Args:
            model (BeadworkModel): The model to remove the column from.
            view (BeadworkView): The view to repaint after the column is removed.
            column (int): The column to remove.
            columnCount (int, optional): The number of columns to remove. Defaults to 1.
            description (str, optional): The description of the command. Defaults to None.
        """
        super().__init__(description)

        self.model = model
        self.view = view
        self.column = column

        self.count = columnCount

        self.columnCountBefore = self.model.columnCount(None)
        self.columnCountAfter = None

        self.columnData = []   # to store rows removed

    def redo(self):
        self.columnData = self.model.removeColumn(self.column, self.count)
        self.columnCountAfter = self.model.columnCount(None)
        self.view.repaint()

    def undo(self):
        if self.column == self.columnCountBefore:
            self.model.insertColumn(self.columnCountAfter, self.count)
        
            for i in range(self.count):
                for r in range(self.model.rowCount()): 
                        logger.debug(f"Setting data at {r}, {self.column + (i-1)} to {self.columnData[r][i]}")
                        self.model.setData(self.model.index(r, self.column + (i-1)), self.columnData[r][i], Qt.ItemDataRole.EditRole)

        else:
            self.model.insertColumn(self.column, self.count)

            for i in range(self.count):
                for r in range(self.model.rowCount()): 
                        logger.debug(f"Setting data at {r}, {self.column + i} to {self.columnData[r][i]}")
                        self.model.setData(self.model.index(r, self.column + i), self.columnData[r][i], Qt.ItemDataRole.EditRole)
        self.view.repaint()