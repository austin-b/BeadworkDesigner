import logging

from PySide6.QtWidgets import QWidget

logger = logging.getLogger(__name__)

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(400, 300)

        logger.info("Settings window initialized.")

    def closeEvent(self, event):
        logger.info("Settings window closed.")