import json
import logging

logger = logging.getLogger(__name__)

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