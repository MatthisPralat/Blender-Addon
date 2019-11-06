# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# by matthis pralat, matthispralat.fr
# with the help of Legigan Jeremy aka Pistiwique
# And Stephen-L from Archipack
# thanks to blender lounge community

# standard library import ---------


#------------------------------
# ADD ON INFO
#------------------------------

bl_info = {
    "name": "Pip_Modules",
    "author": "Matthis Pralat, Special thanks to : Pistiwique and Stephen-L",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": " View3D > SideBar > Pip ",
    "description": "Install new modules with pip to enable new possibility with blender like PySide2 for custom Ui ",
    "warning": "Working for Windows not tested for linux & mac",
    "wiki_url": "matthispralat.fr",
    "category": "Developement",
}



#------------------------------
# IMPORT
#------------------------------

import bpy

# Initialisation of Main ui
from . import PipModule # PIP related utilities

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


#------------------------------
# REGISTER / UNREGISTER / INIT
#------------------------------


def register():
    PipModule.register()

def unregister():
    PipModule.unregister()


if __name__ == "__main__":
    register()


