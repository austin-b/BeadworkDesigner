###
# TODO: populates with default bead widgets until read from file (ie, default model)
###

import logging

from PyQt6.QtWidgets import QGridLayout, QWidget

from Bead import Bead

log = logging.getLogger(__name__)

# TODO: Export this to its own file to be able to change beadwork types
class Beadwork(QWidget):
    """Widget for the beadwork.
    """
    def __init__(self):
        super(QWidget, self).__init__()

        test_grid = QGridLayout()
        test_grid.setSpacing(1)     # TODO: is this spacing ok? how should it change for the size of the beads

        for i in range(0,200):
            for j in [0,4,8,12]:    # test values to make the grid wider
                test_grid.addWidget(Bead("red"), i, j)
                test_grid.addWidget(Bead("blue"), i, j+1)
                test_grid.addWidget(Bead("green"), i, j+2)
                test_grid.addWidget(Bead("purple"), i, j+3)

        self.setLayout(test_grid)

        log.info("Created Beadwork.")