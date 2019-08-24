# by matthis pralat, matthispralat.fr
# with the help of Legigan Jeremy aka Pistiwique
# And s-Leger from Archipack
# thanks to blender lounge community

'''

Init Interface for Material Utils 

'''

import bpy
import subprocess

def module_installed(self):
    print('mom module: ', self)
    moduleStatus = True
    try:
        code = 'import ' + self
        exec (code)
    except ImportError:
        moduleStatus = False

    if moduleStatus == False:
        print('module', self, 'not set')
    if moduleStatus == True:
        print('module', self, 'is set')

    return moduleStatus

if module_installed('PySide2'):
    from . import PySide2_MaterialUi
else:
    print("INSTALL2 !")
# Main ui
class MaterialUtilsPanel2(bpy.types.Panel):
    bl_label = "Pip Module"
    bl_idname = "MATERIAL_UTILS_PANEL_PT_VIEW3D_2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PySide2"

    def draw(self, context):
        layout = self.layout
        layout.label(text="PySide2 Exemple")
        props = context.scene.PipUtilsPropertyGroup

        row = layout.row()
        if module_installed('pip') == False or  module_installed('PySide2') == False :
            layout.label(text="Install PySide2 ")
            row = layout.row()
            row.operator("modules_utils.pip_pyside2")

        else:
            layout.label(text="PySide2 Exemple ")
            row = layout.row()
            row.operator("material_utils.display_py_window")
            layout.label(text="Custom pip Module ")
            box = layout.box()
            row = box.row()
            row.prop(props, "newModuleName")
            row = box.row()
            row.operator("modules_utils.pip_custom")
            row.operator("modules_utils.unpip_custom")




class PipUtilsPropertyGroup( bpy.types.PropertyGroup ):
    # Init Linked Library Update
    newModuleName: bpy.props.StringProperty(name="",  default = "Your pip Module")


# -- Operator ------

class Pip:

    def __init__(self, module=None, action="install", options=None):
        if module is not None:
            self.ensurepip()
            self._cmd(action, options, module)

    def _cmd(self, action, options, module):
        PYPATH = bpy.app.binary_path_python
        cmd = [PYPATH, "-m", "pip", action]
        if options is not None:
            cmd.extend(options)
        cmd.append(module)
        self.run(cmd)

    def _run(self, cmd):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        popen.wait()

    def run(self, cmd):
        for res in self._run(cmd):
            if "ERROR:" in res:
                raise Exception(res)
            print(res)

    def ensurepip(self):
        pip_not_found = False
        try:
            import pip
        except ImportError:
            pip_not_found = True
            pass
        if pip_not_found:
            print("install pip")
            PYPATH = bpy.app.binary_path_python
            self.run([PYPATH, "-m", "ensurepip"])
            self._cmd("install", ["--upgrade"], "pip")

    @staticmethod
    def uninstall(module, options=None):
        if options is None:
            # force confirm
            options = ["-y"]
        Pip(module, "uninstall", options)

    @staticmethod
    def install(module, options=None):
        Pip(module, "install", options)

class pyside2_material_utils(bpy.types.Operator):
    '''Exemple of interface'''
    bl_idname = "material_replace.pyside2_interface"
    bl_label = "Mu with PySide2"
    def execute(self, context):
        PySide2_MaterialUi.mregister()
        #print("hello")
        #Pip.install("PySide2", options=["--user"])
        return {"FINISHED"}

class install_pyside2(bpy.types.Operator):
    '''Instaling PySide2 from PIP into your blender. Can be long, watch your system Console.'''
    bl_idname = "modules_utils.pip_pyside2"
    bl_label = "Install PySide2"
    def execute(self, context):
        print("hello")
        Pip.install("PySide2", options=["--user"])
        return {"FINISHED"}


class uninstall_pyside2(bpy.types.Operator):
    '''Uninstall Pyside 2'''
    bl_idname = "modules_utils.unpip_pyside2"
    bl_label = "Uninstall PySide2"
    def execute(self, context):
        print("hello")
        Pip.uninstall("PySide2")
        return {"FINISHED"}


class install_module(bpy.types.Operator):
    '''Instaling PySide2 from PIP into your blender. Can be long, watch your system Console.'''
    bl_idname = "modules_utils.pip_custom"
    bl_label = "Install Module"

    def execute(self, context):
        props = context.scene.PipUtilsPropertyGroup
        #print(props.newModuleName)
        module =  props.newModuleName
        Pip.install( module, options=["--user"])
        return {"FINISHED"}

class uninstall_module(bpy.types.Operator):
    '''Instaling PySide2 from PIP into your blender. Can be long, watch your system Console.'''
    bl_idname = "modules_utils.unpip_custom"
    bl_label = "Uninstall Module"
    def execute(self, context):
        print(props.newModuleName)
        module = props.newModuleName
        Pip.install(module)
        return {"FINISHED"}

# -- Functions ------
# check module validity
def module_installed(self):
    print('mom module: ', self)
    moduleStatus = True
    try:
        code = 'import ' + self
        exec (code)
    except ImportError:
        moduleStatus = False

    if moduleStatus == False:
        print('module', self, 'not set')
    if moduleStatus == True:
        print('module', self, 'is set')

    return moduleStatus

# -----------------------------
# REGISTER / UNREGISTER / INIT
#------------------------------

classes = [
    pyside2_material_utils,
    install_module,
    uninstall_module,
    PipUtilsPropertyGroup,
    install_pyside2,
    uninstall_pyside2,
    MaterialUtilsPanel2,
    ]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.PipUtilsPropertyGroup = bpy.props.PointerProperty(type=PipUtilsPropertyGroup)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()