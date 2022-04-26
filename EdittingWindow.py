###
# TODO: inherit from QGridLayout
# TODO: populates with default bead widgets until read from file (ie, default model)
###

import logging

from PyQt6.QtWidgets import QGridLayout, QLabel

class EdittingWindow(QGridLayout):
    """Layout for editting the actual bead design.
    """

    def __init__(self):
        super(QGridLayout, self).__init__()

        test = QLabel("Editting Window")