import pytest

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.utils import loadProject, saveProject

@pytest.fixture
def mainWindow(qtbot):
    configs = {
        "debug": False,
        "beadHeight": 22,
        "beadWidth": 1,
        "width": 5,
        "height": 7,
        "defaultOrientation": "Vertical"
    }
    window = MainWindow(debug=False, configs=configs)
    qtbot.addWidget(window)
    return window

def test_mainWindow_loadProject(mainWindow):
    mainWindow.importProject("tests/example.json")
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
        "info": {
            "version": 0.1,
            "title": "Example Project"
        },
        "configs": mainWindow.configs,
        "project": mainWindow.origModel._data
    })
    assert(loadProject("tests/test.json") == loadProject("tests/example.json"))