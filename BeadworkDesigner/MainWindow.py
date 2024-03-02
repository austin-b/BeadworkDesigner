"""
Icons are provided by https://p.yusukekamiyamane.com/. They are licensed under a Creative Commons Attribution 3.0 License.
"""

#####################
#
# TODO: setup types
# TODO: add docstrings
# TODO: create a central location for beadWidth and beadHeight values
# TODO: add save and load options to file menu
# TODO: add a way to change the size of the beads
# TODO: add a way to zoom in and out
# TODO: add a way to change the color of the background
# TODO: add a "bucket fill" option/tool
# TODO: implement undo and redo functionality
# TODO: implement a copy and paste functionality for selected beads
# TODO: add a way to align beads horizontally and vertically
# TODO: implement a way to group and ungroup beads for easier manipulation
# TODO: Add a way to add text labels or annotations to the beadwork design
# TODO: add a way to print or export to PDF
#
#####################

import logging
import os

from PySide6.QtCore import QModelIndex, Qt, QTransposeProxyModel
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QSpinBox,
    QToolBar,
    QWidget,
    QVBoxLayout
)

from BeadworkDesigner.BeadworkModel import BeadworkModel, BeadworkTransposeModel
from BeadworkDesigner.BeadDelegate import BeadDelegate
from BeadworkDesigner.BeadworkView import BeadworkView
from BeadworkDesigner.ColorList import BeadworkToColorListProxyModel, ColorList

logger = logging.getLogger(__name__)

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
bin_dir = os.path.join(base_dir, "bin")
icons_dir = os.path.join(bin_dir, "icons")
qss_dir = os.path.join(bin_dir, "qss")

