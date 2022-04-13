"""
Beadwork Designer by austin-b

TODO: determine license
TODO: what goes in a package summary?
"""


import logging
import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    """Main window of application.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Beadwork Designer")

        self.create_menus()

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
        

if __name__ == "__main__":

    # TODO: implement CLI argument for logging file
    # TODO: make default a log file
    logging.basicConfig(stream = sys.stdout, level=logging.DEBUG)

    logging.info("Starting...")

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    logging.info("Running app")

    app.exec()