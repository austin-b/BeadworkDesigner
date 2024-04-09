import argparse
import datetime
import logging
import glob
import os
import sys

from PySide6.QtWidgets import QApplication

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.utils import loadProject

# TODO: add capability to return config to default_config.py
try:
    from bin.config import project_configs, app_configs  # import config file
except ImportError:
    logging.error("Custom config not found, importing default.")
    from bin.default_config import project_configs, app_configs  # import default config file

parser = argparse.ArgumentParser(description="Beadwork Designer: An attempt at a Python-based desktop application for designing loom-based beadwork (https://en.wikipedia.org/wiki/Beadwork), also known as beadweaving (https://en.wikipedia.org/wiki/Bead_weaving).")
parser.add_argument("--debug", help="Enable debug mode", action="store_true")
parser.add_argument("--log", help="Log file", type=str, default=None)
parser.add_argument("--load", help="Load project", type=str, default=None)

args = parser.parse_args()

debug = (args.debug) or app_configs["debug"]  # check if debug flag is set

# primary log directory
logDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

# check how many log files there are and remove oldest if there are more than 5
logFiles = sorted(glob.glob(os.path.join(logDir, '*')), key=os.path.getmtime)
if len(logFiles) >= 5:
    os.remove(logFiles[0])

# get current time for log file name
nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

# config logging
logging.basicConfig(level=(logging.DEBUG if debug else logging.INFO), 
                    format='%(filename)s:\t'
                            '%(levelname)s:\t'
                            '%(funcName)s():\t'
                            '%(lineno)d:\t'
                            '%(message)s',
                    handlers=[logging.StreamHandler(sys.stdout), # output to console
                              logging.FileHandler(os.path.join(logDir, args.log) if args.log else   # output to custom log file if specified
                                                  os.path.join(logDir, f'{nowTime}.txt'))])         # else output to default log file

logging.info("Starting...")

app = QApplication(sys.argv)

if args.load:
    json = loadProject(args.load)
    for key in json['project_configs'].keys():
        project_configs[key] = json['configs'][key]        # replace any config with the loaded one

window = MainWindow(debug=debug, app_configs=app_configs, project_configs=project_configs)  # check if debug flag is set

if args.load: window.origModel.importData(json['project'])

window.show()

logging.info("Executing...")

app.exec()