class MainWindow(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()

        self.debug = debug

        logger.info("Initializing MainWindow.")

        ### SETUP MODELS AND CONFIGURE VIEW
        self.setupModels()
        self.setupView()

        ### KEEP TRACK OF INITIAL WIDTH x HEIGHT
        self.modelWidth = self.model.columnCount(QModelIndex())
        self.modelHeight = self.model.rowCount(QModelIndex())
        logger.debug(f"Model width: {self.modelWidth}, Model height: {self.modelHeight}.")

        ### SETUP OTHER GUI ELEMENTS
        self.setupMenu()
        self.setupWidthXHeightWidget()
        self.setupOrientationWidget()
        self.setupColorDialogWidget()
        self.setupColorList()
        self.setupSidebar()
        self.setupActions()
        self.setupToolbar()    

        ### SETUP MAIN LAYOUT & WIDGET
        logger.debug("Setting up main layout and widget.")
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.sidebar)
        mainLayout.addWidget(self.beadworkView)

        mainWidget = QWidget()
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

    def setupMenu(self):
        logger.debug("Setting up menus.")
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('File')

    def setupModels(self):
        logger.debug("Setting up BeadworkModel and BeadworkTransposeModel.")
        self.origModel = BeadworkModel(debug=self.debug)
        self.transposeModel = BeadworkTransposeModel()
        self.transposeModel.setSourceModel(self.origModel)

        self.model = self.origModel     # beginning model will be the original model

    def setupView(self):
        logger.debug("Setting up BeadworkView and BeadDelegate.")
        self.beadworkView = BeadworkView()
        self.delegate = BeadDelegate()
        self.beadworkView.setItemDelegate(self.delegate)
        self.beadworkView.setModel(self.model)
        self.beadworkView.clicked.connect(self.updateCurrentColorText)
        self.beadworkView.setObjectName("beadworkView")

    def setupWidthXHeightWidget(self):
        logger.debug("Setting up widthXHeightWidget.")
        self.widthLabel = QLabel("Width:")
        self.widthSpinBox = QSpinBox()
        self.widthSpinBox.setValue(self.modelWidth)
        self.widthSpinBox.valueChanged.connect(self.widthChanged) # TODO: does not support direct input values, only using the up and down arrows
        self.heightLabel = QLabel("Height:")
        self.heightSpinBox = QSpinBox()
        self.heightSpinBox.setValue(self.modelHeight)
        self.heightSpinBox.valueChanged.connect(self.heightChanged) # TODO: does not support direct input values, only using the up and down arrows
        widthXHeightLayout = QHBoxLayout()
        widthXHeightLayout.addWidget(self.widthLabel)
        widthXHeightLayout.addWidget(self.widthSpinBox)
        widthXHeightLayout.addWidget(self.heightLabel)
        widthXHeightLayout.addWidget(self.heightSpinBox)

        self.widthXHeightWidget = QWidget()
        self.widthXHeightWidget.setLayout(widthXHeightLayout)

    def setupOrientationWidget(self):
        logger.debug("Setting up orientationWidget.")
        self.orientationOptions = ["Vertical", "Horizontal"]
        self.currentOrientation = "Vertical" # TODO: make this default changeable via settings (don't forget to change the unit test)
        self.orientationLabel = QLabel("Orientation:")
        self.orientationComboBox = QComboBox()
        self.orientationComboBox.addItems(self.orientationOptions)
        self.orientationComboBox.setCurrentText(self.currentOrientation)
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
        self.currentColor.textChanged.connect(lambda c: self.model.setData(self.beadworkView.currentIndex(), f"#{c}", Qt.ItemDataRole.EditRole)) # TODO: this currently only changes the last one selected, multiple selections do not work
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
        # TODO: fix & add to tests
        logger.debug("Setting up actions.")
        self.addColumnAction = QAction('Add Column', self)
        self.addColumnAction.triggered.connect(self.addColumn)
        self.addColumnAction.setIcon(QIcon(os.path.join(icons_dir, "table-insert-column.png")))

        # TODO: fix & add to tests
        self.removeColumnAction = QAction('Remove Column', self)
        self.removeColumnAction.triggered.connect(self.removeColumn)
        self.removeColumnAction.setIcon(QIcon(os.path.join(icons_dir, "table-delete-column.png")))

        # TODO: fix & add to tests
        self.addRowAction = QAction('Add Row', self)
        self.addRowAction.triggered.connect(self.addRow)
        self.addRowAction.setIcon(QIcon(os.path.join(icons_dir, "table-insert-row.png")))

        # TODO: fix & add to tests
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

    def setupToolbar(self):
        logger.debug("Setting up self.toolbar.")
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.addColumnAction)
        self.toolbar.addAction(self.addRowAction)
        self.toolbar.addAction(self.removeColumnAction)
        self.toolbar.addAction(self.removeRowAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.selectionMode)
        self.toolbar.addAction(self.colorMode)
        self.toolbar.addAction(self.clearMode)

    # TODO: finish implementing 
    def setupColorList(self):
        logger.debug("Setting up colorList.")
        self.colorList = ColorList()
        # TODO: proxyModel does not work -- fix
        # self.proxyModel = BeadworkToColorListProxyModel()
        # self.proxyModel.setSourceModel(self.model)
        self.colorList.setModel(self.model)

    def setupSidebar(self):
        logger.debug("Setting up sidebar.")
        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(self.widthXHeightWidget)
        sidebarLayout.addWidget(self.orientationWidget)
        sidebarLayout.addWidget(self.colorDialogWidget)
        sidebarLayout.addWidget(QLabel('Colors in use:'))
        sidebarLayout.addWidget(self.colorList)
        self.sidebar = QWidget()
        self.sidebar.setLayout(sidebarLayout)
        self.sidebar.setMaximumWidth(200)

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
        logger.info(f"Updating current color text for index {index}.")
        self.currentColor.setText((self.model.data(index, Qt.ItemDataRole.DisplayRole)).upper())

    def addColumn(self):
        logger.debug("Adding column.")
        self.model.insertColumn(self.model.columnCount(QModelIndex()), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.modelWidth = self.model.columnCount(QModelIndex())
        self.widthSpinBox.setValue(self.modelWidth)

    def removeColumn(self):
        logger.debug("Removing column.")
        self.model.removeColumn(self.model.columnCount(QModelIndex()) - 1, self.beadworkView.currentIndex())
        self.modelWidth = self.model.columnCount(QModelIndex())
        self.widthSpinBox.setValue(self.modelWidth)

    def addRow(self):
        logger.debug("Adding row.")
        self.model.insertRow(self.model.rowCount(QModelIndex()), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.modelHeight = self.model.rowCount(QModelIndex())
        self.heightSpinBox.setValue(self.modelHeight)

    def removeRow(self):
        logger.debug("Removing row.")
        self.model.removeRow(self.model.rowCount(QModelIndex()) - 1, self.beadworkView.currentIndex())
        self.modelHeight = self.model.rowCount(QModelIndex())
        self.heightSpinBox.setValue(self.modelHeight)

    def widthChanged(self, value):
        logger.debug(f"Width changed to {value}.")
        self.beadworkView.setCurrentIndex(self.model.index(0, self.modelWidth - 1))
        if value > self.modelWidth:
            self.addColumn()
        else:
            self.removeColumn()
        self.modelWidth = self.model.columnCount(QModelIndex())

    def heightChanged(self, value):
        logger.debug(f"Height changed to {value}.")
        self.beadworkView.setCurrentIndex(self.model.index(self.modelHeight-1, 0))
        if value > self.modelHeight:
            self.addRow()
        else:
            self.removeRow()
        self.modelHeight = self.model.rowCount(QModelIndex())

    # TODO: implement
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
    def inColorMode(self, checked):
        if checked:
            self.selectionMode.setChecked(False)
            self.clearMode.setChecked(False)
        else:
            self.selectionMode.setChecked(True)

    # TODO: implement
    def inClearMode(self, checked):
        if checked:
            self.selectionMode.setChecked(False)
            self.colorMode.setChecked(False)
        else:
            self.selectionMode.setChecked(True)

    def changeOrientation(self, orientation):
        logger.debug(f"Changing orientation to {orientation}.")
        if orientation == "Horizontal":
            self.currentOrientation = "Horizontal"

            self.model = self.transposeModel
            logger.debug(f"self.model changed to {self.model}.")

            self.delegate.changeBeadDimensions(20, 10)

            self.beadworkView.setModel(self.model)
            self.beadworkView.changeOrientation()
            logger.debug(f"self.beadworkView.model() changed to {self.model}.")

            # temporarily disconnect signals to avoid crashes
            self.widthSpinBox.valueChanged.disconnect(self.widthChanged)
            self.heightSpinBox.valueChanged.disconnect(self.heightChanged)
            self.widthLabel.setText("Height:")
            self.widthSpinBox.setValue(self.model.columnCount(None))
            self.heightLabel.setText("Width:")
            self.heightSpinBox.setValue(self.model.rowCount(None))
            # reconnect signals
            self.widthSpinBox.valueChanged.connect(self.widthChanged)
            self.heightSpinBox.valueChanged.connect(self.heightChanged)
            logger.debug(f"widthLabel changed to {self.widthLabel.text()}, widthSpinBox changed to {self.widthSpinBox.value()}, heightLabel changed to {self.heightLabel.text()}, heightSpinBox changed to {self.heightSpinBox.value()}.")
        elif orientation == "Vertical":
            self.currentOrientation = "Vertical"

            self.model = self.origModel
            logger.debug(f"self.model changed to {self.model}.")

            self.delegate.changeBeadDimensions(10, 20)

            self.beadworkView.setModel(self.model)
            self.beadworkView.changeOrientation()
            logger.debug(f"self.beadworkView.model() changed to {self.model}.")

            # temporarily disconnect signals to avoid crashes
            self.widthSpinBox.valueChanged.disconnect(self.widthChanged)
            self.heightSpinBox.valueChanged.disconnect(self.heightChanged)
            self.widthLabel.setText("Width:")
            self.widthSpinBox.setValue(self.model.columnCount(None))
            self.heightLabel.setText("Height:")
            self.heightSpinBox.setValue(self.model.rowCount(None))
            # reconnect signals
            self.widthSpinBox.valueChanged.connect(self.widthChanged)
            self.heightSpinBox.valueChanged.connect(self.heightChanged)
            logger.debug(f"widthLabel changed to {self.widthLabel.text()}, widthSpinBox changed to {self.widthSpinBox.value()}, heightLabel changed to {self.heightLabel.text()}, heightSpinBox changed to {self.heightSpinBox.value()}.")
        logger.debug(f"Orientation changed to {orientation}.")