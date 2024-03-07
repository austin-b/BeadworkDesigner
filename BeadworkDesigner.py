import sys
import logging
import argparse

from PySide6.QtWidgets import QApplication

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.utils import loadProject

from bin.config import configs  # import default config file

# TODO: provide better description for argparser
parser = argparse.ArgumentParser(description="Beadwork Designer")
parser.add_argument("--debug", help="Enable debug mode", action="store_true")
parser.add_argument("--log", help="Log file", type=str, default=None)
parser.add_argument("--load", help="Load project", type=str, default=None)

args = parser.parse_args()

debug = (args.debug) or configs["debug"]  # check if debug flag is set

# TODO: implement CLI argument for logging file
# TODO: make default a log file
logging.basicConfig(stream = sys.stdout, level=(logging.DEBUG if debug else logging.INFO), format='%(filename)s: '    
                                                                        '%(levelname)s: '
                                                                        '%(funcName)s(): '
                                                                        '%(lineno)d:\t'
                                                                        '%(message)s')

logging.info("Starting...")

app = QApplication(sys.argv)

if args.load:
    json = loadProject(args.load)
    for key in json['configs'].keys():
        configs[key] = json['configs'][key]                 # replace any config with the loaded one
    configs['defaultWidth'] = json['configs']['width']      # override default width
    configs['defaultHeight'] = json['configs']['height']    # override default height

window = MainWindow(debug=debug, configs=configs)  # check if debug flag is set

if args.load: window.origModel.importData(json['project'])  # TODO: dirty, replace with a MainWindow method

window.show()

logging.info("Executing...")

app.exec()