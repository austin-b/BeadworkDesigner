"""
Beadwork Designer by austin-b

TODO: determine license
TODO: what goes in a package summary?


Fugue Icons:

(C) 2013 Yusuke Kamiyamane. All rights reserved.

These icons are licensed under a Creative Commons
Attribution 3.0 License.
<http://creativecommons.org/licenses/by/3.0/>
"""


import logging
import sys
from typing import Container

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, 
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
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
        toolbar = QToolBar("Main Toolbar")

        ### NEW
        new_project_button = QAction(QIcon("icons/fugue-icons/document--plus.png"), "New Project", self)
        new_project_button.setStatusTip("New Project")
        # TODO: add new method
        toolbar.addAction(new_project_button)

        ### SAVE
        save_project_button = QAction(QIcon("icons/fugue-icons/disk--pencil.png"), "Save Project", self)
        save_project_button.setStatusTip("Save Project")
        # TODO: add save method
        toolbar.addAction(save_project_button)

        ### LOAD
        load_project_button = QAction(QIcon("icons/fugue-icons/disk--arrow.png"), "Load Project", self)
        load_project_button.setStatusTip("Load Project")
        # TODO: add load method
        toolbar.addAction(load_project_button)

        ### PRINT
        print_project_button = QAction(QIcon("icons/fugue-icons/printer-monochrome.png"), "Print Project", self)
        print_project_button.setStatusTip("Print Project")
        # TODO: add print method
        toolbar.addAction(print_project_button)

        toolbar.addSeparator()

        ### UNDO


        ### REDO


        self.addToolBar(toolbar)

        logging.info("Created toolbar.")

    def create_main_window(self):
        """Creates main viewing window and widgets
        """

        ### BEAD AND PALLETE PICKER
        # TODO: actually make this the widget it should be
        # TODO: put in its own class
        bead_and_pallete_picker = QVBoxLayout()
        bead_and_pallete_picker.setObjectName("bead_and_pallete_picker")

        bead_picker = QLabel("Bead Picker")
        bead_picker.setObjectName("bead_picker")
        bead_picker.setFixedSize(150, 150)

        bead_list = QListWidget()
        bead_list.setObjectName("bead_list")
        bead_list.setFixedWidth(150)

        bead_and_pallete_picker.addWidget(bead_picker)
        bead_and_pallete_picker.addWidget(bead_list)

        logging.info("Created bead and pallete picker layout.")

        ### EDITTING WINDOW
        editting_window = QLabel("Editting Window")
        editting_window.setObjectName("editting_window")

        logging.info("Created editting window.")

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