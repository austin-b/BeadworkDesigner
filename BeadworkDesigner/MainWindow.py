"""
Icons are provided by https://p.yusukekamiyamane.com/. They are licensed under a Creative Commons Attribution 3.0 License.
"""

#####################
#
# TODO: write tests for models and other logic, non-display code (pytest)
# TODO: write unit tests for Qt (pytest-qt)
# TODO: create/make stylesheet
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

        ### SETUP MENU
        menu = self.menuBar()
        fileMenu = menu.addMenu('File')

        ### SETUP BEADWORK VIEW
        self.beadworkView = BeadworkView()
        self.origModel = BeadworkModel(debug=debug)
        self.model = self.origModel
        self.transposeModel = BeadworkTransposeModel() # TODO: create method/way to change orientation (use BeadworkView.changeOrientation()) and switch models
        self.transposeModel.setSourceModel(self.origModel)
        self.delegate = BeadDelegate()
        self.beadworkView.setModel(self.model)
        self.beadworkView.setItemDelegate(self.delegate)
        self.beadworkView.clicked.connect(lambda c: currentColor.setText((self.model.data(c, Qt.ItemDataRole.DisplayRole)).upper()))
        self.beadworkView.setObjectName("beadworkView")

        ### KEEP TRACK OF WIDTH x HEIGHT
        self.modelWidth = self.model.columnCount(QModelIndex())
        self.modelHeight = self.model.rowCount(QModelIndex())

        ### SETUP WIDTH x HEIGHT
        self.widthLabel = QLabel("Width:")
        self.widthSpinBox = QSpinBox()
        self.widthSpinBox.setValue(self.modelWidth)
        self.widthSpinBox.valueChanged.connect(self.widthChanged)
        self.heightLabel = QLabel("Height:")
        self.heightSpinBox = QSpinBox()
        self.heightSpinBox.setValue(self.modelHeight)
        self.heightSpinBox.valueChanged.connect(self.heightChanged)
        widthXHeightLayout = QHBoxLayout()
        widthXHeightLayout.addWidget(self.widthLabel)
        widthXHeightLayout.addWidget(self.widthSpinBox)
        widthXHeightLayout.addWidget(self.heightLabel)
        widthXHeightLayout.addWidget(self.heightSpinBox)
        widthXHeightWidget = QWidget()
        widthXHeightWidget.setLayout(widthXHeightLayout)

        ### SETUP ORIENTATION OPTIONS
        self.orientationOptions = ["Vertical", "Horizontal"]
        self.currentOrientation = "Vertical" # TODO: make this default changeable via settings
        orientationLabel = QLabel("Orientation:")
        orientationComboBox = QComboBox()
        orientationComboBox.addItems(self.orientationOptions)
        orientationComboBox.setCurrentText(self.currentOrientation)
        orientationComboBox.setEditable(False)
        orientationComboBox.currentTextChanged.connect(self.changeOrientation)
        orientationLayout = QHBoxLayout()
        orientationLayout.addWidget(orientationLabel)
        orientationLayout.addWidget(orientationComboBox)
        orientationWidget = QWidget()
        orientationWidget.setLayout(orientationLayout)

        ### SETUP COLOR DIALOG
        colorDialog = QWidget()
        colorDialogLayout = QHBoxLayout()
        currentColorLabel = QLabel('Current Color: #')
        currentColorLabel.setObjectName("currentColorLabel")
        currentColor = QLineEdit()
        currentColor.setFixedWidth(47)
        currentColor.setInputMask('HHHHHH')   # only allows hex color input
        currentColor.textChanged.connect(lambda c: self.model.setData(self.beadworkView.currentIndex(), f"#{c}", Qt.ItemDataRole.EditRole)) # TODO: this currently only changes the last one selected, multiple selections do not work
        colorDialogWidget = QColorDialog()
        # colorDialogWidget.colorSelected.connect(lambda c: currentColor.setText(c.name().upper())) TODO: see below regarding .open()
        colorDialogButton = QPushButton()
        colorDialogButton.setFixedWidth(20)
        colorDialogButton.setIcon(QIcon(os.path.join(icons_dir, "palette.png")))
        # colorDialogButton.clicked.connect(colorDialogWidget.open) TODO: use .open()
        colorDialogLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        colorDialogLayout.addWidget(currentColorLabel)
        colorDialogLayout.addWidget(currentColor)
        colorDialogLayout.addWidget(colorDialogButton)
        colorDialog.setLayout(colorDialogLayout)

        ### SETUP ACTIONS
        addColumnAction = QAction('Add Column', self)
        addColumnAction.triggered.connect(self.addColumn)
        addColumnAction.setIcon(QIcon(os.path.join(icons_dir, "table-insert-column.png")))

        removeColumnAction = QAction('Remove Column', self)
        removeColumnAction.triggered.connect(self.removeColumn)
        removeColumnAction.setIcon(QIcon(os.path.join(icons_dir, "table-delete-column.png")))

        addRowAction = QAction('Add Row', self)
        addRowAction.triggered.connect(self.addRow)
        addRowAction.setIcon(QIcon(os.path.join(icons_dir, "table-insert-row.png")))

        removeRowAction = QAction('Remove Row', self)
        removeRowAction.triggered.connect(self.removeRow)
        removeRowAction.setIcon(QIcon(os.path.join(icons_dir, "table-delete-row.png")))

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

        ### SETUP TOOLBAR
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.addAction(addColumnAction)
        toolbar.addAction(removeColumnAction)
        toolbar.addAction(addRowAction)
        toolbar.addAction(removeRowAction)
        toolbar.addSeparator()
        toolbar.addAction(self.selectionMode)
        toolbar.addAction(self.colorMode)
        toolbar.addAction(self.clearMode)

        ### SETUP COLOR LIST
        colorList = ColorList()
        # TODO: proxyModel does not work -- fix
        # self.proxyModel = BeadworkToColorListProxyModel()
        # self.proxyModel.setSourceModel(self.model)
        colorList.setModel(self.model)

        ### SETUP SIDEBAR
        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(widthXHeightWidget)
        sidebarLayout.addWidget(orientationWidget)
        sidebarLayout.addWidget(colorDialog)
        sidebarLayout.addWidget(QLabel('Colors in use:'))
        sidebarLayout.addWidget(colorList)
        sidebar = QWidget()
        sidebar.setLayout(sidebarLayout)
        sidebar.setMaximumWidth(200)

        ### SETUP MAIN LAYOUT & WIDGET
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(sidebar)
        mainLayout.addWidget(self.beadworkView)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)

        self.setStyleSheet(open(os.path.join(qss_dir, "style.qss")).read())
        self.setCentralWidget(mainWidget)
        self.setMinimumSize(1200, 600)   
        self.setWindowTitle('Beadwork Designer')

    def addColumn(self):
        self.model.insertColumn(self.model.columnCount(QModelIndex()), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.modelWidth = self.model.columnCount(QModelIndex())
        self.widthSpinBox.setValue(self.modelWidth)

    def removeColumn(self):
        self.model.removeColumn(self.model.columnCount(QModelIndex()) - 1, self.beadworkView.currentIndex())
        self.modelWidth = self.model.columnCount(QModelIndex())
        self.widthSpinBox.setValue(self.modelWidth)

    def addRow(self):
        self.model.insertRow(self.model.rowCount(QModelIndex()), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(QModelIndex()) - 1, self.model.columnCount(QModelIndex()) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.modelHeight = self.model.rowCount(QModelIndex())
        self.heightSpinBox.setValue(self.modelHeight)

    def removeRow(self):
        self.model.removeRow(self.model.rowCount(QModelIndex()) - 1, self.beadworkView.currentIndex())
        self.modelHeight = self.model.rowCount(QModelIndex())
        self.heightSpinBox.setValue(self.modelHeight)

    def widthChanged(self, value):
        self.beadworkView.setCurrentIndex(self.model.index(0, self.modelWidth - 1))
        if value > self.modelWidth:
            self.addColumn()
        else:
            self.removeColumn()

    def heightChanged(self, value):
        self.beadworkView.setCurrentIndex(self.model.index(self.modelHeight-1, 0))
        if value > self.modelHeight:
            self.addRow()
        else:
            self.removeRow()

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

    # TODO: changing from horizontal and back to vertical does not work -- fix
    def changeOrientation(self, orientation):
        if orientation == "Horizontal":
            self.currentOrientation = "Horizontal"
            self.model = self.transposeModel
            self.delegate.changeBeadDimensions(20, 10)
            self.beadworkView.setModel(self.model)
            self.beadworkView.changeOrientation()
            self.widthLabel.setText("Height:")
            self.widthSpinBox.setValue(self.model.columnCount(QModelIndex()))
            self.heightLabel.setText("Width:")
            self.heightSpinBox.setValue(self.model.rowCount(QModelIndex()))
        elif orientation == "Vertical":
            self.currentOrientation = "Vertical"
            self.model = self.origModel
            self.delegate.changeBeadDimensions(10, 20)
            self.beadworkView.setModel(self.model)
            self.beadworkView.changeOrientation()
            self.widthLabel.setText("Width:")
            self.widthSpinBox.setValue(self.model.columnCount(QModelIndex()))
            self.heightLabel.setText("Height:")
            self.heightSpinBox.setValue(self.model.rowCount(QModelIndex()))