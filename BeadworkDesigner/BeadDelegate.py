import logging

from PySide6.QtWidgets import (QItemDelegate, QStyle)
from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QColor)

logger = logging.getLogger(__name__)

class BeadDelegate(QItemDelegate):
    
    def __init__(self):
        super().__init__()

        self.beadWidth = 10
        self.beadHeight = 20

        logger.info("BeadDelegate initialized.")
     
    def paint(self, painter, option, index): 
        logger.debug(f"painting: {index.data()} at {index.row()}, {index.column()}.")

        # draw outside black rectangle if selected
        if bool(option.state & QStyle.StateFlag.State_Selected):
            logger.debug(f"painting selected: {index.data()} at {index.row()}, {index.column()}.")
            painter.setPen(QColor("#000000"))
            painter.drawRect(option.rect)

        # translate
        option.rect.translate(1, 1)

        # resize
        option.rect.setSize(QSize(self.beadWidth, self.beadHeight))
        
        # draw a rectangle
        background_color = index.data(role = Qt.ItemDataRole.BackgroundRole)
        painter.fillRect(option.rect, background_color)

    def changeBeadDimensions(self, width, height):
        logger.debug(f"Changing bead dimensions to {width}, {height}.")
        self.beadWidth = width
        self.beadHeight = height