import pytest

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.utils import loadProject, saveProject

from bin.config import configs

@pytest.fixture
def mainWindow(qtbot):
    window = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(window)
    return window

def test_mainWindow_loadProject(mainWindow):
    mainWindow.importProject(loadProject("tests/example.json"))
    assert(mainWindow.origModel._data == [
        ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"],
        ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"],
        ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"],
        ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"],
        ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"],
        ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"],
        ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]
    ])
    assert(mainWindow.configs == loadProject("tests/example.json")["configs"])

def test_mainWindow_saveProject(mainWindow):
    mainWindow.exportProject("tests/test.json")
    assert(loadProject("tests/test.json") == {
        "configs": mainWindow.configs,
        "project": mainWindow.origModel._data
    })
    assert(loadProject("tests/test.json") == loadProject("tests/example.json"))