import sys
import re

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import Widgets.compassWidget
reload(Widgets.compassWidget)
from Widgets.compassWidget import CompassWidget

def mayaMainWindow():
    """
    Returns the Maya main window as a Python object
    """
    mainWindowPtr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(mainWindowPtr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(mainWindowPtr), QtWidgets.QWidget)

class directionChangerView(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    
    def __init__(self, parent=mayaMainWindow()):
        super(directionChangerView, self).__init__(parent)

        self.setWindowTitle("Selection Sets")
        self.setMinimumWidth(300)

        # Checks the Python version then removes the ? from the dialog on windows
        if sys.version_info.major >= 3:
            self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:    
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.__buildUI()

    def __buildUI(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        self.compassWidget = CompassWidget()
        self.compassWidget.direction_vector_changed.connect(self.__directionChanged)
        self.compassWidget.size_changed.connect(self.__sizeChanged)
        self.compassWidget.angle_changed.connect(self.__angleChanged)
        mainLayout.addWidget(self.compassWidget)

    def __directionChanged(self, x, y):
        _x = str(x)
        _y = str(y)
        cmds.warning("Direction vector changed to " + _x + ", " + _y)

    def __sizeChanged(self, width, height):
        cmds.warning("Size changed to width: " + str(width) + " height: " + str(height))

    def __angleChanged(self, angle):
        cmds.warning("Angle changed to " + str(angle))

def showUI():
    """
    Shows the UI and deletes the reference when closed.

    Returns:
        Reference to the OffsetRandomiserView class
    """
    ui = directionChangerView()
    ui.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    ui.show(dockable=True)
    return ui