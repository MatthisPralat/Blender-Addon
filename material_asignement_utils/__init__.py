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

# <pep8 compliant>

# standard library import ---------

#------------------------------
# IMPORT
#------------------------------

import bpy
from bpy.app.handlers import persistent 

# Local imports ---------

# Initialisation of Main ui
from . import material_utils_ui
# function and operator for replace materials
from . import material_utils_replace_materials
# globals variables shared by multiples scripts
from . import material_utils_global_variable

#------------------------------
# ADD ON INFO
#------------------------------

bl_info = {
    "name": "Material asignement utils",
    "author": "Matthis Pralat",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": " View3D > SideBar > Material Asignement ",
    "description": "Material utilities for faster workflow with materials: Replacing material, making materials double sided or one sided",
    "warning": "",
    "wiki_url": "",
    "category": "Material",
}


#------------------------------
# LISTENERS / HANDLER
#------------------------------

# Hear depsgraph change 

# On each blender action call init handler
@persistent
def material_utils_handler_listener():
    bpy.app.handlers.depsgraph_update_pre.append(init_handler)

# clear listener if Add On desactivate 
def material_utils_clear_handler_listener():
    bpy.app.handlers.depsgraph_update_pre.clear(init_handler)


# Action to do in listeners
@persistent
def init_handler(scene):
    if material_utils_global_variable.materialNum != len(bpy.data.materials):
        print("Material Update")
        material_utils_replace_materials.UpdateProperty()

#------------------------------
# REGISTER / UNREGISTER / INIT
#------------------------------

def register():
    material_utils_ui.register()
    material_utils_replace_materials.register()
    material_utils_handler_listener()


def unregister():
    material_utils_ui.unregister()
    material_utils_replace_materials.unregister()
    material_utils_clear_handler_listener()

if __name__ == "__main__":
    register()


