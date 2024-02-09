from PySide6.QtWidgets import (QItemDelegate, QStyle)
from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QColor)

class BeadDelegate(QItemDelegate):
    
    def __init__(self):
        super().__init__()
     
    def paint(self, painter, option, index): 
        # draw outside black rectangle if selected
        if bool(option.state & QStyle.StateFlag.State_Selected):
            painter.setPen(QColor("#000000"))
            painter.drawRect(option.rect)

        # translate
        option.rect.translate(1, 1)

        # resize
        option.rect.setSize(QSize(10, 20))
        
        # draw a rectangle
        background_color = index.data(role = Qt.ItemDataRole.BackgroundRole)
        painter.fillRect(option.rect, background_color)
