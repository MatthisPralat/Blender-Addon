'''

Init Interface for Material Utils 

'''

import bpy

# Local imports ---------
from . import material_utils_global_variable

# VARIABLES ----- 

# Initialisation  of  materials utils ui
MatToReplace = material_utils_global_variable.allMaterials
MaterialToReplace = material_utils_global_variable.allMaterials
LinkedLibrary = material_utils_global_variable.LinkedLibrary
MaterialFaceSelect = material_utils_global_variable.allMaterials


#------------------------------
# CLASSES
#------------------------------

# PANELS ----- 

# Main ui
class MaterialUtilsPanel(bpy.types.Panel):
    
    bl_label = "Material utils panel"
    bl_idname = "MATERIAL_UTILS_PANEL_PT_VIEW3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Materials utils"

    def draw(self, context):
        
        layout = self.layout
        # --- MATERIAL REPLACE  PROPERTY GROUP
        props = context.scene.MaterialReplacePropertyGroup

        #--
        layout.label(text="Material Replace")
        
        box = layout.box() #----------------- box 
    
        row = box.row()
        #---
        row = box.row()
        row.prop(props, "MaterialReplace")
        row = box.row()
        row.prop(props, "MaterialToReplace")
        # --- MATERIAL REPLACE OPERATOR
        row = box.row()
        row.operator("material_utilities.replace_materials")
        
        # --- MATERIAL LINK REPLACE
        row = layout.row()
        layout.label(text="Quick Link materials replace ")

        box = layout.box()   #----------------- box 
        row = box.row()
        row.operator("material_utilities.replace_material_by_linked_materials")
      
        # --- ADVANCED MATERIAL LINK REPLACE
        layout.label(text="Link Material Replace")
        box = layout.box()   #----------------- box 
        row = box.row()
        row.prop(props, "LinkedLibrary")
        row = box.row()
        row.operator("material_utilities.replace_material_linked_advanced")
        
        # --- CLEANING MATERIALS
        row = layout.row()
        layout.label(text="Cleaning materials")
        box = layout.box()   #----------------- box 

        #--   ITERATIVE MATERIAL REPLACE OPERATOR
        row = box.row()
        row.operator("material_utilities.replace_iterative_materials")

        #--   ITERATIVE MATERIAL REPLACE OPERATOR
        row = box.row()
        row.operator("material_utilities.remove_unused_materials")

        #-- Clean Materials Slots
        row = box.row()
        row.operator("material_utilities.clean_materials_slots")

        # --- Material selection
        row = layout.row()
        layout.label(text="Material selection")
        box = layout.box()  # ----------------- box
        row = box.row()
        row.prop(props, "MaterialFaceSelect")
        row = box.row()
        row.operator("material_utilities.select_face_by_material")
       
        # --- BackFace/UnbackFace All Material
        #--
        row = layout.row()
        layout.label(text="Backfaces")
        box = layout.box()   #----------------- box 
        #--
        row = box.row()
        row.operator("material_utilities.backface_materials")
        #--
        row = box.row()
        row.operator("material_utilities.no_backface_materials")


# -- PROPERTY GROUP ------

# initialisation class for  Material Replace
class MaterialReplacePropertyGroup( bpy.types.PropertyGroup ): 
    # Init Linked Library Update
    LinkedLibrary : bpy.props.EnumProperty(items=LinkedLibrary) # the same 
    # Init Updated Material Properties
    MaterialReplace : bpy.props.EnumProperty(items=MatToReplace) # Enum of all Materials on the scene
    MaterialToReplace : bpy.props.EnumProperty(items=MaterialToReplace) # the same
    MaterialFaceSelect : bpy.props.EnumProperty(items=MaterialFaceSelect) # the same


#------------------------------
# REGISTER / UNREGISTER / INIT
#------------------------------

classes = [ 
    MaterialReplacePropertyGroup,
    MaterialUtilsPanel,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.MaterialReplacePropertyGroup = bpy.props.PointerProperty(type=MaterialReplacePropertyGroup)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.MaterialReplacePropertyGroup

if __name__ == "__main__":
    register()