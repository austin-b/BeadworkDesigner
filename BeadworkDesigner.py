"""
Icons are provided by https://p.yusukekamiyamane.com/. They are licensed under a Creative Commons Attribution 3.0 License.
"""

#####################
#
# TODO: create/make stylesheet
# TODO: add save and load options to file menu
# TODO: add a way to change the size of the beads
# TODO: add a way to zoom in and out
# TODO: add a way to change orientation of the model
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

import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QColorDialog,
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

from BeadworkModel import BeadworkModel
from BeadDelegate import BeadDelegate
from BeadworkView import BeadworkView
from ColorList import BeadworkToColorListProxyModel, ColorList

base_dir = os.path.dirname(os.path.abspath(__file__))
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
        self.model = BeadworkModel(debug=debug)
        self.delegate = BeadDelegate()
        self.beadworkView.setModel(self.model)
        self.beadworkView.setItemDelegate(self.delegate)
        self.beadworkView.clicked.connect(lambda c: currentColor.setText((self.model.data(c, Qt.ItemDataRole.DisplayRole)).upper()))
        self.beadworkView.setObjectName("beadworkView")

        ### KEEP TRACK OF WIDTH x HEIGHT
        self.modelWidth = self.model.columnCount(None)
        self.modelHeight = self.model.rowCount(None)

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

        ### SETUP COLOR SIDEBAR
        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(widthXHeightWidget)
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
        self.model.insertColumn(self.model.columnCount(None), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(None) - 1, self.model.columnCount(None) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.modelWidth = self.model.columnCount(None)
        self.widthSpinBox.setValue(self.modelWidth)

    def removeColumn(self):
        self.model.removeColumn(self.model.columnCount(None) - 1, self.beadworkView.currentIndex())
        self.modelWidth = self.model.columnCount(None)
        self.widthSpinBox.setValue(self.modelWidth)

    def addRow(self):
        self.model.insertRow(self.model.rowCount(None), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(None) - 1, self.model.columnCount(None) - 1), [Qt.ItemDataRole.BackgroundRole])
        self.modelHeight = self.model.rowCount(None)
        self.heightSpinBox.setValue(self.modelHeight)

    def removeRow(self):
        self.model.removeRow(self.model.rowCount(None) - 1, self.beadworkView.currentIndex())
        self.modelHeight = self.model.rowCount(None)
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

app = QApplication(sys.argv)
window = MainWindow(debug=("--debug" in sys.argv))  # check if debug flag is set
window.show()

app.exec()