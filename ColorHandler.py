import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor

log = logging.getLogger(__name__)

# TODO: add list of colors currently in use
class ColorHandler():

    picked_color = QColor(255, 255, 255)

    colorChanged = pyqtSignal(QColor)

    def __init__(self):
        pass

    def change_picked_color(self, color):
        self.picked_color = color
        log.info(f"new_color: {color}")