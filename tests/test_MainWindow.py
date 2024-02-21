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

def test_MainWindow_test(qtbot):
    window = MainWindow(debug=True)
    qtbot.addWidget(window)
    window.show()
    assert(window.isVisible())
    window.close()
    assert(not window.isVisible())