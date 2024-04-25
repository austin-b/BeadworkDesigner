import os
import pytest

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from BeadworkDesigner.MainWindow import MainWindow
from BeadworkDesigner.utils import readConfigFile

project_configs, app_configs = readConfigFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../bin/config.json"))  # import config file

####################
# TODO: test SelectionMode
####################

def test_beadworkView_init(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView
    assert(view.isVisible())
    assert(view.model() == mainWindow.origModel)
    assert(view.itemDelegate() == mainWindow.delegate)
    assert(view.showGrid() == False)
    assert(view.beadHeight == mainWindow.getConfig("beadHeight"))  # default value
    assert(view.beadWidth == mainWindow.getConfig("beadWidth"))   # default value
    assert(view.rowHeight(0) == view.beadHeight)  # default value
    assert(view.columnWidth(0) == view.beadWidth) # default value
    assert(view.verticalHeader().isVisible())
    assert(view.horizontalHeader().isVisible())
    assert(view.verticalHeader().count() == project_configs["height"])
    assert(view.horizontalHeader().count() == project_configs["width"])

def test_beadworkView_data(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    testRow, testColumn = 0, 0
    color = mainWindow.model.data(mainWindow.model.index(testRow, testColumn), Qt.ItemDataRole.DisplayRole)

    view.clicked.emit(view.model().index(testRow, testColumn))

    currentColorText = mainWindow.currentColor.text()

    assert(f"#{currentColorText}" == color)

def test_beadworkView_selectListOfBeads(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    testRow, testColumn = 0, 0
    view.clicked.emit(view.model().index(testRow, testColumn))

    selection = [view.model().index(testRow, testColumn)]

    view.selectListOfBeads(selection)

    assert(view.selectionModel().selectedIndexes() == selection)

    testRow, testColumn = 2, 2
    view.clicked.emit(view.model().index(testRow, testColumn))

    selection.append(view.model().index(testRow, testColumn))

    view.selectListOfBeads(selection)

    assert(view.selectionModel().selectedIndexes() == selection)

def test_beadworkView_changeBeadColorFromDialog(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
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
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    # set row width and height to be something else than default
    for i in range(view.model().rowCount(None)):
        view.setRowHeight(i, 30)
    for i in range(view.model().columnCount(None)):
        view.setColumnWidth(i, 30)

    # set bead size back to stored values
    view.setBeadSize()
    
    # ensure that they all get set back properly
    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.beadHeight)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.beadWidth)

    # set bead size to something else than default
    view.setBeadSize(40, 40)

    # ensure that they all got set
    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == 40)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == 40)

def test_beadworkView_changeOrientationOnce(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView
    view.changeOrientation()

    assert(view.beadHeight == mainWindow.getConfig("beadWidth"))
    assert(view.beadWidth == mainWindow.getConfig("beadHeight"))

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.beadHeight)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.beadWidth)

def test_beadworkView_changeOrientationOTwice(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView
    view.changeOrientation()

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    assert(view.beadHeight == mainWindow.getConfig("beadWidth"))
    assert(view.beadWidth == mainWindow.getConfig("beadHeight"))

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.beadHeight)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.beadWidth)

    view.changeOrientation()

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    assert(view.beadHeight == mainWindow.getConfig("beadHeight"))
    assert(view.beadWidth == mainWindow.getConfig("beadWidth"))

    for i in range(view.model().rowCount(None)):
        assert(view.rowHeight(i) == view.beadHeight)
    for i in range(view.model().columnCount(None)):
        assert(view.columnWidth(i) == view.beadWidth)

def test_beadworkView_changeHeight(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    currentHeight = mainWindow.modelHeight
    mainWindow.addRowAction.trigger()

    assert(view.model().rowCount(None) == currentHeight + 1)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    currentHeight = mainWindow.modelHeight
    mainWindow.removeRowAction.trigger()

    assert(view.model().rowCount(None) == currentHeight - 1)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    currentHeight = mainWindow.modelHeight
    mainWindow.changeHeightTo(16)

    assert(view.model().rowCount(None) == 16)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    mainWindow.changeHeightTo(currentHeight)

    assert(view.model().rowCount(None) == currentHeight)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))


