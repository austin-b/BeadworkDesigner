import pytest

from BeadworkDesigner.MainWindow import MainWindow

from bin.config import configs

@pytest.fixture
def mainWindow(qtbot):
    window = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(window)
    return window

