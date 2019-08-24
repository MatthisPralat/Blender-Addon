# by matthis pralat, matthispralat.fr
# with the help of Legigan Jeremy aka Pistiwique
# And s-Leger from Archipack
# thanks to blender lounge community

import bpy
import sys
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QDialog
from PySide2.QtCore import QFile, QObject, Qt, QSize
from PySide2 import QtGui, QtWidgets, QtGui
from PySide2.QtGui import QIcon



# the need is to create windows with function and register, not main
# Create basic window


# ------------------
#   OPERATOR
# ------------------

class PYSIDE2_OT_matut_panel(bpy.types.Operator):

    bl_idname = 'material_utils.display_py_window'
    bl_label = "Material utilities PS2"
    bl_options = {'REGISTER'}

    def execute(self, context):
        self.app = QtWidgets.QApplication.instance()
        if not self.app:
            self.app = QtWidgets.QApplication(['blender'])
        #self.app.exec_()
        script_file = os.path.realpath(__file__)
        directory = os.path.dirname(script_file)
        #self.widget = Example()
        path = directory + "/PySide2ExempleMaterialUtils.ui"
        self.widget = Form(path)

        return {'FINISHED'}

#   CLASS
# ------------------
class Form(QObject):

    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        # ui = Ui_Form()
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        script_file = os.path.realpath(__file__)
        directory = os.path.dirname(script_file)
        path = directory + r"\stylesheet\ConsoleStyle.qss"
        s_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        with open(s_path, 'r') as f:
            self.window.setStyleSheet(f.read())


        # ---------------------------------------
        # SET BUTTONS
        # ---------------------------------------

        # CleanMat_all ----
        button = self.window.findChild(QPushButton, "IteMatBtn_all")
        button.clicked.connect(IteMat)

        # CleanMat_all ----
        button = self.window.findChild(QPushButton, "RemUnMat_all")
        button.clicked.connect(RemUn)

        # CleanMat_all ----
        button = self.window.findChild(QPushButton, "CleanMat_all")
        button.clicked.connect(CleanMat)

        # CleanMat_all ----
        button = self.window.findChild(QPushButton, "Suzanne")
        button.clicked.connect(Suz)

        # self.Button3 = self.findChild(QtGui.QPushButton, 'pushButton_3')
        # widget = self.QtGui.findChild(QPushButton, "pushButton_3")
        # print(pushButton_4)
        # self.Button3.clicked.connect(self.Button3)

        self.window.show()

def IteMat():
    bpy.ops.material_utilities_ps2.replace_iterative_materials()
def RemUn():
    bpy.ops.material_utilities_ps2.remove_unused_materials()
def CleanMat():
    bpy.ops.material_utilities_ps2.clean_materials_slots()
def Suz():
    bpy.ops.mesh.primitive_monkey_add()


CLASSES = [
    PYSIDE2_OT_matut_panel,
    ]


#def IteMatBtn_all():
    #print("helllo")

def register():

    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
