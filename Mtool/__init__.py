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
# And s-Leger from Archipack
# thanks to blender lounge community

# standard library import ---------

#------------------------------
# IMPORT
#------------------------------

import bpy
# Todo : if PySide2 is not instaled open other window with indications
from . import Mtools_Popup

#------------------------------
# ADD-ON INFO
#------------------------------

bl_info = {
    "name": "Mtool",
    "author": "Matthis Pralat, Special thanks to : Pistiwique and stephen-l from Archipack ",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": " View3D > SideBar > PySide2 ",
    "description": "Personal scripts utilities with PySide2 integration",
    "warning": "Working for Windows not tested for linux & mac",
    "wiki_url": "matthispralat.fr",
    "category": "Developement",
}

#--------------------------------
# Panel Launcher
#--------------------------------

class MtoolPanelLauncher(bpy.types.Panel):
    '''Main Panel Launcher'''
    bl_label = "Popup tools"
    bl_idname = "MATERIAL_UTILS_PANEL_PT_VIEW3D_2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mtools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("mtools.open_mtools_popup")


#------------------------------
# REGISTER / UNREGISTER / INIT
#------------------------------

CLASSES = [
    MtoolPanelLauncher,
    ]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    Mtools_Popup.register()

def unregister():

    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

    Mtools_Popup.unregister()

if __name__ == "__main__":
    register()


