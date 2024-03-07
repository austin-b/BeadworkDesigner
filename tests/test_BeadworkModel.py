import re
import pytest

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from BeadworkDesigner.BeadworkModel import BeadworkModel, BeadworkTransposeModel

# TODO: create test for BeadworkModel init with data
# TODO: create test for TransposeModel

def is_hex_color(s):
    return bool(re.fullmatch(r'#[0-9a-fA-F]{6}', s))

### TESTING BEADWORKMODEL ###

def test_BeadworkModel_init_nodata():
    testModel = BeadworkModel()

    # TEST FOR NOT EMPTY
    assert(len(testModel._data) != 0)
    assert(len(testModel._data[0]) != 0)

    # TEST FOR WHITE DEFAULT WHEN NOT DEBUG
    assert(data == "#FFFFFF" for row in testModel._data for data in row)

    # TEST FOR RANDOM COLOR DEFAULT WHEN DEBUG
    testModel = BeadworkModel(debug=True)
    assert(data != "#FFFFFF" for row in testModel._data for data in row)

@pytest.fixture
def testingModel():
    return BeadworkModel(debug=True)

def test_BeadworkModel_rowCount(testingModel):
    assert(testingModel.rowCount(None) == len(testingModel._data))

def test_BeadworkModel_columnCount(testingModel):
    assert(testingModel.columnCount(None) == len(testingModel._data[0]))

def test_BeadworkModel_data(testingModel):
    for row in range(testingModel.rowCount(None)):
        for column in range(testingModel.columnCount(None)):
            assert(is_hex_color(testingModel.data(testingModel.index(row, column), Qt.ItemDataRole.DisplayRole)))
            assert(testingModel.data(testingModel.index(row, column), Qt.ItemDataRole.BackgroundRole) == QColor(testingModel.data(testingModel.index(row, column), Qt.ItemDataRole.DisplayRole)))
            assert(testingModel.data(testingModel.index(row, column), Qt.ItemDataRole.DecorationRole) == QColor(testingModel.data(testingModel.index(row, column), Qt.ItemDataRole.DisplayRole)))

def test_BeadworkModel_setData(testingModel):
    for row in range(testingModel.rowCount(None)):
        for column in range(testingModel.columnCount(None)):
            testingModel.setData(testingModel.index(row, column), "#000000", Qt.ItemDataRole.EditRole)
            assert(testingModel.data(testingModel.index(row, column), Qt.ItemDataRole.DisplayRole) == "#000000")

# TODO: make test for checking that these add the proper row
# 0, 4, and 9 should mark the beginning, middle(ish), and end of the debug data
@pytest.mark.parametrize("input_row", [0, 4, 9])
def test_BeadworkModel_insertRow(testingModel, input_row):
    rowCountBefore = testingModel.rowCount(None)
    index = testingModel.index(input_row, 0)
    testingModel.insertRow(rowCountBefore, index)
    assert(testingModel.rowCount(None) == rowCountBefore + 1)

# TODO: make test for checking that these add the proper column
# 0, 3, and 7 should mark the beginning, middle(ish), and end of the debug data
@pytest.mark.parametrize("input_column", [0, 3, 7])
def test_BeadworkModel_insertColumn(testingModel, input_column):
    columnCountBefore = testingModel.columnCount(None)
    index = testingModel.index(0, input_column)
    testingModel.insertColumn(columnCountBefore, index)
    assert(testingModel.columnCount(None) == columnCountBefore + 1)

# TODO: make test for checking that these remove the proper row
@pytest.mark.parametrize("input_row", [0, 3, 5])
def test_BeadworkModel_removeRow(testingModel, input_row):
    rowCountBefore = testingModel.rowCount(None)
    index = testingModel.index(input_row, 0)
    testingModel.removeRow(input_row, index)
    assert(testingModel.rowCount(None) == rowCountBefore - 1)

# TODO: make test for checking that these remove the proper column
@pytest.mark.parametrize("input_column", [0, 2])
def test_BeadworkModel_removeColumn(testingModel, input_column):
    columnCountBefore = testingModel.columnCount(None)
    index = testingModel.index(0, input_column)
    testingModel.removeColumn(input_column, index)
    assert(testingModel.columnCount(None) == columnCountBefore - 1)

