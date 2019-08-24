'''

Script for Selecting a material 
and replace it by another 

'''
# standard library import ---------
import bpy
# Local imports ---------
from . import material_utils_global_variable

# CLASSES --------


# -- operators ------

# Replace MaterialToreplace by MaterialReplace 
class Replace_Materials(bpy.types.Operator):
    """  Replace all materials setted in MaterialToReplace 
         by the setted material in material replace
    """

    bl_idname = "material_utilities.replace_materials"
    bl_label = "Material replace"

    def execute(self, context):
        props = context.scene.MaterialReplacePropertyGroup # Get Mtr & Mr Prop 
        MATERIAL_REPLACE(props.MaterialToReplace,props.MaterialReplace)
        UpdateDespGraph()
        return {'FINISHED'}

# replace materials xxx.00x by xxx
class Replace_Itterative_Materials(bpy.types.Operator):
    """  
        Replace YourMats.001 by YourMats if YourMatExist
        !-- Warning --!
            Be sure to have a good naming convention will replace all
        basename.xxx if basename is found
    """

    bl_idname = "material_utilities.replace_iterative_materials"
    bl_label = " !- Itterative materials replace -! "

    def execute(self, context):
       
        duplicateMaterials = 0

        for mat in bpy.data.materials:
            name = mat.name #exemple : material.001
            baseName = name[:-4] # = material
            Point = name[-4] # = .
            iterationName = name[-3:] # = 001

            if iterationName.isdigit() == True :
                if Point == ".":
                    if bpy.data.materials[baseName] is not None:
                        MATERIAL_REPLACE(name,baseName)
                        duplicateMaterials = duplicateMaterials + 1
                    
        print("found",duplicateMaterials,"materials")
        UpdateDespGraph()
        return {'FINISHED'}

# Replace Material by Last found Linked materials
class Replace_Materials_By_MaterialLinked(bpy.types.Operator):
    """  Replace materials by linked materials if found """

    bl_idname = "material_utilities.replace_material_by_linked_materials"
    bl_label =  "Linked materials Replace"

    def execute(self, context):
        LinkedMatIndex = 0
        for mat in bpy.data.materials:
            matname = str(mat.name)
            if mat.library is not None:
                print('linked')
                if bpy.data.materials[matname] is not None :
                    if bpy.data.materials[matname].library is None :
                        replaceMatByLinkedMat( LinkedMatIndex , matname )
            LinkedMatIndex = LinkedMatIndex+1
        
        UpdateDespGraph()
        return {'FINISHED'}

# Replace mat by specified link library
class Replace_Materials_Linked_Advanced(bpy.types.Operator):
    """  Replace materials by linked materials in specified link if found """

    bl_idname = "material_utilities.replace_material_linked_advanced"
    bl_label =  "Linked materials Replace"

    def execute(self, context):
        print("hello")
        props = context.scene.MaterialReplacePropertyGroup # Get LinkedLibrary
        
        LinkedMatIndex = 0
        print(props.LinkedLibrary)
       
        for mat in bpy.data.materials:
            matname = str(mat.name)
            if mat.library is not None:
                print('linked')
                if bpy.data.materials[matname] is not None :
                    if str(mat.library.name) == str(props.LinkedLibrary):
                        replaceMatByLinkedMat( LinkedMatIndex , matname )
            LinkedMatIndex = LinkedMatIndex+1
        UpdateDespGraph()
        return {'FINISHED'}
        
# Delete unused materials
class Remove_Unused_Materials(bpy.types.Operator):
    """  Remove unused materials without reloading blend file """

    bl_idname = "material_utilities.remove_unused_materials"
    bl_label = " Remove unused materials"

    def execute(self, context):
        for material in bpy.data.materials:
            if not material.users:
                bpy.data.materials.remove(material)
        UpdateDespGraph()
        return {'FINISHED'}

    import bpy



# Activate Backface on all materials 
class Backface_Material(bpy.types.Operator):
    """ 
        Set Backface boolean for all materials
    """

    bl_idname = "material_utilities.backface_materials"
    bl_label = " Backface All Mats "

    def execute(self, context):
        for mat in bpy.data.materials:
            mat.use_backface_culling = True

        return {'FINISHED'}
        
class NoBackface_Material(bpy.types.Operator):
    """  Unset Backface boolean for all materials """

    bl_idname = "material_utilities.no_backface_materials"
    bl_label = "No Backface All Mats "

    def execute(self, context):
        for mat in bpy.data.materials:
            mat.use_backface_culling = False

        return {'FINISHED'}

class MaterialSlotsClean(bpy.types.Operator):
    """  Clear unused materials slots 
         1 - Check if double mat
         2 - Reasign Double mat
         3 - Clean unused materials slots  
    """

    bl_idname = "material_utilities.clean_materials_slots"
    bl_label = "Clean material slots"

    def execute(self, context):
        for obj in bpy.data.objects:
            Mslots_doubles(obj)
            clearUnusedMatSlot(obj)
        return {'FINISHED'}

