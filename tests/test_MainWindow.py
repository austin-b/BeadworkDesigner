import pytest

from BeadworkDesigner.MainWindow import MainWindow

# What do I need to test?
# - Does the window open?
# - Does the window close?
# - Are the buttons and widgets visible?
# - Are the model and view classes working as expected?
# - Are the proxy models working as expected?
# - Is the delegate working as expected?
# - Are the signals and slots working as expected?
# - are the width and height spinboxes working as expected?
# - are the color buttons working as expected?
# - are the orientation buttons working as expected?
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
