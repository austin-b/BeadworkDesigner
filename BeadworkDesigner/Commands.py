import logging

from PySide6.QtCore import Qt
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

class CommandInsertRow(QUndoCommand):
    def __init__(self, model, row, rowCount=1, description=None):
        # from https://doc.qt.io/qtforpython-6/PySide6/QtCore/QAbstractItemModel.html#PySide6.QtCore.QAbstractItemModel.insertRows:
        #   inserts count rows into the model before the given row
        #   If row is 0, the rows are prepended to any existing rows in the parent.
        #   If row is rowCount() , the rows are appended to any existing rows in the parent.
        super().__init__(description)

        self.model = model
        self.row = row
        self.rowCount = rowCount

        self.rowCountBefore = self.model.rowCount(None)

    def redo(self):
        self.model.insertRow(self.row, self.rowCount)

    def undo(self):
        # just to test the undo functionality -- this is not the correct way to implement undo
        # does not account for which row was inserted, and that needs to be removed
        self.model.removeRow(self.row, None)

class CommandInsertColumn(QUndoCommand):
    pass

class CommandRemoveRow(QUndoCommand):
    # copy the entire row in order to redo properly?
    # add a method to BeadworkModel to retrieve a whole row?
    # and add an option to insertRow to accept data?
    pass

class CommandRemoveColumn(QUndoCommand):
    pass