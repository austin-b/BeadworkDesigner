import logging

from collections.abc import Sequence

from PySide6.QtWidgets import QTableView

logger = logging.getLogger(__name__)

class BeadworkView(QTableView):
    def __init__(self, beadHeight=22, beadWidth=12):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        self.beadHeight = beadHeight
        self.beadWidth = beadWidth
        
        self.setShowGrid(False)

        logger.info("BeadworkView initialized.")

    def setModel(self, model):
        logger.debug(f"Setting model to {model}.")

        super().setModel(model)

        self.verticalHeader().setMinimumSectionSize(0)
        self.horizontalHeader().setMinimumSectionSize(0)

        logger.debug(f"Model set to {model}.")

    def dataChanged(self, topLeft, bottomRight, roles):
        logger.debug(f"Data changed: {topLeft}, {bottomRight}, {roles}.")
        super().dataChanged(topLeft, bottomRight, roles)

        self.setBeadSize()

    # overwritten to explicitly call setBeadSize
    # this is necessary because the view does not seem to update the row and column sizes when the model initially loads
    def repaint(self):
        logger.debug("Repainting.")
        self.setBeadSize()
        super().repaint()

    def setBeadSize(self):
        for i in range(self.model().rowCount(None)):
            self.setRowHeight(i, self.beadHeight)
        for i in range(self.model().columnCount(None)):
            self.setColumnWidth(i, self.beadWidth)

        logger.debug(f"Bead size set to {self.beadWidth}, {self.beadHeight}.")

    def changeOrientation(self):
        self.beadHeight, self.beadWidth = self.beadWidth, self.beadHeight
        self.setBeadSize()
        logger.debug(f"Orientation changed to {self.beadWidth}, {self.beadHeight}.")