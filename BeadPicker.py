import logging

from PyQt6.QtWidgets import QComboBox, QFormLayout, QLabel, QSpinBox

log = logging.getLogger(__name__)

class BeadPicker(QFormLayout):
    def __init__(self):
        super(QFormLayout, self).__init__()

        bead_type = QComboBox()

        rows = QSpinBox()

        columns = QSpinBox()

        self.addRow(QLabel("Bead Type"), bead_type)
        self.addRow(QLabel("Rows"), rows)
        self.addRow(QLabel("Columns"), columns)

        # left, top, right, bottom
        self.setContentsMargins(6, 6, 0, 0)