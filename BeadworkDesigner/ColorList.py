import logging

from PySide6.QtCore import QAbstractProxyModel, QModelIndex, Qt
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QColorDialog, QListView, QMenu

logger = logging.getLogger(__name__)

class BeadworkToColorListProxyModel(QAbstractProxyModel):
    """A proxy model that converts a BeadworkModel to a list of unique colors.

    Must call setSourceModel() with a BeadworkModel to display the colors.
    """

    def __init__(self, parent = None):
        """Initializes the BeadworkToColorListProxyModel.

        Args:
            parent (QObject, optional): The parent object. Defaults to None.
        """
        super().__init__(parent) 

        self._colors = {}
        self._colors_index = []

        logger.info("BeadworkToColorListProxyModel initialized.")

    def setSourceModel(self, sourceModel):
        """Sets the source model for the proxy model.

        Args:
            sourceModel (BeadworkModel): The source model to set. Must be a BeadworkModel.
        """
        super().setSourceModel(sourceModel)  

        self._sourceModel = sourceModel
        
        self.evaluateModelForUniqueColors()

    def data(self, index, role):
        """Returns the data for the given index and role.

        Args:
            index (QModelIndex): The index of the data.
            role (Qt.ItemDataRole.DisplayRole,
                  Qt.ItemDataRole.BackgroundRole): The role of the data.

        Returns:
            Qt.ItemDataRole.DisplayRole -> str: The color at the given index.
            Qt.ItemDataRole.BackgroundRole -> QColor: The color at the given index.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            return self._colors_index[index.row()]
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor(self._colors_index[index.row()])
        else:
            return None

    def rowCount(self, parent):
        """Returns the number of rows in the model.
        
        Args:
            parent (QModelIndex): The parent index.
        
        Returns:
            int: The number of rows in the model.
        """
        return len(self._colors_index)
    
    def columnCount(self, parent):
        """Returns the number of columns in the model.
        
        Args:
            parent (QModelIndex): The parent index.
            
        Returns:
            int: 1 (the number of columns in the model).
        """
        return 1
    
    def index(self, row, column, parent=QModelIndex()):
        """Returns a QIndex for the given row and column.
        
        Args:
            row (int): The row of the index.
            column (int): The column of the index.
            parent (QModelIndex, optional): The parent index. Defaults to QModelIndex().
        """
        return self.createIndex(row, column)
    
    # not sure why this is needed, but it is
    # I believe this behavior defines it as a list model -
    # a single parent index is returned for all rows
    def parent(self, index):
        """Returns the parent index of the given index.
        
        Args:
            index (QModelIndex): The index to find the parent of.
            
        Returns:
            QModelIndex: The parent index of the given index.
        """
        return QModelIndex()

    def mapFromSource(self, sourceIndex):
        """Maps the source index (BeadworkModel) to the proxy 
        index (BeadworkToColorListProxyModel)

        Args:
            sourceIndex (QModelIndex): The index in the source model.

        Returns:
            QModelIndex: The index in the proxy model.
        """
        color = self.sourceModel().data(sourceIndex, Qt.ItemDataRole.DisplayRole)
        logger.debug(f"Mapping from source color: {color}, index: {sourceIndex}")
        proxyIndex = self.createIndex(self._colors_index.index(color), 0) # returns the location in the colors_index list
        logger.debug(f"Mapped to proxy index: {proxyIndex}")
        return proxyIndex

    def mapToSource(self, proxyIndex):
        """Maps the proxy index (BeadworkToColorListProxyModel) to the source
        index (BeadworkModel).

        Args:
            proxyIndex (QModelIndex): The index in the proxy model.

        Returns:
            QModelIndex: The index in the source model.
        """
        try:
            color = self.data(proxyIndex, Qt.ItemDataRole.DisplayRole)
        except:         # occasionally when using clear mode, the proxyIndex is invalid
                        # this is a workaround to prevent a crash
            logger.error(f"Invalid proxy index: {proxyIndex}, using 0,0.")
            self.evaluateModelForUniqueColors()
            proxyIndex = self.index(0, 0)
            color = self.data(proxyIndex, Qt.ItemDataRole.DisplayRole)
        logger.debug(f"Mapping to source color: {color}, index: {proxyIndex}")
        r, c = self._colors[color][0] # we only return the first index of the color
        sourceIndex = self.sourceModel().index(r, c) 
        logger.debug(f"Mapped to source index: {sourceIndex}")
        return sourceIndex
    
    def mapToAllSourceIndexes(self, proxyIndex):
        """Given a proxy index, returns all source indexes that have the same color.

        Args:
            proxyIndex (QModelIndex): The index in the proxy model.

        Returns:
            list: A list of all indexes in the source model that have the same color as proxyIndex.
        """
        color = self.data(proxyIndex, Qt.ItemDataRole.DisplayRole)
        return self.allIndexesForColor(color, proxyIndex)
    
    def allIndexesForColor(self, color, proxyIndex=None):
        """Given a color, returns all source indexes that have that color.

        Args:
            color (str): The color to search for.
            proxyIndex (QModelIndex, optional): The proxy index to search from. Defaults to None.

        Returns:
            list: A list of all indexes in the source model that have the same color as proxyIndex.
        """
        try:
            logger.debug(f"Mapping to source color: {color}, index: {proxyIndex}")
            indexes = self._colors[color]
            logger.debug(f"Mapped to source indexes: {indexes}")
            sourceIndexes = map(lambda index: self.sourceModel().index(index[0], index[1]),
                                indexes)
            return list(sourceIndexes)
        except KeyError:    # just in case the color is not valid
            return None   
        
    def changeAllInstancesOfColor(self, initColor, newColor):
        """Changes all instances of a color in the source model to a new color.

        Args:
            initColor (str): The color to change.
            newColor (str): The new color to change to.
        """
        indexes = self.allIndexesForColor(initColor)
        logger.info(f"Changing all instances of {initColor} to {newColor}.")
        for index in indexes:
            self.sourceModel().setData(index, newColor, Qt.ItemDataRole.EditRole)

    # runs through model and creates a dictionary of unique colors
    def evaluateModelForUniqueColors(self):
        """Evaluates the source model for unique colors and stores them in a dictionary.

        The dictionary is stored as self._colors, with the color as the key and a list of indexes as the value.
        """
        self._colors = {} # reinitialize whenever we call this to prevent carryovers
        for row in range(self.sourceModel().rowCount(None)):
            for column in range(self.sourceModel().columnCount(None)):
                color = self.sourceModel().data(self._sourceModel.index(row, column), Qt.ItemDataRole.DisplayRole)
                if color not in self._colors:
                    self._colors[color] = [(row, column)]
                else:
                    self._colors[color].append((row, column))
        self._colors_index = list(self._colors)
        self._colors_index.sort()

    ### SLOTS
    def updateList(self, topLeft, bottomRight):
        """Slot for when the data in the source model changes.

        Args:
            topLeft (QModelIndex): The top left index of the data that changed.
            bottomRight (QModelIndex): The bottom right index of the data that changed.
        """
        logger.debug(f"Data changed: {topLeft}, {bottomRight}.")
        self.evaluateModelForUniqueColors()
        self.dataChanged.emit(self.mapFromSource(topLeft), self.mapFromSource(bottomRight))

# TODO: implement a method to select all in source model/view that match the color clicked on
class ColorList(QListView):
    """A view for the ColorListProxyModel that displays a list of unique colors.

    Must call setModel() with a ColorListProxyModel to display the colors.
    """

    def __init__(self):
        """Initializes the ColorList view and GUI elements."""
        super().__init__()

        self.triggeredIndex = None # index of the item that was right-clicked

        self.colorDialog = QColorDialog() # used to select the new color
        self.colorDialog.colorSelected.connect(lambda c: self.triggerChangeAll(c.name().upper()))

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.customContextMenu)

        self.selectAllAction = QAction("Select All", self) # TODO: implement

        self.changeAllAction = QAction("Change All Occurrences", self)
        self.changeAllAction.triggered.connect(self.openColorDialog)

        # self.setItemDelegate(ColorListDelegate())

        logger.info("ColorList initialized.")

    def customContextMenu(self, point):
        """Opens a custom context menu when right-clicked.

        Args:
            point (QPoint): The point where the right-click occurred.
        """
        self.triggeredIndex = self.indexAt(point)
        logger.debug(f"Triggered ColorList custom context menu at {self.triggeredIndex}.")

        if self.triggeredIndex.isValid():
            menu = QMenu(self)
            menu.addAction(self.selectAllAction)
            menu.addAction(self.changeAllAction)
            menu.exec(self.mapToGlobal(point))

    def openColorDialog(self):
        """Opens the color dialog to select a new color."""
        self.colorDialog.show()

    def triggerChangeAll(self, newColor):
        """Triggers the change of all occurrences of the color clicked on to the new color.

        Args:
            newColor (str): The new color to change all occurrences to.
        """
        self.model().changeAllInstancesOfColor(self.triggeredIndex.data(Qt.ItemDataRole.DisplayRole), newColor)

    def updateSelected(self, sourceIndex): 
        """Updates the selected item in the ColorList view.

        Args:
            sourceIndex (QModelIndex): The index of the source item selected.
        """ 
        proxyIndex = self.model().mapFromSource(sourceIndex)
        self.setCurrentIndex(proxyIndex)
        self.scrollTo(proxyIndex)

# TODO: implement properly -- selection is not working
        # maybe using https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QStylePainter.html?
# class ColorListDelegate(QItemDelegate):
    
#     def __init__(self):
#         super().__init__()

#     def paint(self, painter, option, index):
#         if bool(option.state & QStyle.StateFlag.State_Selected):
#             painter.setPen(QColor("#000000"))
#             painter.drawRect(option.rect)
#         else:
#             painter.setPen(QColor("#FFFFFF"))
#             painter.drawRect(option.rect)

#         # translate
#         option.rect.translate(2, 2)

#         # resize
#         option.rect.setSize(QSize(option.rect.width()-2, option.rect.height()-6))
        
#         # draw a rectangle
#         background_color = index.data(role = Qt.ItemDataRole.BackgroundRole)
#         painter.fillRect(option.rect, background_color)