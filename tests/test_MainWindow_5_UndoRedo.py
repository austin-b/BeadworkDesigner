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

    rowCountBefore = mainWindow.beadworkView.model().rowCount(None)

    # try with multiple rows in middle
    command = CommandInsertRow(mainWindow.model, mainWindow.beadworkView, 
                               2, 3, f"Add 3 rows at index 2")
    mainWindow.undoStack.push(command)

    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore + 3)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore)

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore + 3)

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

    rowCountBefore = mainWindow.beadworkView.model().rowCount(None)

    rowBefore = [[mainWindow.model.data(mainWindow.model.index(2+r, c), 
                                       role=Qt.ItemDataRole.DisplayRole) 
                        for c in range(mainWindow.model.columnCount(None))]
                        for r in range(3)]

    # try with multiple rows in middle
    command = CommandRemoveRow(mainWindow.model, mainWindow.beadworkView, 
                               2, 3, f"Add 3 rows at index 2")
    mainWindow.undoStack.push(command)

    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore - 3)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore)

    assert(all([
        mainWindow.model.data(mainWindow.model.index(2+r, c), 
                              role=Qt.ItemDataRole.DisplayRole) 
        == rowBefore[r][c] for c in range(mainWindow.model.columnCount(None)) for r in range(3)]))

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore - 3)