import logging

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QColor

log = logging.getLogger(__name__)

# TODO: add list of colors currently in use
class ColorHandler(QObject):

    picked_color = QColor(255, 255, 255)

    colorChanged = pyqtSignal(int)

    def __init__(self):
        super(ColorHandler, self).__init__()

    def change_picked_color(self, color):
        temp_color = QColor()
        if type(color) is QColor:
            temp_color = color
        else:
            padding = 6 - len(color)     # tried zfill and it did not work, this way works for padding at least
            color = '0'*padding + color
            red, green, blue  = color[:2], color[2:4], color[4:]
            red = int(red, 16)
            green = int(green, 16)
            blue = int(blue, 16)

            # update the color value
            temp_color.setRgb(red, green, blue)

        # only change if it is a different color
        if temp_color != self.picked_color:
            self.picked_color = temp_color
            self.colorChanged.emit(self.picked_color_in_hex)
            log.info(f"new picked color: {self.picked_color_string}")

    @property
    def picked_color_in_hex(self):
        return self.qcolor_to_hex(self.picked_color)

    @property
    def picked_color_string(self):
        red = hex( self.picked_color.red() )
        green = hex( self.picked_color.green() )
        blue = hex( self.picked_color.blue() )

        # TODO: see if there is a more effecient way to do this
        return str(red) + str(green)[2:] + str(blue)[2:]

    def qcolor_to_hex(self, color):
        red = hex( color.red() )
        green = hex( color.green() )
        blue = hex( color.blue() )

        # TODO: see if there is a more effecient way to do this
        hex_color = int( str(red)[2:] + str(green)[2:] + str(blue)[2:], 16)
        return hex_color