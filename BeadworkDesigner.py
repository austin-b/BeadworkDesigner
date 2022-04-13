"""
Beadwork Designer by austin-b

TODO: determine license
TODO: what goes in a package summary?
"""


import logging
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Beadwork Designer")

if __name__ == "__main__":

    logging.basicConfig(stream = sys.stdout, level=logging.DEBUG)

    logging.info("Starting...")

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    logging.info("Running app")

    app.exec()