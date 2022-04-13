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
    QToolBar,
    QWidget
)

class MainWindow(QMainWindow):
    """Main window of application.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Beadwork Designer")

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

    def create_main_window(self):
        """Creates main viewing window and widgets
        """

        # TODO: determine width to set this widget too
        # TODO: actually make this the widget it should be
        bead_and_pallete_picker = QLabel("Bead and Pallete Picker")

        # TODO: change background to white
        editting_window = QLabel("Editting Window")

        layout = QHBoxLayout()

        layout.addWidget(bead_and_pallete_picker)
        layout.addWidget(editting_window)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

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