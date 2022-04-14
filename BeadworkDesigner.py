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
    QLineEdit,
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

        self.create_actions()

        self.create_menus()

        self.create_toolbar()

        self.create_main_window()

        self.setMinimumSize(QSize(1024, 600))

        logging.info("Finished setup.")

    def create_actions(self):
        """Create all actions to be used by menus and toolbar.
        """

        ### EXIT
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(quit)

        ### NEW
        self.new_project_action = QAction(QIcon("icons/fugue-icons/document--plus.png"), "New Project", self)
        self.new_project_action.setStatusTip("New Project")
        # TODO: add new method

        ### SAVE
        self.save_project_action = QAction(QIcon("icons/fugue-icons/disk--pencil.png"), "Save Project", self)
        self.save_project_action.setStatusTip("Save Project")
        # TODO: add save method

        ### LOAD
        self.load_project_action = QAction(QIcon("icons/fugue-icons/disk--arrow.png"), "Load Project", self)
        self.load_project_action.setStatusTip("Load Project")
        # TODO: add load method
        
        ### PRINT
        self.print_project_action = QAction(QIcon("icons/fugue-icons/printer-monochrome.png"), "Print Project", self)
        self.print_project_action.setStatusTip("Print Project")
        # TODO: add print method
        
        ### UNDO
        self.undo_action = QAction(QIcon("icons/fugue-icons/arrow-curve-180-left.png"), "Undo", self)
        self.undo_action.setStatusTip("Undo")
        # TODO: add undo method

        ### REDO
        self.redo_action = QAction(QIcon("icons/fugue-icons/arrow-curve.png"), "Redo", self)
        self.redo_action.setStatusTip("Redo")
        # TODO: add redo method
        
        ### ADD
        self.add_action = QAction(QIcon("icons/fugue-icons/paint-brush--plus.png"), "Add", self)
        self.add_action.setStatusTip("Add")
        # TODO: add add method
        
        ### DELETE
        self.delete_action = QAction(QIcon("icons/fugue-icons/paint-brush--minus.png"), "Delete", self)
        self.delete_action.setStatusTip("Delete")
        # TODO: add delete method

        ### FILL
        self.fill_action = QAction(QIcon("icons/fugue-icons/paint-can.png"), "Fill", self)
        self.fill_action.setStatusTip("Fill")
        # TODO: add fill method
        
        ### LINE
        self.line_action = QAction(QIcon("icons/fugue-icons/layer-shape-line.png"), "Line", self)
        self.line_action.setStatusTip("Line")
        # TODO: add line method
        
        ### ADD ROW
        self.add_row_action = QAction(QIcon("icons/fugue-icons/table-insert-row.png"), "Add Row", self)
        self.add_row_action.setStatusTip("Add Row")
        # TODO: add add row method
        
        ### ADD COLUMN
        self.add_column_action = QAction(QIcon("icons/fugue-icons/table-insert-column.png"), "Add Column", self)
        self.add_column_action.setStatusTip("Add Column")
        # TODO: add add column method

        ### REMOVE ROW
        self.remove_row_action = QAction(QIcon("icons/fugue-icons/table-delete-row.png"), "Remove Row", self)
        self.remove_row_action.setStatusTip("Remove Row")
        # TODO: add remove row method
        
        ### REMOVE COLUMN
        self.remove_column_action = QAction(QIcon("icons/fugue-icons/table-delete-column.png"), "Remove Column", self)
        self.remove_column_action.setStatusTip("Remove Column")
        # TODO: add remove column method

        logging.info("Created actions.")

    def create_menus(self):
        """Create all menus for main window.
        """
        menu = self.menuBar()

        ### FILE MENU
        file_menu = menu.addMenu("File")
        file_menu.addAction(self.new_project_action)
        file_menu.addAction(self.save_project_action)
        file_menu.addAction(self.load_project_action)
        file_menu.addSeparator()
        file_menu.addAction(self.print_project_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        ### EDIT MENU
        edit_menu = menu.addMenu("Edit")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        # TODO: more actions?

        ### HELP MENU
        help_menu = menu.addMenu("Help")
        # TODO: add About widget

        logging.info("Created menus.")

    def create_toolbar(self):
        """Create toolbar for main window.
        """
        toolbar = QToolBar("Main Toolbar")

        toolbar.addAction(self.new_project_action)

        toolbar.addAction(self.save_project_action)

        toolbar.addAction(self.load_project_action)

        toolbar.addAction(self.print_project_action)

        toolbar.addSeparator()

        toolbar.addAction(self.undo_action)

        toolbar.addAction(self.redo_action)

        toolbar.addSeparator()

        toolbar.addAction(self.add_action)

        toolbar.addAction(self.delete_action)

        toolbar.addAction(self.fill_action)

        toolbar.addAction(self.line_action)

        toolbar.addSeparator()

        toolbar.addAction(self.add_row_action)

        toolbar.addAction(self.add_column_action)

        toolbar.addAction(self.remove_row_action)

        toolbar.addAction(self.remove_column_action)

        # add toolbar to window
        self.addToolBar(toolbar)

        logging.info("Created toolbar.")

    def create_main_window(self):
        """Creates main viewing window and widgets
        """

        ### BEAD AND PALLETE PICKER
        # TODO: put in its own class
        bead_and_pallete_picker = QVBoxLayout()
        bead_and_pallete_picker.setObjectName("bead_and_pallete_picker")

        # TODO: create mapper widget
        bead_picker = QLabel("Bead Picker")
        bead_picker.setObjectName("bead_picker")
        bead_picker.setFixedSize(150, 150)

        list_search = QLineEdit()
        list_search.setObjectName("list_search")
        list_search.setFixedWidth(150)

        bead_list = QListWidget()
        bead_list.setObjectName("bead_list")
        bead_list.setFixedWidth(150)

        bead_and_pallete_picker.addWidget(bead_picker)
        bead_and_pallete_picker.addWidget(list_search)
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