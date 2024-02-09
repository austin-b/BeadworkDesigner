"""
Icons are provided by https://p.yusukekamiyamane.com/. They are licensed under a Creative Commons Attribution 3.0 License.
"""

import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QColorDialog,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QToolBar,
    QWidget,
    QVBoxLayout
)

from BeadworkModel import BeadworkModel
from BeadDelegate import BeadDelegate
from BeadworkView import BeadworkView
from ColorList import ColorList

base_dir = os.path.dirname(os.path.abspath(__file__))
bin_dir = os.path.join(base_dir, "bin")
icons_dir = os.path.join(bin_dir, "icons")

class MainWindow(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()

        ### SETUP MENU
        menu = self.menuBar()
        fileMenu = menu.addMenu('File')

        ### TODO: add dialog for width x height

        ### SETUP COLOR DIALOG
        colorDialog = QWidget()
        colorDialogLayout = QHBoxLayout()
        currentColorLabel = QLabel('Current Color: #') # TODO: fix padding with stylesheets
        currentColor = QLineEdit()
        currentColor.setInputMask('HHHHHH')   # only allows hex color input
        currentColor.textChanged.connect(lambda c: self.model.setData(self.beadworkView.currentIndex(), f"#{c}", Qt.ItemDataRole.EditRole)) # TODO: this currently only changes the last one selected, multiple selections do not work
        colorDialogWidget = QColorDialog()
        # colorDialogWidget.colorSelected.connect(lambda c: currentColor.setText(c.name().upper())) TODO: see below regarding .open()
        colorDialogButton = QPushButton('C') # TODO: add icon
        colorDialogButton.setFixedWidth(20)
        # colorDialogButton.clicked.connect(colorDialogWidget.open) TODO: use .open()
        colorDialogLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        colorDialogLayout.addWidget(currentColorLabel)
        colorDialogLayout.addWidget(currentColor)
        colorDialogLayout.addWidget(colorDialogButton)
        colorDialog.setLayout(colorDialogLayout)

        ### SETUP BEADWORK VIEW
        self.beadworkView = BeadworkView()
        self.model = BeadworkModel(debug=debug)
        self.delegate = BeadDelegate()
        self.beadworkView.setModel(self.model)
        self.beadworkView.setItemDelegate(self.delegate)
        self.beadworkView.clicked.connect(lambda c: currentColor.setText((self.model.data(c, Qt.ItemDataRole.DisplayRole)).upper()))

        ### SETUP ACTIONS
        # TODO: Add icons to the actions
        addColumnAction = QAction('Add Column', self)
        addColumnAction.triggered.connect(self.addColumn)

        removeColumnAction = QAction('Remove Column', self)
        removeColumnAction.triggered.connect(lambda: self.model.removeColumn(self.model.columnCount(None) - 1, self.beadworkView.currentIndex()))

        addRowAction = QAction('Add Row', self)
        addRowAction.triggered.connect(self.addRow)

        removeRowAction = QAction('Remove Row', self)
        removeRowAction.triggered.connect(lambda: self.model.removeRow(self.model.rowCount(None) - 1, self.beadworkView.currentIndex()))

        self.selectionMode = QAction('Selection Mode', self)
        self.selectionMode.setCheckable(True)
        self.selectionMode.triggered.connect(self.inSelectionMode)

        self.colorMode = QAction('Color Mode', self)
        self.colorMode.setCheckable(True)
        self.colorMode.triggered.connect(self.inColorMode)

        self.clearMode = QAction('Clear Mode', self)
        self.clearMode.setCheckable(True)
        self.clearMode.triggered.connect(self.inClearMode)

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
        # TODO: use proxy model to connect colorList to beadworkView
        colorList.setModel(self.model)

        ### SETUP COLOR SIDEBAR
        colorSidebarLayout = QVBoxLayout()
        colorSidebarLayout.addWidget(colorDialog)
        colorSidebarLayout.addWidget(QLabel('Colors in use:'))
        colorSidebarLayout.addWidget(colorList)
        colorSidebar = QWidget()
        colorSidebar.setLayout(colorSidebarLayout)
        colorSidebar.setMaximumWidth(200)

        ### SETUP MAIN LAYOUT & WIDGET
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(colorSidebar)
        mainLayout.addWidget(self.beadworkView)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)

        self.setCentralWidget(mainWidget)
        self.setMinimumSize(1200, 600)   
        self.setWindowTitle('Beadwork Designer')

    # TODO: only adds onto the end, not the current index -- FIX
    def addColumn(self):
        self.model.insertColumn(self.model.columnCount(None), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(None) - 1, self.model.columnCount(None) - 1), [Qt.ItemDataRole.BackgroundRole])

    # TODO: only adds onto the end, not the current index -- FIX
    def addRow(self):
        self.model.insertRow(self.model.rowCount(None), self.beadworkView.currentIndex())
        self.beadworkView.dataChanged(self.model.index(0, 0), self.model.index(self.model.rowCount(None) - 1, self.model.columnCount(None) - 1), [Qt.ItemDataRole.BackgroundRole])

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