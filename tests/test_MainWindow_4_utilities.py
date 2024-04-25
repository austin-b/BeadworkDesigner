import os
import pytest

from BeadworkDesigner.MainWindow import BeadworkOrientation, MainWindow
from BeadworkDesigner.utils import loadProject, readConfigFile

testProjectFilesFolder = "tests/testProjectFiles/"
testSavedProject = testProjectFilesFolder + "test.json"
configFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testProjectFiles/config.json")

@pytest.fixture
def mainWindow(qtbot):
    project_configs, app_configs = readConfigFile(configFilePath)  # import config file

    window = MainWindow(debug=False, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(window)
    return window

# TODO: add tests for failure to load
@pytest.mark.parametrize("filename", ["5x7_Vertical.json", "5x7_Horizontal.json"])
def test_mainWindow_importProject(mainWindow, filename):
    filename = testProjectFilesFolder + filename
    mainWindow.importProject(filename)
    testProject = loadProject(filename)
    assert(mainWindow.origModel._data == testProject["project"])
    assert(mainWindow.project_configs == testProject["configs"])

    if mainWindow.currentOrientation == BeadworkOrientation.VERTICAL:
        assert(mainWindow.getConfig("defaultOrientation") == "Vertical")
        assert(mainWindow.modelWidth == mainWindow.getConfig("width"))
        assert(mainWindow.modelHeight == mainWindow.getConfig("height"))
        assert(mainWindow.beadworkView.beadWidth == mainWindow.getConfig("beadWidth"))
        assert(mainWindow.beadworkView.beadHeight == mainWindow.getConfig("beadHeight"))
    else:
        assert(mainWindow.getConfig("defaultOrientation") == "Horizontal")
        assert(mainWindow.modelWidth == mainWindow.getConfig("height"))
        assert(mainWindow.modelHeight == mainWindow.getConfig("width"))
        assert(mainWindow.beadworkView.beadWidth == mainWindow.getConfig("beadHeight"))
        assert(mainWindow.beadworkView.beadHeight == mainWindow.getConfig("beadWidth"))

    assert(mainWindow.windowTitle() == f'Beadwork Designer - {filename}')

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
        "configs": mainWindow.project_configs,
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

def test_MainWindow_setConfig(mainWindow):
    mainWindow.setConfig("width", 15)
    assert(mainWindow.project_configs["width"] == 15)

    mainWindow.setConfig("beadHeight", 15)
    mainWindow.saveConfig(configFilePath)
    
    _, newConfig = readConfigFile(configFilePath)
    assert(newConfig["beadHeight"] == 15)

def test_MainWindow_getConfig(qtbot):
    app_configs = {
        "debug": True,

        # defaults
        "beadHeight": 22,
        "beadWidth": 12,
    }

    window = MainWindow(debug=False, app_configs=app_configs)
    assert(window.getConfig("height") == 12) # not provided, from default_configs
    assert(window.getConfig("beadHeight") == 22) # from app_configs

    with pytest.raises(KeyError):
        window.getConfig("should_fail") # fails