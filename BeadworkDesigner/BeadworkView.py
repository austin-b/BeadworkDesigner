import logging

from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableView
from PySide6.QtCore import Qt

logger = logging.getLogger(__name__)

class BeadworkView(QTableView):
    """A view for the BeadworkModel that displays the beadwork as a grid of colored beads.

    Must call setModel() with a BeadworkModel to display the beadwork.
    """

    def __init__(self, beadHeight=22, beadWidth=12):
        """Initializes the BeadworkView.

        Args:
            beadHeight (int, optional): Height, in pixels, of the beads. Defaults to 22.
            beadWidth (int, optional): Width, in pixels, of the beads. Defaults to 12.
        """
        super().__init__()

        # TODO: can I remove the grey borders?
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setVisible(False)

        self.beadHeight = beadHeight
        self.beadWidth = beadWidth
        
        self.setShowGrid(False)

        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        logger.info("BeadworkView initialized.")

    def setModel(self, model):
        """Sets the model for the view.

        Args:
            model (BeadworkModel): The model to set for the view. Must be a BeadworkModel.
        """
        logger.debug(f"Setting model to {model}.")

        super().setModel(model)

        self.verticalHeader().setMinimumSectionSize(0)
        self.horizontalHeader().setMinimumSectionSize(0)

        logger.debug(f"Model set to {model}.")

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