# FUNCTIONS --------

# create and delete a data block to update despgraph
# And Keep actual selection
def UpdateDespGraph():
#    if bpy.context.object.mode == 'EDIT':
#        bpy.ops.object.mode_set(mode='OBJECT')
    
    #bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.object.delete()
#Create errors sadly 
'''    Item = []
    # Get selected object
    for obj in bpy.context.selected_objects:
        Item.append( str(obj.name) )
    # Hack refresh despgraph
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.object.delete() 
    # Re-select previously selected object
    for key in Item :
        bpy.data.objects[key].select_set(True)
'''

# Replace all materials mtr by mr 
def MATERIAL_REPLACE(mtr, mr):
    #selecting all object in scene
    objects = bpy.data.objects
    # inspecting in all mats
    for obj in objects:
        if len(obj.material_slots) > 0:
            i = -1
            for mat in obj.material_slots:
                i = i + 1
                if str(mat.name) == str(mtr):
                    obj.data.materials[i] = bpy.data.materials[mr]

def replaceMatByLinkedMat( MatReplaceIndex , MatToReplaceName ):
    objects = bpy.data.objects
    for obj in objects:
        if len(obj.material_slots) > 0:
            i = -1
            for mat in obj.material_slots:
                i = i + 1
                if mat is not None:
                    if str(mat.name) == str(MatToReplaceName):
                        obj.data.materials[i] = bpy.data.materials[MatReplaceIndex] 
    print("material replaced by linked material:", MatToReplaceName )    

# Update Materials Utils Pannel if Material is added or removed
def UpdateProperty():
 
    # Get mat
    AllMaterials = bpy.data.materials
    AllMat = [(mat.name, mat.name, mat.name) for mat in AllMaterials] 
    if len(bpy.data.libraries) > 0 :
        LinkedLib = [(lib.name, lib.name, lib.name,) for lib in bpy.data.libraries]
    else:
        LinkedLib= [('none','none','none')]
    # Class replace
    class MaterialReplacePropertyGroup(bpy.types.PropertyGroup):
        # Init Linked Library Update
        LinkedLibrary : bpy.props.EnumProperty(items=LinkedLib) # the same 
        # Updated Material Properties
        MaterialToReplace : bpy.props.EnumProperty(items=AllMat)
        MaterialReplace : bpy.props.EnumProperty(items=AllMat)
    
    # Reload Class and property Class
    bpy.utils.register_class(MaterialReplacePropertyGroup)
    bpy.types.Scene.MaterialReplacePropertyGroup = bpy.props.PointerProperty(
            type=MaterialReplacePropertyGroup)
    
    # Set Num in Glogal
    material_utils_global_variable.materialNum = len(bpy.data.materials) 


# for passed objects, clear unused material slot
def clearUnusedMatSlot(obj):
    i = 0
    rMatslots ={}
    matslots = {}

    if len(obj.material_slots) > 0: 
        
        # first loop for material slots
        for mats in obj.material_slots:
            matslots.update({str(i) : str(mats.name) } )
            i= i + 1

        # Loop to know if slot mesh is used
        for face in obj.data.polygons:
            if str(face.material_index) in matslots:
                del matslots[str(face.material_index)]

        # Matslot reverse order
        rMatslots = sorted(matslots, reverse=True)

        # If index found delete Matslot
        for uMat in rMatslots:
            obj.active_material_index = int(uMat)
            # overide context
            ctx = bpy.context.copy ()
            ctx['object'] = obj
            # delete operator
            bpy.ops.object.material_slot_remove(ctx)

# Find doubles In object if found  Mslots_Reasign(obj)
def Mslots_doubles(obj):
    # set var to be read elswere
    global Context_M, Context_Doubles_M, Double
    Context_M = {}
    Context_Doubles_M = {}
    Double = False
      
    # check if obj have multiple slot
    if len(obj.material_slots) > 0:
        i = 0
        for m_slots in obj.material_slots:

            # set double index matslot and good index as value
            if m_slots.name in Context_M:
                Double = True
                name = str(m_slots.name)
                Context_Doubles_M.update({i:Context_M[name]})

            # set material name as index with the index of mat slot as value
            else:
                Context_M.update({m_slots.name: i})
            i = i + 1
    # if the mesh has double second loop 
    if Double == True:
        Mslots_reasign(obj)

def Mslots_reasign(obj):

    for face in obj.data.polygons:
        if face.material_index in Context_Doubles_M:
            face.material_index = Context_Doubles_M[face.material_index]

# EXECUTION -------

classes = [
    Replace_Materials,
    Replace_Materials_By_MaterialLinked,
    Replace_Materials_Linked_Advanced,
    Replace_Itterative_Materials,
    Remove_Unused_Materials,
    Backface_Material,
    NoBackface_Material,
    MaterialSlotsClean,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()