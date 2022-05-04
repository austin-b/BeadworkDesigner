# TODO: have different Bead types
# TODO: change to https://doc.qt.io/qt-6/qgraphicsitem.html#setAcceptedMouseButtons
#       to accept hover events

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget

log = logging.getLogger(__name__)

### TODO: add resizing and color change functions
class Bead(QWidget):
    """Widget for individual beads."""
    def __init__(self, color_handler, color=QColor("blue")):
        super().__init__()

        self.color_handler = color_handler

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)

        # TODO: find more accurate bead size
        self.setFixedHeight(15)
        self.setFixedWidth(10)

        self.mousePressEvent = self.change_color

    def change_color(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Window, self.color_handler.picked_color)
            self.setPalette(palette)
            log.info(f"changed color")
 