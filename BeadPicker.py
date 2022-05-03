import logging

from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtWidgets import QColorDialog, QComboBox, QFormLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QColorDialog

log = logging.getLogger(__name__)

class BeadPicker(QFormLayout):
    """The Layout to select bead types, rows, and columns
    """

    # TODO: create mapper widget ------- wat?

    def __init__(self, color_handler):
        super(QFormLayout, self).__init__()

        # TODO: need to refactor to handle this
        self.color_handler = color_handler

        bead_type = QComboBox()

        rows = QSpinBox()

        columns = QSpinBox()

        self.text_color = QSpinBox()
        self.text_color.setObjectName("color")
        self.text_color.setPrefix("#")
        self.text_color.setDisplayIntegerBase(16)
        self.text_color.setRange(0,0xFFFFFF)
        font = self.text_color.font()
        font.setCapitalization(QFont.Capitalization.AllUppercase)
        self.text_color.setFont(font)
        self.text_color.setValue(self.color_handler.picked_color_in_hex)
        self.text_color.textChanged.connect(self.update_color)

        # change text when color is updated
        self.color_handler.colorChanged.connect(lambda hex_color : self.text_color.setValue(hex_color))

        self.color_dialog = QPushButton()
        self.color_dialog.setIcon(QIcon("icons/fugue-icons/color.png"))
        self.color_dialog.setStatusTip("Color Picker")
        self.color_dialog.clicked.connect(self.open_color_picker)

        color_picker = QHBoxLayout()
        color_picker.addWidget(self.text_color)
        color_picker.addWidget(self.color_dialog)

        self.addRow(QLabel("Bead Type:"), bead_type)
        self.addRow(QLabel("Rows:"), rows)
        self.addRow(QLabel("Columns:"), columns)
        self.addRow(QLabel("Color:"), color_picker)

        # left, top, right, bottom
        self.setContentsMargins(6, 6, 0, 0)

        log.info("Created BeadPicker layout.")

    def open_color_picker(self):
        log.info("Opening color picker")
        self.color_picker = QColorDialog()
        new_color = self.color_picker.getColor(self.color_handler.picked_color)

        if new_color.isValid():     # if they press Cancel, just return and do not change
            self.update_color(new_color)

    def update_color(self, new_color):
        if type(new_color) is QColor:
            self.color_handler.change_picked_color(new_color)
        else:
            # to remove the '#' prefix from text_color
            self.color_handler.change_picked_color(new_color[1:])
