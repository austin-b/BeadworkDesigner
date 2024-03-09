import pytest

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.utils import loadProject

testProjectFilesFolder = "tests/testProjectFiles/"
testSavedProject = testProjectFilesFolder + "test.json"

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

# TODO: add tests for ensuring all other GUI elements are properly
# TODO: add tests for failure to load
@pytest.mark.parametrize("filename", ["5x7_Vertical.json", "5x7_Horizontal.json"])
def test_mainWindow_importProject(mainWindow, filename):
    filename = testProjectFilesFolder + filename
    mainWindow.importProject(filename)
    testProject = loadProject(filename)
    assert(mainWindow.origModel._data == testProject["project"])
    assert(mainWindow.configs == testProject["configs"])

# this test depends on loadProject to work properly to ensure identity of saved and loaded projects
    # -- probably not correct, but it's a start
@pytest.mark.parametrize("filename", ["5x7_Vertical.json", "5x7_Horizontal.json"])
def test_mainWindow_exportProject(mainWindow, filename):
    filename = testProjectFilesFolder + filename
    mainWindow.importProject(filename)
    mainWindow.exportProject(testSavedProject)
    assert(loadProject(testSavedProject) == {
        "info": {
            "version": 0.1
        },
        "configs": mainWindow.configs,
        "project": mainWindow.origModel._data
    })
    assert(loadProject(testSavedProject) == loadProject(filename))

def test_MainWindow_addColumn(mainWindow):
    width = mainWindow.modelWidth
    mainWindow.addColumn()
    newWidth = mainWindow.modelWidth
    assert(newWidth == width + 1)
    assert(mainWindow.widthSpinBox.value() == newWidth)
    assert(mainWindow.statusBarWidthLabel.text() == str(newWidth))

def test_MainWindow_addRow(mainWindow):
    height = mainWindow.modelHeight
    mainWindow.addRow()
    newHeight = mainWindow.modelHeight
    assert(newHeight == height + 1)
    assert(mainWindow.heightSpinBox.value() == newHeight)
    assert(mainWindow.statusBarHeightLabel.text() == str(newHeight))

def test_MainWindow_removeColumn(mainWindow):
    width = mainWindow.modelWidth
    mainWindow.removeColumn()
    newWidth = mainWindow.modelWidth
    assert(newWidth == width - 1)
    assert(mainWindow.widthSpinBox.value() == newWidth)
    assert(mainWindow.statusBarWidthLabel.text() == str(newWidth))

def test_MainWindow_removeRow(mainWindow):
    height = mainWindow.modelHeight
    mainWindow.removeRow()
    newHeight = mainWindow.modelHeight
    assert(newHeight == height - 1)
    assert(mainWindow.heightSpinBox.value() == newHeight)
    assert(mainWindow.statusBarHeightLabel.text() == str(newHeight))