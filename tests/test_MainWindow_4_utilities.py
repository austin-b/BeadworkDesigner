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
    assert(mainWindow.widthEdit.text() == str(newWidth))
    assert(mainWindow.statusBarWidthLabel.text() == str(newWidth))

def test_MainWindow_addRow(mainWindow):
    height = mainWindow.modelHeight
    mainWindow.addRow()
    newHeight = mainWindow.modelHeight
    assert(newHeight == height + 1)
    assert(mainWindow.heightEdit.text() == str(newHeight))
    assert(mainWindow.statusBarHeightLabel.text() == str(newHeight))

def test_MainWindow_removeColumn(mainWindow):
    width = mainWindow.modelWidth
    mainWindow.removeColumn()
    newWidth = mainWindow.modelWidth
    assert(newWidth == width - 1)
    assert(mainWindow.widthEdit.text() == str(newWidth))
    assert(mainWindow.statusBarWidthLabel.text() == str(newWidth))

def test_MainWindow_removeRow(mainWindow):
    height = mainWindow.modelHeight
    mainWindow.removeRow()
    newHeight = mainWindow.modelHeight
    assert(newHeight == height - 1)
    assert(mainWindow.heightEdit.text() == str(newHeight))
    assert(mainWindow.statusBarHeightLabel.text() == str(newHeight))

def test_MainWindow_setWidth(mainWindow):
    # test removing and adding multiple columns
    width = mainWindow.modelWidth
    assert(width < 15)
    mainWindow.widthEdit.setText("15")
    mainWindow.changeDimensionsButton.click()

    newWidth = mainWindow.modelWidth
    assert(newWidth == 15)
    assert(mainWindow.widthEdit.text() == str(newWidth))
    assert(mainWindow.statusBarWidthLabel.text() == str(newWidth))

    mainWindow.widthEdit.setText("5")
    mainWindow.changeDimensionsButton.click()

    newWidth = mainWindow.modelWidth
    assert(newWidth == 5)
    assert(mainWindow.widthEdit.text() == str(newWidth))
    assert(mainWindow.statusBarWidthLabel.text() == str(newWidth))

def test_MainWindow_setHeight(mainWindow):
    # test removing and adding multiple rows
    height = mainWindow.modelHeight
    assert(height < 15)
    mainWindow.heightEdit.setText("15")
    mainWindow.changeDimensionsButton.click()

    newHeight = mainWindow.modelHeight
    assert(newHeight == 15)
    assert(mainWindow.heightEdit.text() == str(newHeight))
    assert(mainWindow.statusBarHeightLabel.text() == str(newHeight))

    mainWindow.heightEdit.setText("5")
    mainWindow.changeDimensionsButton.click()

    newHeight = mainWindow.modelHeight
    assert(newHeight == 5)
    assert(mainWindow.heightEdit.text() == str(newHeight))
    assert(mainWindow.statusBarHeightLabel.text() == str(newHeight))
    
def test_MainWindow_selectionModeOnly(mainWindow):
    mainWindow.selectionMode.trigger()
    assert(mainWindow.selectionMode.isChecked() == True)
    assert(mainWindow.colorMode.isChecked() == False)
    assert(mainWindow.clearMode.isChecked() == False)

    # test that it stays on
    mainWindow.selectionMode.trigger()
    assert(mainWindow.selectionMode.isChecked() == True)
    assert(mainWindow.colorMode.isChecked() == False)
    assert(mainWindow.clearMode.isChecked() == False)

def test_MainWindow_colorModeOnly(mainWindow):
    mainWindow.colorMode.trigger()
    assert(mainWindow.selectionMode.isChecked() == False)
    assert(mainWindow.colorMode.isChecked() == True)
    assert(mainWindow.clearMode.isChecked() == False)

    # test that it stays on
    mainWindow.colorMode.trigger()
    assert(mainWindow.selectionMode.isChecked() == False)
    assert(mainWindow.colorMode.isChecked() == True)
    assert(mainWindow.clearMode.isChecked() == False)

    assert(mainWindow.currentColor.text() == "")

def test_MainWindow_clearModeOnly(mainWindow):
    mainWindow.clearMode.trigger()
    assert(mainWindow.selectionMode.isChecked() == False)
    assert(mainWindow.colorMode.isChecked() == False)
    assert(mainWindow.clearMode.isChecked() == True)

    # test that it stays on
    mainWindow.clearMode.trigger()
    assert(mainWindow.selectionMode.isChecked() == False)
    assert(mainWindow.colorMode.isChecked() == False)
    assert(mainWindow.clearMode.isChecked() == True)

    assert(mainWindow.currentColor.text() == "")