
### 
#   TESTING
#
# For documentation on QAbstractTableModel: https://doc.qt.io/qt-5/qabstracttablemodel.html
###

import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

class BeadworkModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(BeadworkModel, self).__init__()
        self._data = data

    # this method must be implemented by a QAbstractTableModel subclass
    # index has a row and column
    # see https://doc.qt.io/qt-5/qt.html#ItemDataRole-enum for different roles
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # .row() -- index of outer list
            # .column() -- index of inner list
            return self._data[index.row()][index.column()]

    # this method must be implemented by a QAbstractTableModel subclass
    # length of outer list
    def rowCount(self, index):
        return len(self._data)

    # this method must be implemented by a QAbstractTableModel subclass
    # length of inner list
    def columnCount(self, index):
        return len(self._data[0]) # this implementation only works if all rows are the same length