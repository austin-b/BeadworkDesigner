import pytest
import logging

from PySide6.QtCore import Qt

from BeadworkDesigner.BeadworkModel import BeadworkModel
from BeadworkDesigner.ColorList import BeadworkToColorListProxyModel

# creates a list of unique colors from the BeadworkModel
def uniqueColors(model):
        colors = list(set([color for row in model._data for color in row]))
        colors.sort()
        return colors

@pytest.fixture
def testBeadworkModel():
    return BeadworkModel(debug=True)

@pytest.fixture
def testProxyModel(testBeadworkModel):
    testProxyModel = BeadworkToColorListProxyModel()
    testProxyModel.setSourceModel(testBeadworkModel)
    return testProxyModel

def test_colorList_initModel(testBeadworkModel, testProxyModel):
    assert(testProxyModel.sourceModel() == testBeadworkModel)

def test_colorList_initColumns(testBeadworkModel, testProxyModel):
    assert(testProxyModel.columnCount(None) == 1)

def test_colorList_initRows(testBeadworkModel, testProxyModel):
    assert(testProxyModel.rowCount(None) == len(uniqueColors(testBeadworkModel)))

def test_colorList_initColors(testBeadworkModel, testProxyModel):
    colors = uniqueColors(testBeadworkModel)
    logging.debug(f"length: {len(colors)}, data: {colors}")
    assert(testProxyModel._colors_index == colors)
    for color in colors:
         assert(color in testProxyModel._colors)

def test_colorList_mapFromSource(testBeadworkModel, testProxyModel):
    for r in range(testBeadworkModel.rowCount(None)):
        for c in range(testBeadworkModel.columnCount(None)):
            index = testBeadworkModel.index(r, c)
            color = testBeadworkModel.data(index, Qt.ItemDataRole.DisplayRole)
            assert(testProxyModel.mapFromSource(index) == testProxyModel.createIndex(testProxyModel._colors_index.index(color), 0))


def test_colorList_mapToSource(testBeadworkModel, testProxyModel):
    for r in range(testProxyModel.rowCount(None)):
        color = testProxyModel.index(r, 0).data(Qt.ItemDataRole.DisplayRole)
        index = testProxyModel.mapToSource(testProxyModel.index(r, 0)) # should return only the first index that matches the color
        assert(testBeadworkModel.data(index, Qt.ItemDataRole.DisplayRole) == color)

def test_colorList_data(qtbot):
    pass

def test_colorList_changeData(qtbot):
    pass

def test_colorList_changeAllInstancesOfColor(qtbot):
    pass