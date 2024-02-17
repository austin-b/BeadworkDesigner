import sys
from PySide6.QtWidgets import QApplication

from BeadworkDesigner.MainWindow import MainWindow

app = QApplication(sys.argv)
window = MainWindow(debug=("--debug" in sys.argv))  # check if debug flag is set
window.show()

app.exec()