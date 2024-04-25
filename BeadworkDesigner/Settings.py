import logging

from PySide6.QtWidgets import (QFormLayout,
                               QLineEdit,
                               QTabWidget, 
                               QVBoxLayout,
                               QWidget)

logger = logging.getLogger(__name__)

# TODO: currently only passing in configs at time of setup, will need to
# refactor for passing in current configs

# TODO: add save/cancel buttons

class SettingsWindow(QWidget):
    def __init__(self, app_configs, project_configs):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(700, 600)

        self.app_configs = app_configs
        self.project_configs = project_configs

        mainlayout = QVBoxLayout()

        tab = QTabWidget()

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

        tab.addTab(appConfigTab, "App Configs")
        tab.addTab(projectConfigTab, "Project Configs")

        mainlayout.addWidget(tab)
        self.setLayout(mainlayout)

        logger.info("Settings window initialized.")

    def closeEvent(self, event):
        logger.info("Settings window closed.")