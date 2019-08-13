# standard library import ---------
import bpy
# Local imports ---------
from . import material_utils_global_variable

# VARIABLES ----- 
MatToReplace = material_utils_global_variable.allMaterials
MaterialToReplace = material_utils_global_variable.allMaterials

# CLASSES --------
class MaterialUtilsPanel(bpy.types.Panel):
    
    bl_label = "Material utils panel"
    bl_idname = "MATERIAL_UTILS_PANEL_PT_VIEW3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Materials utils"

    def draw(self, context):
        
        layout = self.layout
        props = context.scene.MaterialReplacePropertyGroup
        #--
        row = layout.row()
        layout.label(text="Material Replace")
        #---
        row = layout.row()
        row.prop(props, "MaterialReplace")
        row = layout.row()
        row.prop(props, "MaterialToReplace")
        #--
        row = layout.row()
        row.operator("material_utilities.replace_materials")
        #--

# Property group ------
class MaterialReplacePropertyGroup( bpy.types.PropertyGroup ): #test
 
    MyBool : bpy.props.BoolProperty( 
        name = "MyBool",
        description = " Exemple of Bool button ",
        default = False
    )

    MyInt : bpy.props.IntProperty(  
        name = "MyInt",
        description = " Exemple of int button",
        default= 0,
        min= 0,
    )
    oldStuff : bpy.props.EnumProperty(items=MatToReplace)
    MaterialReplace : bpy.props.EnumProperty(items=MatToReplace) # Enum of all Materials on the scene
    MaterialToReplace : bpy.props.EnumProperty(items=MaterialToReplace) # the same 


# OPERATORS --------
class Replace_Materials(bpy.types.Operator):
    """ 
        Get MaterialToReplace and for each materials 
        who get this materials replace it by
        The material setted in MaterialReplace
    """

    bl_idname = "material_utilities.replace_materials"
    bl_label = "Material replace"

    def execute(self, context):
        props = context.scene.MaterialReplacePropertyGroup
        print(props.MaterialReplace)
        MATERIAL_REPLACE(props.MaterialToReplace,props.MaterialReplace)
        UpdateDespGraph()
        return {'FINISHED'}

# FONCTIONS --------

    # create and delete a data block to update despgraph
    # And Keep actual selection
def UpdateDespGraph():
  
    Item = []
   
    for obj in bpy.context.selected_objects:
        Item.append( str(obj.name) )

    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.object.delete() 

    for key in Item :
        bpy.data.objects[key].select_set(True)

    # Replace all materials mtr by mr 
def MATERIAL_REPLACE(mtr, mr):
    
    objects = bpy.context.scene.objects

    for obj in objects:
        if obj.type == "MESH":
            i = -1
            for mat in obj.data.materials:
                i = i + 1
                if mat.name == str(mtr):
                    obj.data.materials[i] = bpy.data.materials[str(mr)]

# Update Materials Utils Pannel if Mat change
def UpdateProperty():
 
    # Get mat
    AllMaterials = bpy.data.materials
    AllMat = [(mat.name, mat.name, mat.name) for mat in AllMaterials] 

    # Class replace
    class MaterialReplacePropertyGroup(bpy.types.PropertyGroup):

        MyBool : bpy.props.BoolProperty( 
            name = "MyBool",
            description = " Exemple of Bool button ",
            default = False
        )

        MyInt : bpy.props.IntProperty(  
            name = "MyInt",
            description = " Exemple of int button",
            default= 0,
            min= 0,
        )

        MaterialToReplace : bpy.props.EnumProperty(items=AllMat)
        MaterialReplace : bpy.props.EnumProperty(items=AllMat)
    
    # Reload Class and property Class
    bpy.utils.register_class(MaterialReplacePropertyGroup)
    bpy.types.Scene.MaterialReplacePropertyGroup = bpy.props.PointerProperty(
            type=MaterialReplacePropertyGroup)
    
    # Set Num in Glogal
    material_utils_global_variable.materialNum = len(bpy.data.materials) 



# EXECUTION -------

classes = [ 
    MaterialReplacePropertyGroup,
    Replace_Materials,
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