def test_beadworkView_changeWidth(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    currentWidth = mainWindow.modelWidth
    mainWindow.addColumnAction.trigger()

    assert(view.model().columnCount(None) == currentWidth + 1)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    currentWidth = mainWindow.modelWidth
    mainWindow.removeColumnAction.trigger()

    assert(view.model().columnCount(None) == currentWidth - 1)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    currentWidth = mainWindow.modelWidth
    mainWindow.changeWidthTo(16)

    assert(view.model().columnCount(None) == 16)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    mainWindow.changeWidthTo(currentWidth)

    assert(view.model().columnCount(None) == currentWidth)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

def test_beadworkView_changeHeightAfterOrientation(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    view.changeOrientation()

    currentHeight = mainWindow.modelHeight
    mainWindow.addRowAction.trigger()

    assert(view.model().rowCount(None) == currentHeight + 1)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    currentHeight = mainWindow.modelHeight
    mainWindow.removeRowAction.trigger()

    assert(view.model().rowCount(None) == currentHeight - 1)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    currentHeight = mainWindow.modelHeight
    mainWindow.changeHeightTo(16)

    assert(view.model().rowCount(None) == 16)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    mainWindow.changeHeightTo(currentHeight)

    assert(view.model().rowCount(None) == currentHeight)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

def test_beadworkView_changeWidthAfterOrientation(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    view.changeOrientation()

    currentWidth = mainWindow.modelWidth
    mainWindow.addColumnAction.trigger()

    assert(view.model().columnCount(None) == currentWidth + 1)
    
    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))
    currentWidth = mainWindow.modelWidth
    mainWindow.removeColumnAction.trigger()

    assert(view.model().columnCount(None) == currentWidth - 1)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    currentWidth = mainWindow.modelWidth
    mainWindow.changeWidthTo(16)

    assert(view.model().columnCount(None) == 16)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

    mainWindow.changeWidthTo(currentWidth)

    assert(view.model().columnCount(None) == currentWidth)

    assert(view.verticalHeader().count() == view.model().rowCount(None))
    assert(view.horizontalHeader().count() == view.model().columnCount(None))

def test_beadworkView_colorMode(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    mainWindow.colorMode.trigger()
    mainWindow.currentColor.setText("FF0000")

    testRow, testColumn = 0, 0

    view.clicked.emit(view.model().index(testRow, testColumn))

    assert(view.model().data(view.model().index(testRow, testColumn), Qt.ItemDataRole.DisplayRole) == "#FF0000")
    
    testRow, testColumn = 2, 2

    view.clicked.emit(view.model().index(testRow, testColumn))

    assert(view.model().data(view.model().index(testRow, testColumn), Qt.ItemDataRole.DisplayRole) == "#FF0000")

def test_beadworkView_clearMode(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    mainWindow.clearMode.trigger()

    testRow, testColumn = 0, 0

    view.clicked.emit(view.model().index(testRow, testColumn))

    assert(view.model().data(view.model().index(testRow, testColumn), Qt.ItemDataRole.DisplayRole) == "#FFFFFF")

    testRow, testColumn = 2, 2

    view.clicked.emit(view.model().index(testRow, testColumn))

    assert(view.model().data(view.model().index(testRow, testColumn), Qt.ItemDataRole.DisplayRole) == "#FFFFFF")

def test_beadworkView_zoomIn(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    beadHeightBefore = view.beadHeight
    beadWidthBefore = view.beadWidth

    mainWindow.zoomIn()

    assert(view.beadHeight == beadHeightBefore + 1)
    assert(view.beadWidth == beadWidthBefore + 1)

    mainWindow.zoomIn()

    assert(view.beadHeight == beadHeightBefore + 2)
    assert(view.beadWidth == beadWidthBefore + 2)

def test_beadworkView_zoomOut(qtbot):
    mainWindow = MainWindow(debug=True, app_configs=app_configs, project_configs=project_configs)
    qtbot.addWidget(mainWindow)
    mainWindow.show()
    view = mainWindow.beadworkView

    beadHeightBefore = view.beadHeight
    beadWidthBefore = view.beadWidth

    mainWindow.zoomOut()

    assert(view.beadHeight == beadHeightBefore - 1)
    assert(view.beadWidth == beadWidthBefore - 1)

    mainWindow.zoomOut()

    assert(view.beadHeight == beadHeightBefore - 2)
    assert(view.beadWidth == beadWidthBefore - 2)