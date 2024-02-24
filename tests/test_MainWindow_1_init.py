import pytest

from BeadworkDesigner.MainWindow import MainWindow

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
    window = MainWindow(debug=True)
    qtbot.addWidget(window)
    return window

def test_MainWindow_init_allItemsVisible(mainWindow):
    mainWindow.show()
    assert(mainWindow.isVisible())

    # all of these widgets are created in MainWindow.__init__(),
    # so all should be visible when the window is shown
    assert(mainWindow.menu.isVisible())
    assert(mainWindow.beadworkView.isVisible())
    assert(mainWindow.widthLabel.isVisible())
    assert(mainWindow.widthSpinBox.isVisible())
    assert(mainWindow.heightLabel.isVisible())
    assert(mainWindow.heightSpinBox.isVisible())
    assert(mainWindow.orientationLabel.isVisible())
    assert(mainWindow.orientationComboBox.isVisible())
    assert(mainWindow.currentColorLabel.isVisible())
    assert(mainWindow.currentColor.isVisible())
    assert(mainWindow.colorDialogButton.isVisible())
    assert(not mainWindow.colorDialog.isVisible()) # this should be hidden until the button is clicked
    assert(mainWindow.colorList.isVisible())
    assert(mainWindow.toolbar.isVisible())

def test_MainWindow_init_menu(mainWindow):
    assert(mainWindow.menu.actions()[0] == mainWindow.fileMenu.menuAction()) # sub-menus are a special type of action, so we see if the Menu action is what's associated with .fileMenu

def test_MainWindow_init_widthXHeightValues(mainWindow):
    assert(mainWindow.modelWidth == mainWindow.model.columnCount(None))
    assert(mainWindow.modelHeight == mainWindow.model.rowCount(None))
    assert(mainWindow.widthSpinBox.value() == mainWindow.modelWidth)
    assert(mainWindow.heightSpinBox.value() == mainWindow.modelHeight)

def test_MainWindow_init_orientationValues(mainWindow):
    assert(mainWindow.currentOrientation == "Vertical")
    assert(mainWindow.orientationComboBox.currentText() == mainWindow.currentOrientation)

def test_MainWindow_init_colorDialogWidget(mainWindow):
    assert(mainWindow.currentColor.text() == "")

def test_MainWindow_init_colorList(mainWindow):
    pass # TODO: implement test_MainWindow_init_colorList

def test_MainWindow_init_toolbar(mainWindow):
    assert(mainWindow.toolbar.actions()[0] == mainWindow.addColumnAction)
    assert(mainWindow.toolbar.actions()[1] == mainWindow.addRowAction)
    assert(mainWindow.toolbar.actions()[2] == mainWindow.removeColumnAction)
    assert(mainWindow.toolbar.actions()[3] == mainWindow.removeRowAction)
    # [4] is a separator
    assert(mainWindow.toolbar.actions()[5] == mainWindow.selectionMode)
    assert(mainWindow.toolbar.actions()[6] == mainWindow.colorMode)
    assert(mainWindow.toolbar.actions()[7] == mainWindow.clearMode)

def test_MainWindow_close(mainWindow):
    mainWindow.close()
    assert(not mainWindow.isVisible())
