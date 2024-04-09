import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QUndoCommand

logger = logging.getLogger(__name__)

class CommandChangeColor(QUndoCommand):
    def __init__(self, model, index, color, description=None):
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