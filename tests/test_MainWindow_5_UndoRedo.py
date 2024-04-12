import pytest

from PySide6.QtCore import Qt

from BeadworkDesigner.MainWindow import MainWindow

from bin.config import configs

@pytest.fixture
def mainWindow(qtbot):
    window = MainWindow(debug=True, configs=configs)
    qtbot.addWidget(window)
    return window

def test_undoRedo_CommandChangeColor(mainWindow):
    mainWindow.colorMode.trigger()
    mainWindow.currentColor.setText("#FF0000")

    oldColor = mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 0), Qt.ItemDataRole.DisplayRole)

    mainWindow.beadworkView.clicked.emit(mainWindow.beadworkView.model().index(0, 0))

    assert(mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 0), Qt.ItemDataRole.DisplayRole) == "#FF0000")

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 0), Qt.ItemDataRole.DisplayRole) == oldColor)
    
    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 0), Qt.ItemDataRole.DisplayRole) == "#FF0000")

def test_UndoRedo_CommandInsertRow(mainWindow):
    rowCountBefore = mainWindow.beadworkView.model().rowCount(None)

    mainWindow.addRowAction.trigger()

    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore + 1)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore)

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore + 1)