def test_BeadworkModel_exportDict(testingModel):
    testDict = testingModel.exportDict()
    assert(testDict == {"project": testingModel._data})

def test_BeadworkModel_importDict(testingModel):
    testDict = testingModel.exportDict()
    testModel = BeadworkModel()
    testModel.importDict(testDict)
    assert(testModel._data == testingModel._data)


### TESTING BEADWORKTRANSPOSEMODEL ###

@pytest.fixture
def testingTransposeModels():
    testModel = BeadworkModel(debug=True)
    testTransposeModel = BeadworkTransposeModel()
    testTransposeModel.setSourceModel(testModel)
    return (testModel, testTransposeModel)

def test_BeadworkTransposeModel_init(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    assert(testTransposeModel.sourceModel() == testModel)

def test_BeadworkTransposeModel_rowCount(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    assert(testTransposeModel.rowCount(None) == testModel.columnCount(None))

def test_BeadworkTransposeModel_columnCount(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    assert(testTransposeModel.columnCount(None) == testModel.rowCount(None))

def test_BeadworkTransposeModel_data(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    for row in range(testModel.rowCount(None)):
        for column in range(testModel.columnCount(None)):
            assert(testTransposeModel.data(testTransposeModel.index(column, row), Qt.ItemDataRole.DisplayRole) == testModel.data(testModel.index(row, column), Qt.ItemDataRole.DisplayRole))
            assert(testTransposeModel.data(testTransposeModel.index(column, row), Qt.ItemDataRole.BackgroundRole) == testModel.data(testModel.index(row, column), Qt.ItemDataRole.BackgroundRole))
            assert(testTransposeModel.data(testTransposeModel.index(column, row), Qt.ItemDataRole.DecorationRole) == testModel.data(testModel.index(row, column), Qt.ItemDataRole.DecorationRole))

def test_BeadworkTransposeModel_setData(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    for row in range(testModel.rowCount(None)):
        for column in range(testModel.columnCount(None)):
            testTransposeModel.setData(testTransposeModel.index(column, row), "#000000", Qt.ItemDataRole.EditRole)
            assert(testTransposeModel.data(testTransposeModel.index(column, row), Qt.ItemDataRole.DisplayRole) == "#000000")
            assert(testModel.data(testModel.index(row, column), Qt.ItemDataRole.DisplayRole) == "#000000")

def test_BeadworkTransposeModel_insertRow(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    rowCountBefore = testTransposeModel.rowCount(None)
    index = testTransposeModel.index(0, 0)
    testTransposeModel.insertRow(rowCountBefore, index)
    assert(testTransposeModel.rowCount(None) == rowCountBefore + 1)
    assert(testModel.columnCount(None) == rowCountBefore + 1)

def test_BeadworkTransposeModel_insertColumn(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    columnCountBefore = testTransposeModel.columnCount(None)
    index = testTransposeModel.index(0, 0)
    testTransposeModel.insertColumn(columnCountBefore, index)
    assert(testTransposeModel.columnCount(None) == columnCountBefore + 1)
    assert(testModel.rowCount(None) == columnCountBefore + 1)

def test_BeadworkTransposeModel_removeRow(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    rowCountBefore = testTransposeModel.rowCount(None)
    index = testTransposeModel.index(0, 0)
    testTransposeModel.removeRow(0, index)
    assert(testTransposeModel.rowCount(None) == rowCountBefore - 1)
    assert(testModel.columnCount(None) == rowCountBefore - 1)

def test_BeadworkTransposeModel_removeColumn(testingTransposeModels):
    testModel, testTransposeModel = testingTransposeModels
    columnCountBefore = testTransposeModel.columnCount(None)
    index = testTransposeModel.index(0, 0)
    testTransposeModel.removeColumn(0, index)
    assert(testTransposeModel.columnCount(None) == columnCountBefore - 1)
    assert(testModel.rowCount(None) == columnCountBefore - 1)