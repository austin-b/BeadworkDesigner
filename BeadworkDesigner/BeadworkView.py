import logging

from collections.abc import Sequence

from PySide6.QtWidgets import QTableView

logger = logging.getLogger(__name__)

class BeadworkView(QTableView):
    def __init__(self):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        self.bead_height = 22
        self.bead_width = 12
        
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

    def setBeadSize(self):
        for i in range(self.model().rowCount(None)):
            self.setRowHeight(i, self.bead_height)
        for i in range(self.model().columnCount(None)):
            self.setColumnWidth(i, self.bead_width)

        logger.debug(f"Bead size set to {self.bead_width}, {self.bead_height}.")

    def changeOrientation(self):
        self.bead_height, self.bead_width = self.bead_width, self.bead_height
        self.setBeadSize()
        logger.debug(f"Orientation changed to {self.bead_width}, {self.bead_height}.")