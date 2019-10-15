import bpy
import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QDialog
from PySide2.QtCore import QFile, QObject, Qt, QSize
from PySide2 import QtGui, QtWidgets, QtGui

# ------------------
#   Open Window
# ------------------

class Open_Mtools_Popup(bpy.types.Operator):
    '''Open Mtools popup '''

    bl_idname = "mtools.open_mtools_popup"
    bl_label = "M Tools"
    bl_options = {'REGISTER'}

    def execute(self, context):
        self.app = QtWidgets.QApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        self.widget = Window()
        return {'FINISHED'}

#-------------
# Main Window
#-------------
class Window(QtCore.QObject):

    def __init__(self, parent=None):
        super(Window,self).__init__(parent)
        self.load_interface()
        # interface
        self.script_path = os.path.realpath(__file__)
        self.directory = os.path.dirname(self.script_path)
        self.ui_path = self.directory + r"\resources\SourceInterface.ui"
        print(self.ui_path)
        self.ui_file = QtCore.QFile(self.ui_path)
        self.ui_file.open(QtCore.QFile.ReadOnly)
        self.loader = QtUiTools.QUiLoader()
        self.window = self.loader.load(self.ui_file)
        self.ui_file.close()
        self.window.setWindowFlags(self.window.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.window.show()



    def load_interface(self):
        print("hello")
        pass
    def load_style(self):
        pass
    def setup_connection(self):
        pass



CLS =[
    Open_Mtools_Popup,
    ]

def register():
    for cls in CLS:
        bpy.utils.register_class(cls)

def unregister():
    for cls in CLS:
        bpy.utils.unregister_class(cls)
