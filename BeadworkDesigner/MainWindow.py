"""
Icons are provided by https://p.yusukekamiyamane.com/. They are licensed under a Creative Commons Attribution 3.0 License.
"""

#####################
# TODO: make a Goals/Ideas/Features file
#
# TODO: add Save As file menu action
# TODO: add "New Project" option to menu
#       - have loadNewProject - needs to import default config and create blank project, not load default
#       - OR: load default_project.json, but not allow Save, only Save As (determine via non-existent title field?)
# TODO: change from RGB hex to HSV
# TODO: add hints
# TODO: Settings menu
#       TODO: font options
#       TODO: add a way to change the size of the beads
# TODO: add a way to zoom in and out (just change bead size?)
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
    """The application Main Window. This handles the main GUI elements and interactions."""

    def __init__(self, debug=False, app_configs=None, project_configs=None, modelData=None):
        """Initialize the MainWindow, all GUI elements, and the BeadworkModel.

        Args:
            debug (bool, optional): Enable debug mode. Defaults to False.
            app_configs (dict, optional): Application configurations. Defaults to None.
            project_configs (dict, optional): Project configurations. Defaults to None.
            modelData (list, optional): Initial model data. Defaults to None. If set, will import into a BeadworkModel.
        """

        super().__init__()

        self.debug = debug
        self.app_configs = app_configs
        self.project_configs = project_configs

        # set initial orientation dict as we need nice string representations
        # TODO: is this needed if I replace the width x label spinbox?
        # TODO: or do I replace Enum with a StrEnum which has a nice string representation? https://docs.python.org/3/library/enum.html#enum.StrEnum
        self.orientationOptions = {BeadworkOrientation.HORIZONTAL: "Horizontal", BeadworkOrientation.VERTICAL: "Vertical"}
        
        logger.info("Initializing MainWindow.")

        ### TRACK INITIAL ORIENTATION
        if self.retrieveConfig("defaultOrientation") == "Horizontal":
            self.currentOrientation = BeadworkOrientation.HORIZONTAL
        else:
            self.currentOrientation = BeadworkOrientation.VERTICAL
        
        ### SETUP MODELS & VIEW
        self.setupModels(self.retrieveConfig("height"), self.retrieveConfig("width"), modelData)
        self.setupView(self.retrieveConfig("beadHeight"), self.retrieveConfig("beadWidth"))

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
        """Sets up the BeadworkModel and BeadworkTransposeModel.

        Args:
            height (int): The height (rows) of the model.
            width (int): The width (columns) of the model. 
            modelData (list): The initial data for the model as a 2D list of hex colors.
        """
        logger.debug("Setting up BeadworkModel and BeadworkTransposeModel.")
        self.origModel = BeadworkModel(debug=self.debug, defaultHeight=height, defaultWidth=width, data=modelData)
        self.transposeModel = BeadworkTransposeModel()
        self.transposeModel.setSourceModel(self.origModel)

        self.model = self.origModel     # beginning model will be the original model

    def setupView(self, beadHeight, beadWidth):
        """Sets up the BeadworkView and BeadDelegate.

        Args:
            beadHeight (int): The height of the beads (in pixels) to draw in the view.
            beadWidth (int): The width of the beads (in pixels) to draw in the view.
        """
        logger.debug("Setting up BeadworkView and BeadDelegate.")
        self.beadworkView = BeadworkView(beadHeight=beadHeight if self.currentOrientation == BeadworkOrientation.VERTICAL else beadWidth, 
                                         beadWidth=beadWidth if self.currentOrientation == BeadworkOrientation.VERTICAL else beadHeight)
        self.delegate = BeadDelegate(beadHeight=beadHeight if self.currentOrientation == BeadworkOrientation.VERTICAL else beadWidth, 
                                     beadWidth=beadWidth if self.currentOrientation == BeadworkOrientation.VERTICAL else beadHeight)
        self.beadworkView.setItemDelegate(self.delegate)
        self.beadworkView.setModel(self.model)
        self.beadworkView.clicked.connect(self.handleViewClicked)
        self.beadworkView.setObjectName("beadworkView")

    def setupOrientationWidget(self):
        """Sets up the orientationWidget to allow the user to change the orientation of the beadwork."""
        logger.debug("Setting up orientationWidget.")
        self.orientationLabel = QLabel("Orientation:")
        self.orientationComboBox = QComboBox()
        self.orientationComboBox.addItems([v for k,v in self.orientationOptions.items()])
        self.orientationComboBox.setCurrentText(self.orientationOptions[self.currentOrientation])
        self.orientationComboBox.setEditable(False)
        self.orientationComboBox.setToolTip("Change the orientation of the beadwork.")
        self.orientationComboBox.currentTextChanged.connect(self.changeOrientation)
        orientationLayout = QHBoxLayout()
        orientationLayout.addWidget(self.orientationLabel)
        orientationLayout.addWidget(self.orientationComboBox)

        self.orientationWidget = QWidget()
        self.orientationWidget.setLayout(orientationLayout)

    def setupColorDialogWidget(self):
        """Sets up the colorDialogWidget to allow the user to change the color of the beads."""
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
        self.colorDialogButton.setToolTip("Open color dialog to select a color.")
        colorDialogLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        colorDialogLayout.addWidget(self.currentColorLabel)
        colorDialogLayout.addWidget(self.currentColor)
        colorDialogLayout.addWidget(self.colorDialogButton)

        self.colorDialogWidget = QWidget()
        self.colorDialogWidget.setLayout(colorDialogLayout)

    def setupActions(self):
        """Sets up the actions for the toolbar and menus."""
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
        self.selectionMode.setChecked(True) # default mode

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
        """Sets up the toolbar with the orientationWidget and the actions."""
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
        """Sets up the ColorList view and the BeadworkToColorListProxyModel."""
        logger.debug("Setting up colorList.")
        self.colorList = ColorList()
        self.proxyModel = BeadworkToColorListProxyModel()
        self.proxyModel.setSourceModel(self.model)
        self.model.dataChanged.connect(self.proxyModel.updateList)
        self.proxyModel.dataChanged.connect(self.colorList.dataChanged)
        self.beadworkView.clicked.connect(self.colorList.updateSelected) # update selected color in list when bead is selected
        self.colorList.setModel(self.proxyModel)

    def setupSidebar(self):
        """Sets up the sidebar with the colorDialogWidget and the colorList."""
        logger.debug("Setting up sidebar.")
        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(self.colorDialogWidget)
        sidebarLayout.addWidget(QLabel('Colors in use:'))
        sidebarLayout.addWidget(self.colorList)
        self.sidebar = QWidget()
        self.sidebar.setLayout(sidebarLayout)
        self.sidebar.setMaximumWidth(200)

    def setupStatusBar(self):
        """Sets up the statusBar with a generic text label and the beadwork 
        project's dimensions."""
        logger.debug("Setting up statusBar.")
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("QStatusBar {text-align: left;}")

        self.statusBarTextLabel = QLabel("")

        self.statusBarWidthLabel = QLabel(f"{self.modelWidth}")
        self.statusBarHeightLabel = QLabel(f"{self.modelHeight}")

        self.statusBarDimensionsLayout = QHBoxLayout()
        self.statusBarDimensionsLayout.addWidget(self.statusBarTextLabel)
        self.statusBarDimensionsLayout.addWidget(QLabel("Size:"))
        self.statusBarDimensionsLayout.addWidget(self.statusBarWidthLabel)
        self.statusBarDimensionsLayout.addWidget(QLabel("x"))
        self.statusBarDimensionsLayout.addWidget(self.statusBarHeightLabel)
        
        self.statusBarDimensionsWidget = QWidget()
        self.statusBarDimensionsWidget.setLayout(self.statusBarDimensionsLayout)

        self.statusBar.insertPermanentWidget(0, self.statusBarDimensionsWidget)

        self.setStatusBar(self.statusBar)

    def setupMenu(self):
        """Sets up all menus: file, edit, etc."""
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
        """Sets up the dimensionsWindow to allow the user to adjust the 
        dimensions of the beadwork more than one row or column at a time."""
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

    # This is currently the workaround as I cannot figure out how to
    # get the rows and columns to size properly without explicitly
    # calling repaint()
    def show(self):
        """Overrides the show method to guarantee repainting the beadworkView."""
        super().show()
        self.beadworkView.repaint()

    ########################################
    # SLOTS
    ########################################
        
    def updateCurrentColorText(self, index):
        """Updates the current color text in the colorDialogWidget if the user
        is in Selection Mode.

        Args:
            index (QIndex): the location of the selected bead.
        """
        logger.debug(f"Updating current color text for index {index}.")
        self.currentColor.setText((self.model.data(index, Qt.ItemDataRole.DisplayRole)).upper())

    def handleViewClicked(self, index):
        """Handles different behavior types for clicking on the BeadworkView
        depending on the mode selected:
            Selection Mode: updates the current color text.
            Color Mode: changes the color of the bead selected.
            Clear Mode: clears the color of the bead selected.

        Args:
            index (QIndex): the location of the selected bead.
        """
        logger.debug(f"View clicked at index {index}.")
        if self.selectionMode.isChecked():      # if in selection mode, update the current color text
            self.updateCurrentColorText(index) 
        elif self.colorMode.isChecked():        # if in color mode, change the color of the bead selected
            # TODO: currently, does set the color of the bead, but does not account for multiple selections
            self.model.setData(index, f"#{self.currentColor.text()}", Qt.ItemDataRole.EditRole)
        elif self.clearMode.isChecked():        # if in clear mode, clear the color of the bead selected
            # TODO: currently, does clear the color of the bead, but does not account for multiple selections
            self.model.setData(index, "#FFFFFF", Qt.ItemDataRole.EditRole)

    def addColumn(self):
        """Adds a single column to the original beadwork model."""
        logger.debug("Adding column.")
        self.beadworkView.setCurrentIndex(self.model.index(0, self.modelWidth - 1)) # TODO: allow for selecting index
        self.model.insertColumn(self.model.columnCount(QModelIndex()), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.updateWidthXHeight()

    def removeColumn(self):
        """Removes a single column from the original beadwork model."""
        logger.debug("Removing column.")
        self.beadworkView.setCurrentIndex(self.model.index(0, self.modelWidth - 1)) # TODO: allow for selecting index
        self.model.removeColumn(self.model.columnCount(QModelIndex()) - 1, self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.updateWidthXHeight()

    def addRow(self):
        """Adds a single row to the original beadwork model."""
        logger.debug("Adding row.")
        self.beadworkView.setCurrentIndex(self.model.index(self.modelHeight-1, 0)) # TODO: allow for selecting index
        self.model.insertRow(self.model.rowCount(QModelIndex()), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.updateWidthXHeight()

    def removeRow(self):
        """Removes a single row from the original beadwork model."""
        logger.debug("Removing row.")
        self.beadworkView.setCurrentIndex(self.model.index(self.modelHeight-1, 0)) # TODO: allow for selecting index
        self.model.removeRow(self.model.rowCount(QModelIndex()) - 1, self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.updateWidthXHeight()

    def changeWidthTo(self, value):
        """Changes the width (columns) of the beadwork model to the specified value.
        
        Args:
            value (int): The new width of the beadwork model.
        """
        logger.debug(f"Width changing to {value}.")
        self.beadworkView.setCurrentIndex(self.model.index(0, self.modelWidth-1))
        if value > self.modelWidth:
            self.model.insertColumns(self.model.columnCount(QModelIndex()), value - self.modelWidth, self.beadworkView.currentIndex())
        else:
            self.model.removeColumns(self.model.columnCount(QModelIndex())-1, self.modelWidth - value, self.beadworkView.currentIndex())  

    def changeHeightTo(self, value):
        """Changes the height (rows) of the beadwork model to the specified value.

        Args:
            value (int): The new height of the beadwork model.
        """
        logger.debug(f"Height changing to {value}.")
        self.beadworkView.setCurrentIndex(self.model.index(self.modelHeight-1, 0))
        if value > self.modelHeight:
            self.model.insertRows(self.model.rowCount(QModelIndex()), value - self.modelHeight, self.beadworkView.currentIndex())
        else:
            self.model.removeRows(self.model.rowCount(QModelIndex())-1, self.modelHeight - value, self.beadworkView.currentIndex())  

    def adjustDimensions(self):
        """Adjusts the dimensions of the beadwork model to the specified width 
        and height. Called from and retrieves values from the dimensionsWindow."""
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

    def changeColor(self, colorString):
        """Changes the color of a selected bead when the colorDialog is updated.

        Args:
            colorString (str): hex value of color.
        """
        if self.selectionMode.isChecked():
            self.model.setData(self.beadworkView.currentIndex(), f"#{colorString}", Qt.ItemDataRole.EditRole)
        
    # NOTES:
        # selectionMode is default
        # in this mode, the user can select beads by clicking on them
        # the user can also select multiple beads by clicking and dragging
        # the currentColor dialog populates with the color of the selected bead(s)
        # if checked, should disconnect the relevant methods from the other modes
    def inSelectionMode(self, checked):
        """Changes the mode to Selection Mode. Slot for the triggered selectionMode action.

        Args:
            checked (bool): flag for if the selectionMode action/button is checked.
        """
        if checked:
            self.colorMode.setChecked(False)
            self.clearMode.setChecked(False)
        else:   # if not checked but clicked, revert back to checked
            self.selectionMode.setChecked(True)

        self.writeToStatusBar("Selection Mode")

        logger.debug("Entered selection mode.")

        # TODO: research these selection methods
            # self.beadworkView.setSelectionMode(QListView.SelectionMode.MultiSelection)
        #else:
            # self.beadworkView.setSelectionMode(QListView.SelectionMode.SingleSelection)

    # NOTES:
        # colorMode allows the user to change the color of multiple beads at once
        # every bead the user clicks on will change to the color in the currentColor dialog
        # if checked, should disconnect the relevant methods from the other modes
        # and enable the currentColor dialog to change the color of the "painter"
    def inColorMode(self, checked):
        """Changes the mode to Color Mode. Slot for the triggered colorMode action.

        Args:
            checked (bool): flag for if the colorMode action/button is checked.
        """
        if checked:
            self.selectionMode.setChecked(False)
            self.clearMode.setChecked(False)
        else:   # if not checked but clicked, revert back to checked
            self.colorMode.setChecked(True)

        self.writeToStatusBar("Color Mode")

        logger.debug("Entered color mode.")

    # NOTES:
        # clearMode allows the user to clear the color of multiple beads at once
        # every bead clicked/selected will change to white/transparent
        # if selecting multiple beads, hint to the user that they will all clear when finished selecting
        # if checked, should disconnect the relevant methods from the other modes
    def inClearMode(self, checked):
        """Changes the mode to Clear Mode. Slot for the triggered clearMode action.

        Args:
            checked (bool): flag for if the clearMode action/button is checked.
        """
        if checked:
            self.selectionMode.setChecked(False)
            self.colorMode.setChecked(False)
        else:   # if not checked but clicked, revert back to checked
            self.clearMode.setChecked(True)

        self.writeToStatusBar("Clear Mode")

        self.currentColor.setText("")   # clear the current color dialog

        logger.debug("Entered clear mode.")

    def changeOrientation(self, spinboxValue): # does not use spinboxValue yet, may implement later if there are more orientation options
        """Changes the orientation of the beadwork from horizontal to vertical or vice versa.

        Args:
            spinboxValue (str): the value of the spinbox when changed.
        """
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

        logger.info(f"Orientation changed to {self.orientationOptions[self.currentOrientation]}.")

    # TODO: currently shows the default_project.json filename -- refactor this to just pull 
        # default config and a blank project data before implementing a single "SAVE" action
        # without a file dialog
    def loadNewProject(self):
        """Loads a new project, replacing the current project with a blank one."""
        logger.info("Loading new project")
        self.importProject(bin_dir + "/default_project.json")

    def saveDialog(self):
        """Opens a file dialog to save the project to a JSON file."""
        logger.info("Saving project.")
        filename = QFileDialog.getSaveFileName(self, 'Save Project', os.path.expanduser("~"), 'Beadwork Designer Project (*.json)')[0]
        logger.debug(f"Selected filename: {filename}.")
        if filename:
            try:
                self.exportProject(filename)
                self.writeToStatusBar("Saved")
            except Exception as e:
                logger.error(f"Failed to save project to {filename}: {e}.")
                self.writeToStatusBar("Failed to save project.")
            
    def openDialog(self):
        """Opens a file dialog to open a project from a JSON file."""
        logger.info("Opening project.")
        filename = QFileDialog.getOpenFileName(self, 'Open Project', os.path.expanduser("~"), 'Beadwork Designer Project (*.json)')[0]
        logger.debug(f"Selected filename: {filename}.")
        if filename:
            self.importProject(filename)

    ########################################
    # UTILITY METHODS
    ########################################

    # TODO: clear the status bar message after a certain time?
    def writeToStatusBar(self, text):
        """Writes a message to the status bar.

        Args:
            text (str): The message to write to the status bar.
        """
        delimiter = " 🞄"
        self.statusBarTextLabel.setText(text + delimiter)

    def updateWidthXHeight(self):
        """Updates the width and height of the beadwork model to all needed areas."""
        # get up to date model dimensions
        self.modelWidth = self.model.columnCount(None)
        self.modelHeight = self.model.rowCount(None)

        self.statusBarWidthLabel.setText(f"{self.modelWidth}")
        self.statusBarHeightLabel.setText(f"{self.modelHeight}")

        self.widthEdit.setText(str(self.modelWidth))
        self.heightEdit.setText(str(self.modelHeight))
        
    def exportProject(self, filename):
        """Exports the project to a JSON file.

        Args:
            filename (str): The filename to save the project to.
        """
        self.setWindowTitle(f'Beadwork Designer - {filename}')

        # these ifs are necessary as a horizontal model is only changing the orientation,
        # not the underlying structure
        self.project_configs["width"] = self.modelWidth if self.currentOrientation == BeadworkOrientation.VERTICAL else self.modelHeight    
        self.project_configs["height"] = self.modelHeight if self.currentOrientation == BeadworkOrientation.VERTICAL else self.modelWidth

        self.project_configs["defaultOrientation"] = self.orientationOptions[self.currentOrientation]

        project = {
            "info": {
                        "version": 0.1 # TODO: version checking?
                    },
            "configs": self.project_configs,    # TODO: do I pull current configs from variables or reassign directly to configs?
            "project": self.origModel.exportData()
        }
        utils.saveProject(project, filename)

    # TODO: this is a bit of a mess, but it works for now
    # TODO: handle failure to load project
    def importProject(self, filename):
        """Imports a project from a JSON file.

        Args:
            filename (str): The filename to load the project from.
        """
        self.setWindowTitle(f'Beadwork Designer - {filename}')

        json = utils.loadProject(filename)
        for key in json['configs'].keys():
            self.project_configs[key] = json['configs'][key]           # replace any config with the loaded one
        
        self.currentOrientation = BeadworkOrientation.VERTICAL     # if this does not match the config, it will be changed in the if statement

        ### LOAD DATA
        self.origModel.importData(json['project'], debug=self.retrieveConfig('debug'))

        ### UPDATE ELEMENTS & CHANGE ORIENTATION IF NECESSARY
        if json['configs']["defaultOrientation"] == "Horizontal":
            self.changeOrientation("Horizontal")

            self.orientationComboBox.currentTextChanged.disconnect(self.changeOrientation)  # temporarily disconnect signal  
            self.orientationComboBox.setCurrentText("Horizontal")                           # to avoid switching back to Vertical on this set
            self.orientationComboBox.currentTextChanged.connect(self.changeOrientation)     # reconnect signal
        else:
            self.updateWidthXHeight()

    # retrieveConfig method: and if no config is available, log it to prevent errors (and use default config instead)
    # NOTE: this still fails with a KeyError if the key is not in any config
    def retrieveConfig(self, key, config=None):
        """Retrieves a configuration value from the project or app configs.

        Args:
            key (str): The key to retrieve from the configs.
            config (dict, optional): The config to retrieve from. Defaults to None.
        """
        if config and config is self.project_configs:
            value = self.project_configs[key]
        elif config and config is self.app_configs:
            value = self.app_configs[key]
        else:
            try:
                if key in self.project_configs:
                    value = self.project_configs[key]
                else:
                    value = self.app_configs[key]
            except (TypeError, KeyError) as e:
                logger.error(f"Config {key} not found, returning default. Message: {e}.")
                import bin.default_config as default_config
                try:
                    value = default_config.project_configs[key]
                except KeyError:
                    value = default_config.app_configs[key]
                finally:
                    del default_config  # clean up
        
        logger.debug(f"Returning {value} for {key}.")
        return value