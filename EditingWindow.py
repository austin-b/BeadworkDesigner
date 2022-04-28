###
# TODO: populates with default bead widgets until read from file (ie, default model)
# TODO: add logging functionality
###

import logging

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QGridLayout, QWidget, QScrollArea

log = logging.getLogger(__name__)

### TODO: FOR TEST PURPOSES ONLY, DELETE WHEN FINISHED
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        self.setFixedHeight(500)

# TODO: Export this to its own file
class Beadwork(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        test_grid = QGridLayout()

        for i in range(0,3):
            test_grid.addWidget(Color("red"), i, 0)
            test_grid.addWidget(Color("blue"), i, 1)
            test_grid.addWidget(Color("green"), i, 2)
            test_grid.addWidget(Color("purple"), i, 3)

        self.setLayout(test_grid)
        

class EditingWindow(QScrollArea):
    """Layout for editting the actual bead design.
    """

    def __init__(self):
        super(QWidget, self).__init__()

        beadwork = Beadwork()
        beadwork.setObjectName("beadwork")

        self.setWidget(beadwork)
        self.setWidgetResizable(True)