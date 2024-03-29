"""
Icons are provided by https://p.yusukekamiyamane.com/. They are licensed under a Creative Commons Attribution 3.0 License.
"""

#####################
#
# TODO: add Save As file menu action
# TODO: add "New Project" option to menu
#       - have loadNewProject - needs to import default config and create blank project, not load default
#       - OR: load default_project.json, but not allow Save, only Save As (determine via non-existent title field?)
# TODO: change from RGB hex to HSV
# TODO: add docstrings
# TODO: add localization
# TODO: font options
# TODO: add a way to change the size of the beads
# TODO: add a way to zoom in and out
# TODO: add a way to change the color of the background
# TODO: add a "bucket fill" option/tool
# TODO: implement undo and redo functionality
#       - https://www.informit.com/articles/article.aspx?p=1187104&seqNum=3
#       - https://doc.qt.io/qtforpython-6/overviews/qundo.html
#       - https://doc.qt.io/qtforpython-6/PySide6/QtGui/QUndoStack.html#qundostack
# TODO: implement a copy and paste functionality for selected beads
# TODO: add a way to align beads horizontally and vertically
# TODO: implement a way to group and ungroup beads for easier manipulation
# TODO: Add a way to add text labels or annotations to the beadwork design
# TODO: add a way to print or export to PDF
#
#####################

import logging
import os
from enum import Enum

from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QColorDialog, QComboBox, QFileDialog,
                               QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                               QPushButton, QSpinBox, QStatusBar, QToolBar,
                               QVBoxLayout, QWidget)

import BeadworkDesigner.utils as utils
from BeadworkDesigner.BeadDelegate import BeadDelegate
from BeadworkDesigner.BeadworkModel import (BeadworkModel,
                                            BeadworkTransposeModel)
from BeadworkDesigner.BeadworkView import BeadworkView
from BeadworkDesigner.ColorList import BeadworkToColorListProxyModel, ColorList

logger = logging.getLogger(__name__)

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
bin_dir = os.path.join(base_dir, "bin")
icons_dir = os.path.join(bin_dir, "icons")
qss_dir = os.path.join(bin_dir, "qss")

class BeadworkOrientation(Enum):
    VERTICAL = 0
    HORIZONTAL = 1

