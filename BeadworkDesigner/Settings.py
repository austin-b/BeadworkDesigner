import logging
import os

from PySide6.QtWidgets import (QFormLayout,
                               QLineEdit,
                               QTabWidget, 
                               QVBoxLayout,
                               QWidget)

from BeadworkDesigner import utils

logger = logging.getLogger(__name__)

# TODO: unit tests

# TODO: add save/cancel buttons

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
bin_dir = os.path.join(base_dir, "bin")
configFile = os.path.join(bin_dir, "config.json")

class SettingsWindow(QWidget):
    def __init__(self, app_configs, project_configs):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(700, 600)

        self.app_configs = app_configs
        self.project_configs = project_configs

        mainlayout = QVBoxLayout()

        self.tab = QTabWidget()

        self.updateConfigs(app_configs, project_configs)

        mainlayout.addWidget(self.tab)
        self.setLayout(mainlayout)

        logger.info("Settings window initialized.")

    def updateConfigs(self, app_configs, project_configs):
        self.app_configs = app_configs
        self.project_configs = project_configs

        self.tab.clear()

        appConfigTab = QWidget()
        appConfigForm = QFormLayout()

        for key in self.app_configs.keys():
            appConfigForm.addRow(key, QLineEdit(str(self.app_configs[key]))) # wrapped in str() because QLineEdit only accepts strings, not bools

        appConfigTab.setLayout(appConfigForm)

        projectConfigTab = QWidget()
        projectConfigForm = QFormLayout()

        for key in self.project_configs.keys():
            projectConfigForm.addRow(key, QLineEdit(str(self.project_configs[key]))) # wrapped in str() because QLineEdit only accepts strings, not bools

        projectConfigTab.setLayout(projectConfigForm)

        self.tab.addTab(appConfigTab, "App Configs")
        self.tab.addTab(projectConfigTab, "Project Configs")

    # TODO: unit tests
    def saveAppConfig(self):
        """Saves the app configurations to the config file."""
        default_project_configs, _ = utils.readConfigFile(configFile) # not overwriting project configs, just app configs
        utils.saveConfigFile({"app_configs": self.app_configs, "project_configs": default_project_configs}, configFile)

    # TODO: unit tests
    def saveDefaultProjectConfig(self):
        """Saves the default project configurations to the config file."""
        _, default_app_configs = utils.readConfigFile(configFile) # not overwriting project configs, just app configs
        utils.saveConfigFile({"app_configs": default_app_configs, "project_configs": self.project_configs}, configFile)

    def closeEvent(self, event):
        logger.info("Settings window closed.")