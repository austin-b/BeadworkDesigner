from PySide6.QtWidgets import (QHeaderView, QLayout, QTableView)
from PySide6.QtCore import (QModelIndex, QPersistentModelIndex, Qt)

class BeadworkView(QTableView):
    def __init__(self):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        self.bead_height = 22
        self.bead_width = 12
        
        self.setShowGrid(False)

    def setModel(self, model):
        super().setModel(model)

        self.verticalHeader().setMinimumSectionSize(0)
        self.horizontalHeader().setMinimumSectionSize(0)

        self.setBeadSize(model.rowCount(None), model.columnCount(None))

    def dataChanged(self, topLeft, bottomRight, roles):
        super().dataChanged(topLeft, bottomRight, roles)

        self.setBeadSize(bottomRight.row(), bottomRight.column())

    def setBeadSize(self, rows, columns):
        for i in range(rows):
            self.setRowHeight(i, self.bead_height)
        for i in range(columns):
            self.setColumnWidth(i, self.bead_width)