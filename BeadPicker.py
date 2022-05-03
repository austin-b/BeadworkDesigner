import logging

from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtWidgets import QColorDialog, QComboBox, QFormLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QColorDialog

log = logging.getLogger(__name__)

class BeadPicker(QFormLayout):
    """The Layout to select bead types, rows, and columns
    """

    # TODO: create mapper widget ------- wat?

    color = QColor(255, 255, 255)

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
        self.text_color.setValue(self.qcolor_to_hex(self.color))
        self.text_color.textChanged.connect(self.update_color)

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

    def qcolor_to_hex(self, color):
        red = hex( color.red() )
        green = hex( color.green() )
        blue = hex( color.blue() )

        # TODO: see if there is a more effecient way to do this
        hex_color = int( str(red)[2:] + str(green)[2:] + str(blue)[2:], 16)
        return hex_color

    def open_color_picker(self):
        log.info("Opening color picker")
        self.color_picker = QColorDialog()
        new_color = self.color_picker.getColor(self.color)

        if new_color.isValid():     # if they press Cancel, just return and do not change
            self.update_color(new_color)

    def update_color(self, new_color):
        if type(new_color) is QColor:
            new_color = self.qcolor_to_hex(new_color)
            self.text_color.setValue(new_color)
            new_color = str(new_color)      # needs to be a string to process the rest
        else:
            if len(new_color) > 7:      # shouldn't ever happen, might as well try to catch it
                log.warn("Invalid color.")
                self.text_color.setStyleSheet("background-color: red;")
                return
         
        new_color = str(new_color[1:])   # removes prefix (#)

        padding = 6 - len(new_color)     # tried zfill and it did not work, this way works for padding at least
        new_color = '0'*padding + new_color
        
        self.text_color.setStyleSheet("background-color: white;")   # in case it was red before

        try:
            # split the colors into rgb components
            red, green, blue  = new_color[:2], new_color[2:4], new_color[4:]
            red = int(red, 16)
            green = int(green, 16)
            blue = int(blue, 16)

            # update the color value
            self.color.setRgb(red, green, blue)

            # emit the color_changed signal
            self.color_handler.change_picked_color(self.color)
            log.info(f"Updated color: red {self.color.red()}, green {self.color.green()}, blue {self.color.blue()}")
        except:
            log.error(f"Invalid color operation.")