from PySide6.QtWidgets import (QItemDelegate, QStyle)
from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QColor)

class BeadDelegate(QItemDelegate):
    
    def __init__(self):
        super().__init__()

        self.beadWidth = 10
        self.beadHeight = 20
     
    def paint(self, painter, option, index): 
        # print(f"painting: {index.data()}")

        # draw outside black rectangle if selected
        if bool(option.state & QStyle.StateFlag.State_Selected):
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
        self.beadWidth = width
        self.beadHeight = height