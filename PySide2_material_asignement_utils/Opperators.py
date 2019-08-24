# by matthis pralat, matthispralat.fr
# with the help of Legigan Jeremy aka Pistiwique
# And s-Leger from Archipack
# thanks to blender lounge community

import bpy

# ----------------------------------------------------------
# OPERATORS
# ----------------------------------------------------------

# mat.001 to mat
class Replace_Itterative_Materials(bpy.types.Operator):
    """
        Replace YourMats.001 by YourMats if YourMatExist
        !-- Warning --!
            Be sure to have a good naming convention will replace all
        basename.xxx if basename is found
    """

    bl_idname = "material_utilities_ps2.replace_iterative_materials"
    bl_label = " !- Itterative materials replace -! "

    def execute(self, context):

        duplicateMaterials = 0

        for mat in bpy.data.materials:
            name = mat.name  # exemple : material.001
            baseName = name[:-4]  # = material
            Point = name[-4]  # = .
            iterationName = name[-3:]  # = 001

            if iterationName.isdigit() == True:
                if Point == ".":
                    if bpy.data.materials[baseName] is not None:
                        MATERIAL_REPLACE(name, baseName)
                        duplicateMaterials = duplicateMaterials + 1

        print("found", duplicateMaterials, "materials")
        return {'FINISHED'}

# Delete unused materials
class Remove_Unused_Materials(bpy.types.Operator):
    """  Remove unused materials without reloading blend file """

    bl_idname = "material_utilities_ps2.remove_unused_materials"
    bl_label = " Remove unused materials"

    def execute(self, context):
        for material in bpy.data.materials:
            if not material.users:
                bpy.data.materials.remove(material)
        return {'FINISHED'}

    import bpy

# Clear mat slot
class MaterialSlotsClean(bpy.types.Operator):
    """  Clear unused materials slots
         1 - Check if double mat
         2 - Reasign Double mat
         3 - Clean unused materials slots
    """

    bl_idname = "material_utilities_ps2.clean_materials_slots"
    bl_label = "Clean material slots"

    def execute(self, context):
        for obj in bpy.data.objects:
            Mslots_doubles(obj)
            clearUnusedMatSlot(obj)
        return {'FINISHED'}

# ----------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------
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

def clearUnusedMatSlot(obj):
    i = 0
    rMatslots = {}
    matslots = {}

    if len(obj.material_slots) > 0:

        # first loop for material slots
        for mats in obj.material_slots:
            matslots.update({str(i): str(mats.name)})
            i = i + 1

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
            ctx = bpy.context.copy()
            ctx['object'] = obj
            # delete operator
            bpy.ops.object.material_slot_remove(ctx)


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
                Context_Doubles_M.update({i: Context_M[name]})

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

classes = [
    Replace_Itterative_Materials,
    Remove_Unused_Materials,
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