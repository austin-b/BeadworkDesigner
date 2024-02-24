import pytest
from PySide6.QtCore import Qt

from BeadworkDesigner.MainWindow import MainWindow

####################
# TODO: test SelectionMode
####################

@pytest.fixture
def mainWindow(qtbot):
    window = MainWindow(debug=True)
    qtbot.addWidget(window)
    return window

def test_beadworkView_init(mainWindow):
    mainWindow.show()
    view = mainWindow.beadworkView
    assert(view.isVisible())
    assert(view.model() == mainWindow.origModel)
    assert(view.itemDelegate() == mainWindow.delegate)
    assert(not view.verticalHeader().isVisible())
    assert(not view.horizontalHeader().isVisible())
    assert(view.showGrid() == False)
    assert(view.bead_height == 22)  # default value
    assert(view.bead_width == 12)   # default value
    assert(view.rowHeight(0) == view.bead_height)  # default value
    assert(view.columnWidth(0) == view.bead_width) # default value

### TODO: work on finishing this test
# def test_beadworkView_data(mainWindow):
#     view = mainWindow.beadworkView

#     # TODO: can I test if the data is being displayed properly?
#     testRow, testColumn = 0, 0
#     color = mainWindow.model.data(mainWindow.model.index(testRow, testColumn), Qt.ItemDataRole.DisplayRole)

#     # TODO: can I simulate a click to make sure it works properly?
#     view.clicked(view.model().index(testRow, testColumn)).emit()

#     currentColorText = mainWindow.currentColor.text()

#     assert(currentColorText == color)

def test_beadworkView_setBeadSize(mainWindow):
    view = mainWindow.beadworkView

    # set row width and height to be something else than default
    for i in range(view.model().rowCount(None)):
        view.setRowHeight(i, 30)
    for i in range(view.model().columnCount(None)):
        view.setColumnWidth(i, 30)

    view.setBeadSize()
    
    # ensure that they all get set back properly
    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.bead_height)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.bead_width)

def test_beadworkView_changeOrientationOnce(mainWindow):
    view = mainWindow.beadworkView
    view.changeOrientation()

    assert(view.bead_height == 12)
    assert(view.bead_width == 22)

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.bead_height)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.bead_width)

def test_beadworkView_changeOrientationOTwice(mainWindow):
    view = mainWindow.beadworkView
    view.changeOrientation()

    assert(view.bead_height == 12)
    assert(view.bead_width == 22)

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.bead_height)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.bead_width)

    view.changeOrientation()

    assert(view.bead_height == 22)
    assert(view.bead_width == 12)

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.bead_height)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.bead_width)