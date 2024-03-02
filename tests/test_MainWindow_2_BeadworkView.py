import pytest

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from BeadworkDesigner.MainWindow import MainWindow

from bin.config import configs

####################
# TODO: test SelectionMode
####################

def test_beadworkView_init(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView
    assert(view.isVisible())
    assert(view.model() == mainWindow.origModel)
    assert(view.itemDelegate() == mainWindow.delegate)
    assert(not view.verticalHeader().isVisible())
    assert(not view.horizontalHeader().isVisible())
    assert(view.showGrid() == False)
    assert(view.beadHeight == 22)  # default value
    assert(view.beadWidth == 12)   # default value
    assert(view.rowHeight(0) == view.beadHeight)  # default value
    assert(view.columnWidth(0) == view.beadWidth) # default value

def test_beadworkView_data(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    testRow, testColumn = 0, 0
    color = mainWindow.model.data(mainWindow.model.index(testRow, testColumn), Qt.ItemDataRole.DisplayRole)

    view.clicked.emit(view.model().index(testRow, testColumn))

    currentColorText = mainWindow.currentColor.text()

    assert(f"#{currentColorText}" == color)

def test_beadworkView_changeBeadColorFromDialog(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    testRow, testColumn = 0, 0
    view.setCurrentIndex(view.model().index(testRow, testColumn))

    mainWindow.currentColor.setText("FF0000")

    testColor = mainWindow.model.data(mainWindow.model.index(testRow, testColumn), Qt.ItemDataRole.DisplayRole)

    currentColorText = mainWindow.currentColor.text()

    assert(f"#{currentColorText}" == testColor)

    mainWindow.colorDialog.colorSelected.emit(QColor("#00FF00"))

    testColor = mainWindow.model.data(mainWindow.model.index(testRow, testColumn), Qt.ItemDataRole.DisplayRole)

    assert(testColor == "#00FF00")

def test_beadworkView_setBeadSize(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    # set row width and height to be something else than default
    for i in range(view.model().rowCount(None)):
        view.setRowHeight(i, 30)
    for i in range(view.model().columnCount(None)):
        view.setColumnWidth(i, 30)

    view.setBeadSize()
    
    # ensure that they all get set back properly
    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.beadHeight)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.beadWidth)

def test_beadworkView_changeOrientationOnce(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView
    view.changeOrientation()

    assert(view.beadHeight == 12)
    assert(view.beadWidth == 22)

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.beadHeight)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.beadWidth)

def test_beadworkView_changeOrientationOTwice(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView
    view.changeOrientation()

    assert(view.beadHeight == 12)
    assert(view.beadWidth == 22)

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.beadHeight)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.beadWidth)

    view.changeOrientation()

    assert(view.beadHeight == 22)
    assert(view.beadWidth == 12)

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.beadHeight)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.beadWidth)

# TODO: test for direct input values of any kind, not just current+1
def test_beadworkView_changeHeight(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    # add a row from the spinbox
    currentHeight = mainWindow.heightSpinBox.value()
    mainWindow.heightSpinBox.setValue(currentHeight + 1)

    assert(view.model().rowCount(None) == currentHeight + 1)

    # remove a row from the spinbox
    currentHeight = mainWindow.heightSpinBox.value()
    mainWindow.heightSpinBox.setValue(currentHeight - 1)

    assert(view.model().rowCount(None) == currentHeight - 1)

# TODO: test for direct input values of any kind, not just current+1
def test_beadworkView_changeWidth(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    currentWidth = mainWindow.widthSpinBox.value()
    mainWindow.widthSpinBox.setValue(currentWidth + 1)

    assert(view.model().columnCount(None) == currentWidth + 1)

    currentWidth = mainWindow.widthSpinBox.value()
    mainWindow.widthSpinBox.setValue(currentWidth - 1)

    assert(view.model().columnCount(None) == currentWidth - 1)

# TODO: test for direct input values of any kind, not just current+1
def test_beadworkView_changeHeightAfterOrientation(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    view.changeOrientation()

    currentHeight = mainWindow.heightSpinBox.value()
    mainWindow.heightSpinBox.setValue(currentHeight + 1)

    assert(view.model().rowCount(None) == currentHeight + 1)

    currentHeight = mainWindow.heightSpinBox.value()
    mainWindow.heightSpinBox.setValue(currentHeight - 1)

    assert(view.model().rowCount(None) == currentHeight - 1)

# TODO: test for direct input values of any kind, not just current+1
def test_beadworkView_changeWidthAfterOrientation(qtbot):
    mainWindow = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    view.changeOrientation()

    currentWidth = mainWindow.widthSpinBox.value()
    mainWindow.widthSpinBox.setValue(currentWidth + 1)

    assert(view.model().columnCount(None) == currentWidth + 1)

    currentWidth = mainWindow.widthSpinBox.value()
    mainWindow.widthSpinBox.setValue(currentWidth - 1)

    assert(view.model().columnCount(None) == currentWidth - 1)