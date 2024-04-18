import pytest
import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.BeadworkModel import BeadworkModel
from BeadworkDesigner.ColorList import BeadworkToColorListProxyModel

from bin.config import app_configs, project_configs

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
    testBeadworkModel.dataChanged.connect(testProxyModel.updateList)
    return testProxyModel

def test_colorList_initModel(testBeadworkModel, testProxyModel):
    assert(testProxyModel.sourceModel() == testBeadworkModel)

def test_colorList_initColumns(testProxyModel):
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

def test_colorList_data(testProxyModel):
    for r in range(testProxyModel.rowCount(None)):
        color = testProxyModel._colors_index[r]
        assert(testProxyModel.data(testProxyModel.index(r, 0), Qt.ItemDataRole.DisplayRole) == color)
        assert(testProxyModel.data(testProxyModel.index(r, 0), Qt.ItemDataRole.BackgroundRole) == QColor(color))

def test_colorList_returnAllInstancesOfColor(testBeadworkModel, testProxyModel):
    # ensure at least two of the same color are present
    testBeadworkModel.setData(testBeadworkModel.index(0,0), "#000000", Qt.ItemDataRole.EditRole)
    testBeadworkModel.setData(testBeadworkModel.index(0,1), "#000000", Qt.ItemDataRole.EditRole)
    proxModelIndex = testProxyModel.createIndex(testProxyModel._colors_index.index("#000000"), 0)
    testIndexes = testProxyModel.mapToAllSourceIndexes(proxModelIndex)
    assert(testBeadworkModel.index(0,0) in testIndexes)
    assert(testBeadworkModel.index(0,1) in testIndexes)

def test_colorList_changeAllInstancesOfColor(testBeadworkModel, testProxyModel):
    # ensure at least two of the same color are present
    testBeadworkModel.setData(testBeadworkModel.index(0,0), "#000000", Qt.ItemDataRole.EditRole)
    testBeadworkModel.setData(testBeadworkModel.index(0,1), "#000000", Qt.ItemDataRole.EditRole)
    testIndexes = testProxyModel.allIndexesForColor("#000000") # get all indexes for init color
    
    testProxyModel.changeAllInstancesOfColor("#000000", "#FFFFFF")

    for index in testIndexes:
        assert(testBeadworkModel.data(index, Qt.ItemDataRole.DisplayRole) == "#FFFFFF")

def test_colorList_changeDataFromColorDialog(qtbot):
    main = MainWindow(debug=False, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(main)
    main.show()

    main.currentColor.setText("000000")
    assert(main.colorListModel.data(main.colorListModel.index(0,0), Qt.ItemDataRole.DisplayRole) == "#000000")