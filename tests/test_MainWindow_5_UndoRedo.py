import pytest

from PySide6.QtCore import Qt

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.Commands import (CommandChangeColor, CommandInsertRow, CommandRemoveRow)

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

def test_UndoRedo_CommandRemoveRow(mainWindow):
    rowCountBefore = mainWindow.beadworkView.model().rowCount(None)

    rowBefore = [mainWindow.model.data(mainWindow.model.index(mainWindow.model.rowCount(None)-1, c), role=Qt.ItemDataRole.DisplayRole) for c in range(mainWindow.model.columnCount(None))]

    mainWindow.removeRowAction.trigger()

    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore - 1)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore)
    assert(all([
        mainWindow.model.data(mainWindow.model.index(mainWindow.model.rowCount(None)-1, c), role=Qt.ItemDataRole.DisplayRole) 
        == rowBefore[c] for c in range(mainWindow.model.columnCount(None))]) == True)

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore - 1)