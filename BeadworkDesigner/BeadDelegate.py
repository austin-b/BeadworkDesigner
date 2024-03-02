import logging

from PySide6.QtWidgets import (QItemDelegate, QStyle)
from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QColor)

logger = logging.getLogger(__name__)

class BeadDelegate(QItemDelegate):
    
    def __init__(self, beadWidth=12, beadHeight=22):
        super().__init__()

        self.beadWidth = beadWidth-2    # subtract 2 to account for the 1 pixel border
        self.beadHeight = beadHeight-2  # subtract 2 to account for the 1 pixel border

        logger.info("BeadDelegate initialized.")
     
    def paint(self, painter, option, index): 
        # draw outside black rectangle if selected
        # TODO: this sometimes leaves an artifact of the black rectangle, investigate
        if bool(option.state & QStyle.StateFlag.State_Selected):
            logger.debug(f"painting selected: {index.data()} at {index.row()}, {index.column()}.")
            painter.setPen(QColor("#000000"))
            painter.drawRect(option.rect)
        else:
            logger.debug(f"painting unselected: {index.data()} at {index.row()}, {index.column()}.")
            painter.setPen(QColor("#FFFFFF"))
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