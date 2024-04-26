import logging
import os

from PySide6.QtWidgets import (QPushButton,
                               QFormLayout,
                               QLineEdit,
                               QTabWidget, 
                               QVBoxLayout,
                               QWidget)

from BeadworkDesigner import utils

logger = logging.getLogger(__name__)

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
bin_dir = os.path.join(base_dir, "bin")
configFile = os.path.join(bin_dir, "config.json")

class SettingsWindow(QWidget):
    """A window for changing the application and project configurations."""

    def __init__(self, app_configs, project_configs):
        """Initializes the settings window.

        Args:
            app_configs (dict): The application configurations.
            project_configs (dict): The project configurations.
        """
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(700, 600)

        self.app_configs = app_configs
        self.project_configs = project_configs

        mainlayout = QVBoxLayout()

        tab = QTabWidget()

        appConfigTab = QWidget()
        appConfigTabLayout = QVBoxLayout()
        self.appConfigForm = QFormLayout()

        for key in self.app_configs.keys():
            self.appConfigForm.addRow(key, QLineEdit(str(self.app_configs[key]))) # wrapped in str() because QLineEdit only accepts strings, not bools

        appConfigTabLayout.addLayout(self.appConfigForm)

        saveAppConfigButton = QPushButton("Save App Configs")
        saveAppConfigButton.clicked.connect(self.saveAppConfig)

        appConfigTabLayout.addWidget(saveAppConfigButton)

        appConfigTab.setLayout(appConfigTabLayout)

        projectConfigTab = QWidget()
        projectConfigTabLayout = QVBoxLayout()
        self.projectConfigForm = QFormLayout()

        for key in self.project_configs.keys():
            self.projectConfigForm.addRow(key, QLineEdit(str(self.project_configs[key]))) # wrapped in str() because QLineEdit only accepts strings, not bools

        projectConfigTabLayout.addLayout(self.projectConfigForm)

        saveDefaultProjectConfigButton = QPushButton("Save Default Project Configs")
        saveDefaultProjectConfigButton.clicked.connect(self.saveDefaultProjectConfig)

        projectConfigTabLayout.addWidget(saveDefaultProjectConfigButton)

        projectConfigTab.setLayout(projectConfigTabLayout)

        tab.addTab(appConfigTab, "App Configs")
        tab.addTab(projectConfigTab, "Project Configs")

        mainlayout.addWidget(tab)
        self.setLayout(mainlayout)

        logger.info("Settings window initialized.")

    def updateConfigs(self, app_configs, project_configs):
        """Updates the configurations in the settings window. All fields are removed and then re-added with the new configurations.
        
        Args:
            app_configs (dict): The new app configurations.
            project_configs (dict): The new project configurations.
        """
        self.app_configs = app_configs
        self.project_configs = project_configs

        # remove old fields
        for i in range(self.appConfigForm.rowCount()):
            self.appConfigForm.removeRow(0)

        for i in range(self.projectConfigForm.rowCount()):
            self.projectConfigForm.removeRow(0)

        # add new fields
        for key in self.app_configs.keys():
            self.appConfigForm.addRow(key, QLineEdit(str(self.app_configs[key])))     

        for key in self.project_configs.keys():
            self.projectConfigForm.addRow(key, QLineEdit(str(self.project_configs[key])))   

    def saveAppConfig(self):
        """Saves the app configurations to the config file."""
        default_project_configs, _ = utils.readConfigFile(configFile) # not overwriting project configs, just app configs
        utils.saveConfigFile({"app_configs": self.app_configs, "project_configs": default_project_configs}, configFile)

    def saveDefaultProjectConfig(self):
        """Saves the default project configurations to the config file."""
        _, default_app_configs = utils.readConfigFile(configFile) # not overwriting project configs, just app configs
        utils.saveConfigFile({"app_configs": default_app_configs, "project_configs": self.project_configs}, configFile)

    def closeEvent(self, event):
        """Logs that the settings window was closed."""
        logger.info("Settings window closed.")