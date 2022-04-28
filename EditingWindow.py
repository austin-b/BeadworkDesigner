###
# TODO: populates with default bead widgets until read from file (ie, default model)
# TODO: add logging functionality
###

import logging

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QGridLayout, QWidget, QScrollArea

log = logging.getLogger(__name__)

### TODO: add resizing and color change functions
class Bead(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        self.setFixedHeight(15)
        self.setFixedWidth(10)

# TODO: Export this to its own file
class Beadwork(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        test_grid = QGridLayout()
        test_grid.setSpacing(1)

        for i in range(0,200):
            for j in [0,4,8,12]:    # test values to make the grid wider
                test_grid.addWidget(Bead("red"), i, j)
                test_grid.addWidget(Bead("blue"), i, j+1)
                test_grid.addWidget(Bead("green"), i, j+2)
                test_grid.addWidget(Bead("purple"), i, j+3)

        self.setLayout(test_grid)
        

class EditingWindow(QScrollArea):
    """Layout for editting the actual bead design.
    """

    def __init__(self):
        super(QWidget, self).__init__()

        beadwork = Beadwork()
        beadwork.setObjectName("beadwork")

        self.setWidget(beadwork)
        #self.setWidgetResizable(True)