###
# TODO: populates with default bead widgets until read from file (ie, default model)
###

import logging

from PyQt6.QtWidgets import QGridLayout, QWidget

from Bead import Bead

log = logging.getLogger(__name__)

class Beadwork(QWidget):
    """Widget for the beadwork.
    """

    def __init__(self, color_handler, rows=200, columns=16):
        super(QWidget, self).__init__()

        self.rows = rows
        self.columns = columns

        # TODO: will need to switch this to a QGraphicsView
        self.beadwork = QGridLayout()
        self.beadwork.setSpacing(1)     # TODO: is this spacing ok? how should it change for the size of the beads

        # fill in blank beads if it is default, ie a "new" project
        for i in range(0,self.rows):
            for j in range(0,columns-1):    # test values to make the grid wider
                self.beadwork.addWidget(Bead(color_handler=color_handler), i, j)

        self.setLayout(self.beadwork)

        log.info("Created Beadwork.")