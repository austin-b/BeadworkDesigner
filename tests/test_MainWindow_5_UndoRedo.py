import pytest

from PySide6.QtCore import Qt

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.Commands import (CommandChangeColor, 
                                       CommandInsertRow, 
                                       CommandRemoveRow,
                                       CommandInsertColumn,
                                       CommandRemoveColumn)

from bin.config import app_configs, project_configs

@pytest.fixture
def mainWindow(qtbot):
    window = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
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

def test_UndoRedo_CommandChangeMultipleColors(mainWindow):
    mainWindow.colorMode.trigger()

    oldColors = {mainWindow.beadworkView.model().index(0, 0): mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 0), Qt.ItemDataRole.DisplayRole),
                 mainWindow.beadworkView.model().index(0, 1): mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 1), Qt.ItemDataRole.DisplayRole),
                 mainWindow.beadworkView.model().index(0, 2): mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 2), Qt.ItemDataRole.DisplayRole)}

    mainWindow.beadworkView.selectListOfBeads([mainWindow.beadworkView.model().index(0, 0),
                                                mainWindow.beadworkView.model().index(0, 1),
                                                mainWindow.beadworkView.model().index(0, 2)])
    
    mainWindow.currentColor.setText("#FF0000")

    assert(mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 0), Qt.ItemDataRole.DisplayRole) == "#FF0000")
    assert(mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 1), Qt.ItemDataRole.DisplayRole) == "#FF0000")
    assert(mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 2), Qt.ItemDataRole.DisplayRole) == "#FF0000")

    mainWindow.undoAction.trigger()
    assert(all([mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 0), Qt.ItemDataRole.DisplayRole) == oldColors[mainWindow.beadworkView.model().index(0, 0)],
                mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 1), Qt.ItemDataRole.DisplayRole) == oldColors[mainWindow.beadworkView.model().index(0, 1)],
                mainWindow.beadworkView.model().data(mainWindow.beadworkView.model().index(0, 2), Qt.ItemDataRole.DisplayRole) == oldColors[mainWindow.beadworkView.model().index(0, 2)]]))

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

    # try with multiple rows at end
    rowCountBefore = mainWindow.beadworkView.model().rowCount(None)

    rowBefore = [[mainWindow.model.data(mainWindow.model.index(rowCountBefore-1-r, c),
                                       role=Qt.ItemDataRole.DisplayRole)
                        for c in range(mainWindow.model.columnCount(None))]
                        for r in range(3)]
    
    command = CommandRemoveRow(mainWindow.model, mainWindow.beadworkView,
                                  rowCountBefore-3, 3, f"Remove 3 rows at end")
    
    mainWindow.undoStack.push(command)

    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore - 3)

    mainWindow.undoAction.trigger()

    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore)

    assert(all([mainWindow.model.data(mainWindow.model.index(rowCountBefore-1-r, c),
                                      role=Qt.ItemDataRole.DisplayRole)
                == rowBefore[r][c] for c in range(mainWindow.model.columnCount(None)) for r in range(3)]))

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().rowCount(None) == rowCountBefore - 3)

def test_UndoRedo_CommandInsertColumn(mainWindow):
    columnCountBefore = mainWindow.beadworkView.model().columnCount(None)

    mainWindow.addColumnAction.trigger()

    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore + 1)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore)

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore + 1)

    columnCountBefore = mainWindow.beadworkView.model().columnCount(None)

    # try with multiple columns in middle
    command = CommandInsertColumn(mainWindow.model, mainWindow.beadworkView, 
                               2, 3, f"Add 3 columns at index 2")
    mainWindow.undoStack.push(command)

    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore + 3)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore)

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore + 3)

def test_UndoRedo_CommandRemoveColumn(mainWindow):
    columnCountBefore = mainWindow.beadworkView.model().columnCount(None)

    columnBefore = [mainWindow.model.data(mainWindow.model.index(r, mainWindow.model.columnCount(None)-1), role=Qt.ItemDataRole.DisplayRole) for r in range(mainWindow.model.rowCount(None))]

    mainWindow.removeColumnAction.trigger()

    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore - 1)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore)
    assert(all([
        mainWindow.model.data(mainWindow.model.index(r, mainWindow.model.columnCount(None)-1), role=Qt.ItemDataRole.DisplayRole) 
        == columnBefore[r] for r in range(mainWindow.model.rowCount(None))]) == True)

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore - 1)

    columnCountBefore = mainWindow.beadworkView.model().columnCount(None)

    columnBefore = [[mainWindow.model.data(mainWindow.model.index(r, 2+c), 
                                       role=Qt.ItemDataRole.DisplayRole) 
                        for r in range(mainWindow.model.rowCount(None))]
                        for c in range(3)]

    # try with multiple columns in middle
    command = CommandRemoveColumn(mainWindow.model, mainWindow.beadworkView, 
                               2, 3, f"Add 3 columns at index 2")
    mainWindow.undoStack.push(command)

    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore - 3)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore)

    assert(all([mainWindow.model.data(mainWindow.model.index(r, 2+c), 
                              role=Qt.ItemDataRole.DisplayRole) 
        == columnBefore[c][r] for r in range(mainWindow.model.rowCount(None)) for c in range(3)]))

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore - 3)

    # try with multiple columns at end
    columnCountBefore = mainWindow.beadworkView.model().columnCount(None)

    columnBefore = [[mainWindow.model.data(mainWindow.model.index(r, columnCountBefore-1-c),
                                       role=Qt.ItemDataRole.DisplayRole) 
                        for r in range(mainWindow.model.rowCount(None))]
                        for c in range(3)]
    
    command = CommandRemoveColumn(mainWindow.model, mainWindow.beadworkView,
                                  columnCountBefore-3, 3, f"Remove 3 columns at end")
    
    mainWindow.undoStack.push(command)

    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore - 3)

    mainWindow.undoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore)

    assert(all([mainWindow.model.data(mainWindow.model.index(r, columnCountBefore-1-c),
                                      role=Qt.ItemDataRole.DisplayRole) 
                == columnBefore[c][r] for r in range(mainWindow.model.rowCount(None)) for c in range(3)]))

    mainWindow.redoAction.trigger()
    assert(mainWindow.beadworkView.model().columnCount(None) == columnCountBefore - 3)
