import pytest

from BeadworkDesigner.MainWindow import BeadworkOrientation, MainWindow

from bin.config import app_configs, project_configs

# What do I need to test?
# - Are the proxy models working as expected?
# - Is the delegate working as expected?
# - Are the signals and slots working as expected?
# - are the width and height spinboxes working as expected?
# - are the color buttons working as expected?
# - are the file buttons working as expected?
# - are the toolbar actions working as expected?
# - have all icons loaded properly?
# - have all tooltips been set?
# - does the ColorList work as expected?
# - does the stylesheet load correctly?
# - do the selection modes work as expected?
# - does the statusbar work as expected?

@pytest.fixture
def mainWindow(qtbot):
    window = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(window)
    return window

def test_MainWindow_init_allItemsVisible(mainWindow):
    mainWindow.show()
    assert(mainWindow.isVisible())

    # all of these widgets are created in MainWindow.__init__(),
    # so all should be visible when the window is shown
    assert(mainWindow.menu.isVisible())
    assert(mainWindow.beadworkView.isVisible())
    assert(mainWindow.orientationLabel.isVisible())
    assert(mainWindow.orientationComboBox.isVisible())
    assert(mainWindow.currentColorLabel.isVisible())
    assert(mainWindow.currentColor.isVisible())
    assert(mainWindow.colorDialogButton.isVisible())
    assert(not mainWindow.colorDialog.isVisible()) # this should be hidden until the button is clicked
    assert(mainWindow.colorList.isVisible())
    assert(mainWindow.toolbar.isVisible())
    assert(mainWindow.statusBarDimensionsWidget.isVisible())

def test_MainWindow_init_menu(mainWindow):
    assert(mainWindow.menu.actions()[0] == mainWindow.fileMenu.menuAction()) # sub-menus are a special type of action, so we see if the Menu action is what's associated with .fileMenu

def test_MainWindow_init_widthXHeightValues(mainWindow):
    assert(mainWindow.modelWidth == mainWindow.model.columnCount(None))
    assert(mainWindow.modelHeight == mainWindow.model.rowCount(None))
    assert(mainWindow.statusBarWidthLabel.text() == str(mainWindow.modelWidth))
    assert(mainWindow.statusBarHeightLabel.text() == str(mainWindow.modelHeight))

def test_MainWindow_init_orientationValues(mainWindow):
    assert(mainWindow.currentOrientation == BeadworkOrientation.VERTICAL)
    assert(mainWindow.orientationComboBox.currentText() == mainWindow.orientationOptions[mainWindow.currentOrientation])

def test_MainWindow_init_colorDialogWidget(mainWindow):
    assert(mainWindow.currentColor.text() == "")

def test_MainWindow_init_colorList(mainWindow):
    pass # TODO: implement test_MainWindow_init_colorList

def test_MainWindow_init_toolbar(mainWindow):
    assert(mainWindow.toolbar.actions()[0] == mainWindow.toolbarOrientationAction)
    # [1] is a separator
    assert(mainWindow.toolbar.actions()[2] == mainWindow.undoAction)
    assert(mainWindow.toolbar.actions()[3] == mainWindow.redoAction)
    # [4] is a separator
    assert(mainWindow.toolbar.actions()[5] == mainWindow.zoomInAction)
    assert(mainWindow.toolbar.actions()[6] == mainWindow.zoomOutAction)
    # [7] is a separator
    assert(mainWindow.toolbar.actions()[8] == mainWindow.addColumnAction)
    assert(mainWindow.toolbar.actions()[9] == mainWindow.addRowAction)
    assert(mainWindow.toolbar.actions()[10] == mainWindow.removeColumnAction)
    assert(mainWindow.toolbar.actions()[11] == mainWindow.removeRowAction)
    # [12] is a separator
    assert(mainWindow.toolbar.actions()[13] == mainWindow.selectionMode)
    assert(mainWindow.toolbar.actions()[14] == mainWindow.colorMode)
    assert(mainWindow.toolbar.actions()[15] == mainWindow.clearMode)

def test_MainWindow_close(mainWindow):
    mainWindow.close()
    assert(not mainWindow.isVisible())
