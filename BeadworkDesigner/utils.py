import json
import logging

logger = logging.getLogger(__name__)

def readConfigFile(filename):
    """Reads a configuration file in JSON format.

    Args:
        filename (str): The filename of the configuration file.

    Returns:
        dict: The configuration file as a dictionary.
    """
    with open(filename, 'r') as file:
        config = json.load(file)
    logger.info(f"Config file {filename} read.")
    return config["project_configs"], config["app_configs"]

# TODO: implement
# project configs will save in the project, so only save the 
# project configs if the user wants them to be default
def saveConfigFile(configs, filename):
    """Saves a configuration file in JSON format.

    Args:
        configs (dict): The configuration file to save.
        filename (str): The filename to save the configuration file to.
    """
    with open(filename, 'w') as file:
        json.dump(configs, file)
    logger.info(f"Config file saved to {filename}.")

def saveProject(project, filename):
    """Saves a project to a file in JSON format.

    Args:
        project (dict): The project to save. Includes project_configs and the model data.
        filename (str): The filename to save the project to.
    """
    with open(filename, 'w') as file:
        json.dump(project, file)
    logger.info(f"Project saved to {filename}.")

def loadProject(filename):
    """Loads a project from a file in JSON format.

    Args:
        filename (str): The filename to load the project from.

    Returns:
        dict: The project loaded from the file. Includes project_configs and the model data.
    """
    with open(filename, 'r') as file:
        project = json.load(file)
    logger.info(f"Project loaded from {filename}.")
    return project