class MainWindow(QMainWindow):
    def __init__(self, debug=False, configs=None, modelData=None):
        super().__init__()

        self.debug = debug
        self.configs = configs

        # set initial orientation dict as we need nice string representations
        # TODO: is this needed if I replace the width x label spinbox?
        # TODO: or do I replace Enum with a StrEnum which has a nice string representation? https://docs.python.org/3/library/enum.html#enum.StrEnum
        self.orientationOptions = {BeadworkOrientation.HORIZONTAL: "Horizontal", BeadworkOrientation.VERTICAL: "Vertical"}
        
        logger.info("Initializing MainWindow.")

        ### TRACK INITIAL ORIENTATION
        if self.configs["defaultOrientation"] == "Horizontal":
            self.currentOrientation = BeadworkOrientation.HORIZONTAL
        else:
            self.currentOrientation = BeadworkOrientation.VERTICAL
        
        ### SETUP MODELS & VIEW
        self.setupModels(self.configs["height"], self.configs["width"], modelData)
        self.setupView(self.configs["beadHeight"], self.configs["beadWidth"])

        ### KEEP TRACK OF INITIAL WIDTH x HEIGHT
        self.modelWidth = self.model.columnCount(QModelIndex())
        self.modelHeight = self.model.rowCount(QModelIndex())
        logger.debug(f"Model width: {self.modelWidth}, Model height: {self.modelHeight}.")

        ### SETUP OTHER GUI ELEMENTS
        # self.setupWidthXHeightWidget()
        self.setupOrientationWidget()
        self.setupColorDialogWidget()
        self.setupColorList()
        self.setupSidebar()
        self.setupActions()
        self.setupToolbar()  
        self.setupStatusBar()
        self.setupMenu()
        self.setupDimensionsWindow()
  
        ### SETUP MAIN LAYOUT & WIDGET
        logger.debug("Setting up main layout and widget.")
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.sidebar)
        mainLayout.addWidget(self.beadworkView)

        mainWidget = QWidget()
        mainWidget.setObjectName("mainWidget")
        mainWidget.setLayout(mainLayout)

        ### MAIN WINDOW CONFIGS
        self.setStyleSheet(open(os.path.join(qss_dir, "style.qss")).read())
        self.setCentralWidget(mainWidget)
        self.setMinimumSize(1200, 600)   
        self.setWindowTitle('Beadwork Designer')

        logger.info("MainWindow initialized.")

    ########################################
    # SETUP METHODS
    ########################################

    def setupModels(self, height, width, modelData):
        logger.debug("Setting up BeadworkModel and BeadworkTransposeModel.")
        self.origModel = BeadworkModel(debug=self.debug, defaultHeight=height, defaultWidth=width, data=modelData)
        self.transposeModel = BeadworkTransposeModel()
        self.transposeModel.setSourceModel(self.origModel)

        self.model = self.origModel     # beginning model will be the original model

    def setupView(self, beadHeight, beadWidth):
        logger.debug("Setting up BeadworkView and BeadDelegate.")
        self.beadworkView = BeadworkView(beadHeight=beadHeight if self.currentOrientation == BeadworkOrientation.VERTICAL else beadWidth, 
                                         beadWidth=beadWidth if self.currentOrientation == BeadworkOrientation.VERTICAL else beadHeight)
        self.delegate = BeadDelegate(beadHeight=beadHeight if self.currentOrientation == BeadworkOrientation.VERTICAL else beadWidth, 
                                     beadWidth=beadWidth if self.currentOrientation == BeadworkOrientation.VERTICAL else beadHeight)
        self.beadworkView.setItemDelegate(self.delegate)
        self.beadworkView.setModel(self.model)
        self.beadworkView.clicked.connect(self.updateCurrentColorText)
        self.beadworkView.setObjectName("beadworkView")

    def setupOrientationWidget(self):
        logger.debug("Setting up orientationWidget.")
        self.orientationLabel = QLabel("Orientation:")
        self.orientationComboBox = QComboBox()
        self.orientationComboBox.addItems([v for k,v in self.orientationOptions.items()])
        self.orientationComboBox.setCurrentText(self.orientationOptions[self.currentOrientation])
        self.orientationComboBox.setEditable(False)
        self.orientationComboBox.currentTextChanged.connect(self.changeOrientation)
        orientationLayout = QHBoxLayout()
        orientationLayout.addWidget(self.orientationLabel)
        orientationLayout.addWidget(self.orientationComboBox)

        self.orientationWidget = QWidget()
        self.orientationWidget.setLayout(orientationLayout)

    def setupColorDialogWidget(self):
        logger.debug("Setting up colorDialogWidget.")
        colorDialogLayout = QHBoxLayout()
        self.currentColorLabel = QLabel('Current Color: #')
        self.currentColorLabel.setObjectName("currentColorLabel")
        self.currentColor = QLineEdit()
        self.currentColor.setFixedWidth(47)
        self.currentColor.setInputMask('HHHHHH')   # only allows hex color input
        self.currentColor.textChanged.connect(self.changeColor) 
        self.colorDialog = QColorDialog()
        self.colorDialog.colorSelected.connect(lambda c: self.currentColor.setText(c.name().upper()))
        self.colorDialogButton = QPushButton()
        self.colorDialogButton.setFixedWidth(20)
        self.colorDialogButton.setIcon(QIcon(os.path.join(icons_dir, "palette.png")))
        self.colorDialogButton.clicked.connect(self.colorDialog.open)
        colorDialogLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        colorDialogLayout.addWidget(self.currentColorLabel)
        colorDialogLayout.addWidget(self.currentColor)
        colorDialogLayout.addWidget(self.colorDialogButton)

        self.colorDialogWidget = QWidget()
        self.colorDialogWidget.setLayout(colorDialogLayout)

    def setupActions(self):
        logger.debug("Setting up actions.")

        ### TOOLBAR ACTIONS

        self.addColumnAction = QAction('Add Column', self)
        self.addColumnAction.triggered.connect(self.addColumn)
        self.addColumnAction.setIcon(QIcon(os.path.join(icons_dir, "table-insert-column.png")))

        self.removeColumnAction = QAction('Remove Column', self)
        self.removeColumnAction.triggered.connect(self.removeColumn)
        self.removeColumnAction.setIcon(QIcon(os.path.join(icons_dir, "table-delete-column.png")))

        self.addRowAction = QAction('Add Row', self)
        self.addRowAction.triggered.connect(self.addRow)
        self.addRowAction.setIcon(QIcon(os.path.join(icons_dir, "table-insert-row.png")))

        self.removeRowAction = QAction('Remove Row', self)
        self.removeRowAction.triggered.connect(self.removeRow)
        self.removeRowAction.setIcon(QIcon(os.path.join(icons_dir, "table-delete-row.png")))

        self.selectionMode = QAction('Selection Mode', self)
        self.selectionMode.setCheckable(True)
        self.selectionMode.triggered.connect(self.inSelectionMode)
        self.selectionMode.setIcon(QIcon(os.path.join(icons_dir, "selection.png")))

        self.colorMode = QAction('Color Mode', self)
        self.colorMode.setCheckable(True)
        self.colorMode.triggered.connect(self.inColorMode)
        self.colorMode.setIcon(QIcon(os.path.join(icons_dir, "color.png")))

        self.clearMode = QAction('Clear Mode', self)
        self.clearMode.setCheckable(True)
        self.clearMode.triggered.connect(self.inClearMode)
        self.clearMode.setIcon(QIcon(os.path.join(icons_dir, "eraser.png")))

        ### FILE MENU ACTIONS

        self.newAction = QAction('New', self)
        self.newAction.triggered.connect(self.loadNewProject)

        self.saveAction = QAction('Save', self)
        self.saveAction.triggered.connect(self.saveDialog)

        self.openAction = QAction('Open', self)
        self.openAction.triggered.connect(self.openDialog)

        ### EDIT MENU ACTIONS

        self.adjustDimensionsAction = QAction('Adjust Dimensions', self)
        self.adjustDimensionsAction.triggered.connect(lambda x: self.dimensionsWindow.show())

    def setupToolbar(self):
        logger.debug("Setting up self.toolbar.")
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbarOrientationAction = self.toolbar.addWidget(self.orientationWidget) # returns the action, not sure if I will ever need
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.addColumnAction)
        self.toolbar.addAction(self.addRowAction)
        self.toolbar.addAction(self.removeColumnAction)
        self.toolbar.addAction(self.removeRowAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.selectionMode)
        self.toolbar.addAction(self.colorMode)
        self.toolbar.addAction(self.clearMode)

    def setupColorList(self):
        logger.debug("Setting up colorList.")
        self.colorList = ColorList()
        self.proxyModel = BeadworkToColorListProxyModel()
        self.proxyModel.setSourceModel(self.model)
        self.model.dataChanged.connect(self.proxyModel.updateList)
        self.proxyModel.dataChanged.connect(self.colorList.dataChanged)
        self.beadworkView.clicked.connect(self.colorList.updateSelected) # update selected color in list when bead is selected
        self.colorList.setModel(self.proxyModel)

    def setupSidebar(self):
        logger.debug("Setting up sidebar.")
        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(self.colorDialogWidget)
        sidebarLayout.addWidget(QLabel('Colors in use:'))
        sidebarLayout.addWidget(self.colorList)
        self.sidebar = QWidget()
        self.sidebar.setLayout(sidebarLayout)
        self.sidebar.setMaximumWidth(200)

    def setupStatusBar(self):
        logger.debug("Setting up statusBar.")
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("QStatusBar {text-align: left;}")

        self.statusBarWidthLabel = QLabel(f"{self.modelWidth}")
        self.statusBarHeightLabel = QLabel(f"{self.modelHeight}")

        self.statusBarDimensionsLayout = QHBoxLayout()
        self.statusBarDimensionsLayout.addWidget(QLabel("Size:"))
        self.statusBarDimensionsLayout.addWidget(self.statusBarWidthLabel)
        self.statusBarDimensionsLayout.addWidget(QLabel("x"))
        self.statusBarDimensionsLayout.addWidget(self.statusBarHeightLabel)
        
        self.statusBarDimensionsWidget = QWidget()
        self.statusBarDimensionsWidget.setLayout(self.statusBarDimensionsLayout)

        self.statusBar.insertPermanentWidget(0, self.statusBarDimensionsWidget)

        self.setStatusBar(self.statusBar)

    def setupMenu(self):
        logger.debug("Setting up menus.")
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('File')
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAction)

        self.editMenu = self.menu.addMenu('Edit')
        self.editMenu.addAction(self.adjustDimensionsAction)

    def setupDimensionsWindow(self):
        logger.debug("Setting up dimensionsWindow.")
        self.dimensionsWindow = QWidget()
        self.dimensionsWindow.setWindowTitle("Adjust Dimensions")
        self.dimensionsWindow.setFixedSize(300, 200)
        self.dimensionsWindow.setWindowModality(Qt.ApplicationModal)
        self.dimensionsWindowLayout = QVBoxLayout()
        self.dimensionsWindow.setLayout(self.dimensionsWindowLayout)

        self.widthEdit = QLineEdit()
        self.widthEdit.setText(str(self.modelWidth))

        widthLine = QHBoxLayout()
        widthLine.addWidget(QLabel("Width:"))
        widthLine.addWidget(self.widthEdit)
        widthLineWidget = QWidget()
        widthLineWidget.setLayout(widthLine)

        self.heightEdit = QLineEdit()
        self.heightEdit.setText(str(self.modelHeight))

        heightLine = QHBoxLayout()
        heightLine.addWidget(QLabel("Height:"))
        heightLine.addWidget(self.heightEdit)
        heightLineWidget = QWidget()
        heightLineWidget.setLayout(heightLine)

        self.changeDimensionsButton = QPushButton("Change")
        self.changeDimensionsButton.clicked.connect(self.adjustDimensions)

        self.dimensionsWindowLayout.addWidget(widthLineWidget)
        self.dimensionsWindowLayout.addWidget(heightLineWidget)
        self.dimensionsWindowLayout.addWidget(self.changeDimensionsButton)

    # Override this function so that it repaints the beadworkView.
    # This is currently the workaround as I cannot figure out how to
    # get the rows and columns to size properly without explicitly
    # calling repaint()
    def show(self):
        super().show()
        self.beadworkView.repaint()

    ########################################
    # SLOTS
    ########################################
        
    def updateCurrentColorText(self, index):
        logger.debug(f"Updating current color text for index {index}.")
        self.currentColor.setText((self.model.data(index, Qt.ItemDataRole.DisplayRole)).upper())

    def addColumn(self):
        logger.debug("Adding column.")
        self.beadworkView.setCurrentIndex(self.model.index(0, self.modelWidth - 1)) # TODO: allow for selecting index
        self.model.insertColumn(self.model.columnCount(QModelIndex()), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.updateWidthXHeight()

    def removeColumn(self):
        logger.debug("Removing column.")
        self.beadworkView.setCurrentIndex(self.model.index(0, self.modelWidth - 1)) # TODO: allow for selecting index
        self.model.removeColumn(self.model.columnCount(QModelIndex()) - 1, self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.updateWidthXHeight()

    def addRow(self):
        logger.debug("Adding row.")
        self.beadworkView.setCurrentIndex(self.model.index(self.modelHeight-1, 0)) # TODO: allow for selecting index
        self.model.insertRow(self.model.rowCount(QModelIndex()), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.updateWidthXHeight()

    def removeRow(self):
        logger.debug("Removing row.")
        self.beadworkView.setCurrentIndex(self.model.index(self.modelHeight-1, 0)) # TODO: allow for selecting index
        self.model.removeRow(self.model.rowCount(QModelIndex()) - 1, self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.updateWidthXHeight()

    def changeWidthTo(self, value):
        logger.debug(f"Width changing to {value}.")
        self.beadworkView.setCurrentIndex(self.model.index(0, self.modelWidth-1))
        if value > self.modelWidth:
            self.model.insertColumns(self.model.columnCount(QModelIndex()), value - self.modelWidth, self.beadworkView.currentIndex())
        else:
            self.model.removeColumns(self.model.columnCount(QModelIndex())-1, self.modelWidth - value, self.beadworkView.currentIndex())  

    def changeHeightTo(self, value):
        logger.debug(f"Height changing to {value}.")
        self.beadworkView.setCurrentIndex(self.model.index(self.modelHeight-1, 0))
        if value > self.modelHeight:
            self.model.insertRows(self.model.rowCount(QModelIndex()), value - self.modelHeight, self.beadworkView.currentIndex())
        else:
            self.model.removeRows(self.model.rowCount(QModelIndex())-1, self.modelHeight - value, self.beadworkView.currentIndex())  

    # TODO: unit tests
    def adjustDimensions(self):
        self.dimensionsWindow.close()

        newWidth = int(self.widthEdit.text())
        newHeight = int(self.heightEdit.text())
        logger.debug(f"Adjusting dimensions to {newWidth}, {newHeight}.")

        if newWidth != self.modelWidth:
            self.changeWidthTo(newWidth)

        if newHeight != self.modelHeight:
            self.changeHeightTo(newHeight)

        self.updateWidthXHeight()

        logger.info(f"New width: {newWidth}, New height: {newHeight}.")

    # TODO: this currently only changes the last one selected, multiple selections do not work
    def changeColor(self, colorString):
        self.model.setData(self.beadworkView.currentIndex(), f"#{colorString}", Qt.ItemDataRole.EditRole)
        
    # TODO: implement
    # NOTES:
        # selectionMode is default
        # in this mode, the user can select beads by clicking on them
        # the user can also select multiple beads by clicking and dragging
        # the currentColor dialog populates with the color of the selected bead(s)
        # if checked, should disconnect the relevant methods from the other modes
    def inSelectionMode(self, checked):
        if checked:
            self.colorMode.setChecked(False)
            self.clearMode.setChecked(False)
        else:
            self.selectionMode.setChecked(True)

        # TODO: research these selection methods
            # self.beadworkView.setSelectionMode(QListView.SelectionMode.MultiSelection)
        #else:
            # self.beadworkView.setSelectionMode(QListView.SelectionMode.SingleSelection)

    # TODO: implement
    # NOTES:
        # colorMode allows the user to change the color of multiple beads at once
        # every bead the user clicks on will change to the color in the currentColor dialog
        # if checked, should disconnect the relevant methods from the other modes
        # and enable the currentColor dialog to change the color of the "painter"
    def inColorMode(self, checked):
        if checked:
            self.selectionMode.setChecked(False)
            self.clearMode.setChecked(False)
        else:
            self.selectionMode.setChecked(True)

    # TODO: implement
    # NOTES:
        # clearMode allows the user to clear the color of multiple beads at once
        # every bead clicked/selected will change to white/transparent
        # if selecting multiple beads, hint to the user that they will all clear when finished selecting
        # if checked, should disconnect the relevant methods from the other modes
    def inClearMode(self, checked):
        if checked:
            self.selectionMode.setChecked(False)
            self.colorMode.setChecked(False)
        else:
            self.selectionMode.setChecked(True)

    def changeOrientation(self, spinboxValue): # does not use spinboxValue yet, may implement later if there are more orientation options
        logger.debug(f"Changing orientation to {self.orientationOptions[self.currentOrientation]}.")

        self.currentOrientation = BeadworkOrientation.VERTICAL if self.currentOrientation == BeadworkOrientation.HORIZONTAL else BeadworkOrientation.HORIZONTAL

        # swap models
        if self.model == self.origModel:
            self.model = self.transposeModel
        else:
            self.model = self.origModel
        self.beadworkView.setModel(self.model)
        self.proxyModel.setSourceModel(self.model)

        # change internal orientations of delegate and view
        self.delegate.changeOrientation()
        self.beadworkView.changeOrientation()
        logger.debug(f"self.beadworkView.model() changed to {self.model}.")

        self.updateWidthXHeight()

        # TODO: switch addRow/addColumn actions to fit with the new orientation

        logger.info(f"Orientation changed to {self.orientationOptions[self.currentOrientation]}.")

    # TODO: currently shows the default_project.json filename -- refactor this to just pull 
        # default config and a blank project data before implementing a single "SAVE" action
        # without a file dialog
    def loadNewProject(self):
        logger.info("Loading new project")
        self.importProject(bin_dir + "/default_project.json")

    def saveDialog(self):
        logger.info("Saving project.")
        filename = QFileDialog.getSaveFileName(self, 'Save Project', os.path.expanduser("~"), 'Beadwork Designer Project (*.json)')[0]
        logger.debug(f"Selected filename: {filename}.")
        if filename:
            self.exportProject(filename)
        # TODO: update status bar with save status
            
    def openDialog(self):
        logger.info("Opening project.")
        filename = QFileDialog.getOpenFileName(self, 'Open Project', os.path.expanduser("~"), 'Beadwork Designer Project (*.json)')[0]
        logger.debug(f"Selected filename: {filename}.")
        if filename:
            self.importProject(filename)

    ########################################
    # UTILITY METHODS
    ########################################

    def updateWidthXHeight(self):
        # get up to date model dimensions
        self.modelWidth = self.model.columnCount(None)
        self.modelHeight = self.model.rowCount(None)

        self.statusBarWidthLabel.setText(f"{self.modelWidth}")
        self.statusBarHeightLabel.setText(f"{self.modelHeight}")

        self.widthEdit.setText(str(self.modelWidth))
        self.heightEdit.setText(str(self.modelHeight))
        
    def exportProject(self, filename):
        self.setWindowTitle(f'Beadwork Designer - {filename}')

        # these ifs are necessary as a horizontal model is only changing the orientation,
        # not the underlying structure
        self.configs["width"] = self.modelWidth if self.currentOrientation == BeadworkOrientation.VERTICAL else self.modelHeight    
        self.configs["height"] = self.modelHeight if self.currentOrientation == BeadworkOrientation.VERTICAL else self.modelWidth

        self.configs["defaultOrientation"] = self.orientationOptions[self.currentOrientation]

        project = {
            "info": {
                        "version": 0.1 # TODO: version checking?
                    },
            "configs": self.configs,    # TODO: do I pull current configs from variables or reassign directly to configs?
            "project": self.origModel.exportData()
        }
        utils.saveProject(project, filename)

    # TODO: this is a bit of a mess, but it works for now
    # TODO: handle failure to load project
    def importProject(self, filename):
        self.setWindowTitle(f'Beadwork Designer - {filename}')

        json = utils.loadProject(filename)
        for key in json['configs'].keys():
            self.configs[key] = json['configs'][key]           # replace any config with the loaded one
        
        self.currentOrientation = BeadworkOrientation.VERTICAL     # if this does not match the config, it will be changed in the if statement

        ### LOAD DATA
        self.origModel.importData(json['project'], debug=self.configs['debug'])

        ### UPDATE ELEMENTS & CHANGE ORIENTATION IF NECESSARY
        if json['configs']["defaultOrientation"] == "Horizontal":
            self.changeOrientation("Horizontal")

            self.orientationComboBox.currentTextChanged.disconnect(self.changeOrientation)  # temporarily disconnect signal  
            self.orientationComboBox.setCurrentText("Horizontal")                           # to avoid switching back to Vertical on this set
            self.orientationComboBox.currentTextChanged.connect(self.changeOrientation)     # reconnect signal
        else:
            self.updateWidthXHeight()