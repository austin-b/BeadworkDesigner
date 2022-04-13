"""
Beadwork Designer by austin-b

TODO: determine license
TODO: what goes in a package summary?
"""


import logging
import sys
from typing import Container

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, 
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QVBoxLayout,
    QWidget
)

class MainWindow(QMainWindow):
    """Main window of application.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Beadwork Designer")

        # TODO: make this changeable
        stylesheet = "beadworkdesigner.qss"
        try:
            f = open(stylesheet, "r")
            self.setStyleSheet(f.read())
            logging.info("Set style.")
        except Exception as e:
            logging.critical("Failed to open stylesheet")
            exit()

        self.create_menus()

        self.create_toolbar()

        self.create_main_window()

        self.setMinimumSize(QSize(1024, 600))

        logging.info("Finished setup.")

    def create_menus(self):
        """Create all menus for main window.
        """
        menu = self.menuBar()

        ### FILE MENU
        file_menu = menu.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(quit)

        file_menu.addAction(exit_action)

        ### EDIT MENU
        edit_menu = menu.addMenu("Edit")

        ### HELP MENU
        help_menu = menu.addMenu("Help")
        # TODO: add About widget

        logging.info("Created menus.")

    def create_toolbar(self):
        """Create toolbar for main window.
        """
        # TODO: add help tips for toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.addWidget(QLabel("Toolbar"))
        self.addToolBar(toolbar)

        logging.info("Created toolbar.")

    def create_main_window(self):
        """Creates main viewing window and widgets
        """

        ### BEAD AND PALLETE PICKER
        # TODO: actually make this the widget it should be
        bead_and_pallete_picker = QVBoxLayout()
        bead_and_pallete_picker.setObjectName("bead_and_pallete_picker")
        bead_picker = QLabel("Bead Picker")
        bead_picker.setFixedWidth(150)
        bead_and_pallete_picker.addWidget(bead_picker)

        ### EDITTING WINDOW
        # TODO: change background to white
        editting_window = QLabel("Editting Window")
        editting_window.setObjectName("editting_window")

        ### MAIN LAYOUT
        layout = QHBoxLayout()
        layout.addLayout(bead_and_pallete_picker)
        layout.addWidget(editting_window)
        layout.setContentsMargins(0,0,0,0)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        logging.info("Created main window.")

if __name__ == "__main__":

    # TODO: implement CLI argument for logging file
    # TODO: make default a log file
    logging.basicConfig(stream = sys.stdout, level=logging.DEBUG)

    logging.info("Starting...")

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    logging.info("Executing app.")

    app.exec()