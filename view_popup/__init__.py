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

# ------------------------------
# IMPORT
# ------------------------------

import bpy
from bpy.types import Header, Menu, Panel

# ------------------------------
# ADD ON INFO
# ------------------------------

bl_info = {
    "name": "Editor Popup",
    "author": "Matthis Pralat",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": " Header > Icon ",
    "description": "Open editor type in popup",
    "warning": "",
    "wiki_url": "",
    "category": "Editor",
}


# ------------------------------
# Add PanneL
# ------------------------------

class TOPBAR_HT_popup_editor(Header):
    bl_space_type = 'TOPBAR'

    def draw(self, context):
        region = context.region

        if region.alignment == 'RIGHT':
            self.draw_right(context)
            
    def draw_right(self, context):
        layout = self.layout

        window = context.window
        screen = context.screen
        scene = window.scene

        # If statusbar is hidden, still show messages at the top
        if not screen.show_statusbar:
            layout.template_reports_banner()
            layout.template_running_jobs()

        # Active workspace view-layer is retrieved through window, not through workspace.
        layout = self.layout
        layout.separator()
        layout.operator("popup.open_viewtd", icon='VIEW3D')
        layout.operator("popup.open_uv", icon='UV')
        layout.operator("popup.open_shader", icon='NODE_MATERIAL')
        layout.operator("popup.open_layout", icon='NODE_MATERIAL')


# ------------------------------
# OPPERATOR
# ------------------------------

class Popup_View3D(bpy.types.Operator):
    """
        Create View 3D popup
    """

    bl_idname = "popup.open_viewtd"
    bl_label = ""

    def execute(self, context):
        Popup("VIEW_3D")
        return {'FINISHED'}


class Popup_UV(bpy.types.Operator):
    """
       Create UV popup
    """

    bl_idname = "popup.open_uv"
    bl_label = ""

    def execute(self, context):
        Popup("IMAGE_EDITOR")
        return {'FINISHED'}


class Popup_Shader(bpy.types.Operator):
    """  Replace all materials setted in MaterialToReplace 
         by the setted material in material replace
    """

    bl_idname = "popup.open_shader"
    bl_label = ""

    def execute(self, context):
        Popup("NODE_EDITOR")
        return {'FINISHED'}

class Popup_Layout(bpy.types.Operator):
    """
       Create UV popup
    """

    bl_idname = "popup.open_uv"
    bl_label = ""

    def execute(self, context):
        Popup("IMAGE_EDITOR")
        return {'FINISHED'}


def Popup(selArea):
    # Modify scene settings
    render = bpy.context.scene.render
    render.resolution_x = 640
    render.resolution_y = 480
    render.resolution_percentage = 100
    render.display_mode = "WINDOW"

    # Call image editor window
    bpy.ops.render.view_show("INVOKE_DEFAULT")

    # Change area type
    area = bpy.context.window_manager.windows[-1].screen.areas[0]
    if selArea == "IMAGE_EDITOR" :
        area.ui_type('UV')


    else:
         area.type = selArea

    # Restore scene settings
    # render.resolution_x = original_value
    # etc.


classes = (
    Popup_View3D,
    Popup_UV,
    Popup_Shader,
    Popup_Layout,
    TOPBAR_HT_popup_editor,
    )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
   for cls in classes:
        bpy.utils.unregister_class(cls)
        print("GoodBye")

if __name__ == "__main__":
    register()
