# by matthis pralat, matthispralat.fr
# with the help of Legigan Jeremy aka Pistiwique
# And s-Leger from Archipack
# thanks to blender lounge community

#------------------------------
# IMPORT
#------------------------------

import bpy
import subprocess
import os
import sys

#------------------------------
# INTERFACE - CLASS
#------------------------------

class PipModuleInstallPanel(bpy.types.Panel):
    bl_label = "Pip Module"
    bl_idname = "PIP_UTILS_PANEL_PT_VIEW3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "pip"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Pip module install")
        props = context.scene.PipUtilsPropertyGroup



        row = layout.row()
        PyStatut, PyMsg= verify_python_version(self) # verify Python Version on Blender and your computer

        # -- If Python version is not good
        if PyStatut == False:
            layout.label(text="1-Install python")
            layout.label(text="     Your version is not the same as blender, or is not installed ")
            row = layout.row()
            row.operator("modules_utils.install_python")

        # -- If Python version is good but pip is not installed
        if PyStatut == True and module_installed('pip') == False :
            layout.label(text="Install pip ")
            row.operator("modules_utils.ensure_pip")

        # -- Python and Pip installed !
        if module_installed('pip') == True and PyStatut == True:
            layout.label(text="pip is installed")

            # Custom Module installer ! tadaaa ! ----------------
            layout.label(text="Custom pip Module ")
            box = layout.box()
            row = box.row()
            row.prop(props, "newModuleName")
            row = box.row()
            row.operator("modules_utils.pip_custom")
            row.operator("modules_utils.unpip_custom")

        layout.label(text=" Open Console to follow installation")
        row = layout.row()
        row.operator('wm.console_toggle')

#------------------------------
# CLASSES
#------------------------------
class PipUtilsPropertyGroup( bpy.types.PropertyGroup ):
    newModuleName: bpy.props.StringProperty(name="",  default = "ex : PySide2")

class Pip:
    ''' Command in console '''
    def __init__(self, module=None, action="install", options=None):
        if module is not None:
            self.ensurepip()
            self._cmd(action, options, module)

    def _cmd(self, action, options, module):
        ''' In blender console do pip actions'''
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
        ''' Instal pip if not installed '''
        pip_not_found = False

        try:
            import pip
        except ImportError:
            pip_not_found = True
            print("Pip not installed")
            pass

        if pip_not_found:
            print("Installing and upgrading pip")
            PYPATH = bpy.app.binary_path_python
            self.run([PYPATH, "-m", "ensurepip"])
            self._cmd("install", ["--upgrade"], "pip")
        else:
            print("pip already install")

    @staticmethod
    def uninstall(module, options=None):
        if options is None:
            options = ["-y"] # force confirm
        Pip(module, "uninstall", options)

    @staticmethod
    def install(module, options=None):
        Pip(module, "install", options)


# OPERATORS BLENDER ------------------------------

class ensure_pip(bpy.types.Operator):
    '''Install pip'''
    bl_idname = "modules_utils.ensure_pip"
    bl_label = "2 - Install pip"

    def execute(self, context):
        PYPATH = bpy.app.binary_path_python
        cmd = str(PYPATH), "-m", "ensurepip"
        subprocess.run(cmd, shell=True, check=True)

class install_python(bpy.types.Operator):
    '''Open Python installer'''
    bl_idname = "modules_utils.install_python"
    bl_label = "1- Install Python"

    def execute(self, context):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.replace("\\", "\\\\")
        pyth_path = r"\app\python-3.7.0-amd64.exe"
        full_path = str(dir_path) + str(pyth_path)
        print(full_path)
        subprocess.call([full_path, "PrependPath=1" ])  # call exe and toogle add to path



class install_pip(bpy.types.Operator):
    '''Instal pip'''
    bl_idname = "modules_utils.pip_install"
    bl_label = "Install pip"

    def execute(self, context):
        Pip(self)
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
        module =  props.newModuleName
        Pip.install( module, options=["--user"])
        return {"FINISHED"}


class uninstall_module(bpy.types.Operator):
    '''Instaling PySide2 from PIP into your blender. Can be long, watch your system Console.'''
    bl_idname = "modules_utils.unpip_custom"
    bl_label = "Uninstall Module"
    def execute(self, context):
        props = context.scene.PipUtilsPropertyGroup
        module = props.newModuleName
        Pip.uninstall(module)
        return {"FINISHED"}

#------------------------------
# FUNCTIONS
#------------------------------

def verify_python_version(self):


    # GET BLENDER PYTHON VERSION  ------------------------
    BPV = sys.version_info # Blender PythonVersion
    BlenderPythonVersionBase = r"Python " + str(BPV[0]) + "." + str(BPV[1]) + "." + str(BPV[2]) + "  "
    BlenderPythonVersion = BlenderPythonVersionBase.strip()

    # GET WINDOWS PYTHON VERSION INSTALLED ------------------------
    PWV = subprocess.run(['python', '-V'], stdout=subprocess.PIPE)
    WindowsPythonVersion = str(PWV.stdout.decode('utf-8'))
    WindowsPythonVersion = WindowsPythonVersion.strip()

    if BlenderPythonVersion == WindowsPythonVersion:
        m1 = "your python path is the same as blender"
        msg = m1
        return (True, msg)

    else:
        m1 = "PYTHONPATH =" + str(WindowsPythonVersion)
        return( False , m1 )


def module_installed(self):
    ''' Check Module validity '''
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
    ensure_pip,
    install_python,
    install_pip,
    install_module,
    uninstall_module,
    PipUtilsPropertyGroup,
    install_pyside2,
    uninstall_pyside2,
    PipModuleInstallPanel,
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