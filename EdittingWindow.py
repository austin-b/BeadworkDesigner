###
# TODO: inherit from QGridLayout
# TODO: populates with default bead widgets until read from file (ie, default model)
###

import logging

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QGridLayout, QWidget

### TODO: FOR TEST PURPOSES ONLY, DELETE WHEN FINISHED
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class EdittingWindow(QGridLayout):
    """Layout for editting the actual bead design.
    """

    def __init__(self):
        super(QGridLayout, self).__init__()

        test = QLabel("Editting Window")