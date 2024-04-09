import json
import logging

logger = logging.getLogger(__name__)

def saveProject(project, filename):
    with open(filename, 'w') as file:
        json.dump(project, file)
    logger.info(f"Project saved to {filename}.")

def loadProject(filename):
    with open(filename, 'r') as file:
        project = json.load(file)
    logger.info(f"Project loaded from {filename}.")
    return project

# TODO: provide a retrieveConfig method, and if no config is available, log it to prevent errors (and use default config instead)