from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QTableView

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

        self.source = model

        self.verticalHeader().setMinimumSectionSize(0)
        self.horizontalHeader().setMinimumSectionSize(0)

        self.setBeadSize()

    def dataChanged(self, topLeft, bottomRight, roles):
        super().dataChanged(topLeft, bottomRight, roles)

        self.setBeadSize()

    def setBeadSize(self):
        for i in range(self.source.rowCount(QModelIndex())):
            self.setRowHeight(i, self.bead_height)
        for i in range(self.source.columnCount(QModelIndex())):
            self.setColumnWidth(i, self.bead_width)