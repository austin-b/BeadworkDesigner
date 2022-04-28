
import logging

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

log = logging.getLogger(__name__)

class AboutWindow(QWidget):
    """About Window class.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.icon = QLabel("[insert icon here]")

        self.version = QLabel("version 0.0")

        self.about = QLabel("""
        This app was made by austin-b. To contact him, check out his <a href="https://github.com/austin-b">Github</a>. 
        """)

        layout.addWidget(self.icon)
        layout.addWidget(self.version)
        layout.addWidget(self.about)

        self.setLayout(layout)

        log.info("Created About Window.")