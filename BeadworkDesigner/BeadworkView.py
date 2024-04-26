import logging

from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QMenu, QTableView
from PySide6.QtCore import (QItemSelection,
                            QItemSelectionModel,
                            QItemSelectionRange,
                            Qt)

from BeadworkDesigner.Commands import CommandInsertRow, CommandInsertColumn, CommandRemoveRow, CommandRemoveColumn

logger = logging.getLogger(__name__)

class BeadworkHeaderView(QHeaderView):
    """A header view for the BeadworkModel that displays the row and column headers as numbers."""

    def __init__(self, orientation):
        """Initializes the BeadworkHeaderView.

        Args:
            orientation (Qt.Orientation): The orientation of the header view.
        """
        super().__init__(orientation)

        self.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.setMinimumSectionSize(0)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        logger.info("BeadworkHeaderView initialized.")

    # TODO: unit tests
    def showContextMenu(self, position):
        """Shows the context menu at the given position.

        Args:
            position (QPoint): The position to show the context menu.
        """
        index = self.logicalIndexAt(position)
        logger.debug(f"Context menu requested at {position} for index {index}, orientation {self.orientation()}.")
        menu = QMenu(self)
        if self.orientation() == Qt.Orientation.Horizontal:
            menu.addAction("Insert Column", lambda: self.insert(index))
            menu.addAction("Remove Column", lambda: self.remove(index))
        else:
            menu.addAction("Insert Row", lambda: self.insert(index))
            menu.addAction("Remove Row", lambda: self.remove(index))
        menu.exec(self.viewport().mapToGlobal(position))
    
    def insert(self, index):
        """Inserts a row or column at the current index."""
        # TODO: should I be using the parent() method to get the main window, or should the undoStack be a global variable?
        undostack = self.parent().parent.undoStack    # the parent of the header view is the table view, and the parent of the table view is the main window
        if self.orientation() == Qt.Orientation.Horizontal:
            logger.debug(f"Inserting column at {index}.")
            undostack.push(CommandInsertColumn(self.parent().model(), self.parent(), index))
        else:
            logger.debug(f"Inserting row at {index}.")
            undostack.push(CommandInsertRow(self.parent().model(), self.parent(), index))

    def remove(self, index):
        """Removes a row or column at the current index."""
        undostack = self.parent().parent.undoStack    # the parent of the header view is the table view, and the parent of the table view is the main window
        if self.orientation() == Qt.Orientation.Horizontal:
            logger.debug(f"Removing column at {index}.")
            undostack.push(CommandRemoveColumn(self.parent().model(), self.parent(), index))
        else:
            logger.debug(f"Removing row at {index}.")
            undostack.push(CommandRemoveRow(self.parent().model(), self.parent(), index))

class BeadworkView(QTableView):
    """A view for the BeadworkModel that displays the beadwork as a grid of colored beads.

    Must call setModel() with a BeadworkModel to display the beadwork.
    """

    def __init__(self, beadHeight=22, beadWidth=12, parent=None):
        """Initializes the BeadworkView.

        Args:
            beadHeight (int, optional): Height, in pixels, of the beads. Defaults to 22.
            beadWidth (int, optional): Width, in pixels, of the beads. Defaults to 12.
        """
        super().__init__(parent=parent)

        self.parent = parent

        # TODO: can I remove the grey borders?
        self.setVerticalHeader(BeadworkHeaderView(Qt.Orientation.Vertical))
        self.setHorizontalHeader(BeadworkHeaderView(Qt.Orientation.Horizontal))

        self.beadHeight = beadHeight
        self.beadWidth = beadWidth
        
        self.setShowGrid(False)

        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection) # allows using shift and ctrl when selecting

        logger.info("BeadworkView initialized.")

    def setModel(self, model):
        """Sets the model for the view.

        Args:
            model (BeadworkModel): The model to set for the view. Must be a BeadworkModel.
        """
        logger.debug(f"Setting model to {model}.")

        super().setModel(model)

        logger.debug(f"Model set to {model}.")

    # TODO: any way to optimize?
    # ClearAndSelect flag does as it sounds - clears what was previously selected, and selects the next group
    def selectListOfBeads(self, selection, command=QItemSelectionModel.SelectionFlag.ClearAndSelect):
        """Selects a list of beads in the view.

        Args:
            selection (list): A list of QModelIndexes to select.
            command (QItemSelectionModel.SelectionFlag, optional): The selection flag to use. 
                                                                    Defaults to QItemSelectionModel.SelectionFlag.ClearAndSelect.
        """
        selectionRanges = []
        itemSelection = QItemSelection()    # build the selection
        for index in selection:             # turn each index into a 
            selectionRanges.append(QItemSelectionRange(index))  # selection range (possible room for optimization)
        itemSelection.append(selectionRanges) # append all ranges to the selection we want
        self.selectionModel().select(itemSelection, command)    # select the selection
        logger.debug(f"Selected list {selection} in BeadworkView.")

    def dataChanged(self, topLeft, bottomRight, roles):
        """Slot for when the data in the model changes.

        Args:
            topLeft (QModelIndex): The top left index of the data that changed.
            bottomRight (QModelIndex): The bottom right index of the data that changed.
            roles (list): The roles that changed.
        """
        logger.debug(f"Data changed: {topLeft}, {bottomRight}, {roles}.")
        super().dataChanged(topLeft, bottomRight, roles)
        self.setBeadSize()

    # overwritten to explicitly call setBeadSize
    # this is necessary because the view does not seem to update the row and column sizes when the model initially loads
    def repaint(self):
        """Repaints the view."""
        logger.debug("Repainting.")
        self.setBeadSize()
        super().repaint()

    def setBeadSize(self, height=None, width=None):
        """Sets the size of the beads in the view.
        
        Args:
            height (int, optional): The height, in pixels, of the beads. 
                                    If none, uses stored value. Defaults to None.
            width (int, optional):  The width, in pixels, of the beads. 
                                    If none, uses stored value. Defaults to None.
        """
        if height != None:
            self.beadHeight = height

        if width != None:
            self.beadWidth = width

        for i in range(self.model().rowCount(None)):
            self.setRowHeight(i, self.beadHeight)
        for i in range(self.model().columnCount(None)):
            self.setColumnWidth(i, self.beadWidth)

        # may need to scale the 1 pixel border to fit with size -- a large bead size should have a larger border
        self.itemDelegate().changeBeadDimensions(self.beadWidth-1, self.beadHeight-1)

        logger.debug(f"Bead size set to {self.beadWidth}, {self.beadHeight}.")

    def changeOrientation(self):
        """Changes the orientation of the beads in the view - swaps width and height."""
        self.beadHeight, self.beadWidth = self.beadWidth, self.beadHeight
        self.setBeadSize()
        logger.debug(f"Orientation changed to {self.beadWidth}, {self.beadHeight}.")