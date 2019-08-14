'''

Global varialble, readable everywhere if we use 
from . import materials_utils_global_variable 
in this folder 
or
from material_asignement_utils import materials_utils_global_variable 
in another add-on or file or script.

'''
# standard library import ---------
import bpy

init = False # first launch
materialNum = 0 # current material number in the scene
allMaterials =  [('none','none','none')] # init Enum Property