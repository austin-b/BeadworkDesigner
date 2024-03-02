import sys
import logging

from PySide6.QtWidgets import QApplication

from BeadworkDesigner.MainWindow import MainWindow

from bin.config import configs  # import default config file

debug = ("--debug" in sys.argv) or configs["debug"]  # check if debug flag is set

# TODO: implement CLI argument for logging file
# TODO: make default a log file
logging.basicConfig(stream = sys.stdout, level=(logging.DEBUG if debug else logging.INFO), format='%(filename)s: '    
                                                                        '%(levelname)s: '
                                                                        '%(funcName)s(): '
                                                                        '%(lineno)d:\t'
                                                                        '%(message)s')

logging.info("Starting...")

app = QApplication(sys.argv)
window = MainWindow(debug=debug, configs=configs)  # check if debug flag is set
window.show()

logging.info("Executing...")

app.exec()