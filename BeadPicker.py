import logging

from PyQt6.QtGui import QAction, QFont, QColor, QIcon
from PyQt6.QtWidgets import QComboBox, QFormLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QColorDialog

log = logging.getLogger(__name__)

class BeadPicker(QFormLayout):
    """The Layout to select bead types, rows, and columns
    """

    # TODO: create mapper widget

    def __init__(self):
        super(QFormLayout, self).__init__()

        bead_type = QComboBox()

        rows = QSpinBox()

        columns = QSpinBox()

        color = QSpinBox()
        color.setPrefix("#")
        color.setDisplayIntegerBase(16)
        color.setRange(0,0xFFFFFF)
        font = color.font()
        font.setCapitalization(QFont.Capitalization.AllUppercase)
        color.setFont(font)
        color.setValue(0xFF)

        color_dialog = QPushButton()
        color_dialog.setIcon(QIcon("icons/fugue-icons/color.png"))
        color_dialog.setStatusTip("Color Picker")
        # TODO: add connect to color dialog picker

        color_picker = QHBoxLayout()
        color_picker.addWidget(color)
        color_picker.addWidget(color_dialog)

        self.addRow(QLabel("Bead Type:"), bead_type)
        self.addRow(QLabel("Rows:"), rows)
        self.addRow(QLabel("Columns:"), columns)
        self.addRow(QLabel("Color:"), color_picker)

        # left, top, right, bottom
        self.setContentsMargins(6, 6, 0, 0)

        log.info("Created BeadPicker layout.")