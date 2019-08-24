# PYSIDE 2 Exemple 
with materials utils
Quick and dirty documentation

![](https://raw.githubusercontent.com/MatthisPralat/Blender-Addon/master/PySide2_material_asignement_utils/PySide2_documentation_Img/PySide2_Exemple.gif)

This is an integration of PySide2 in blender with button interactions with the Blender Editor. 
It's a quick and dirty integration ! just for the proof and concept


## Install Pip

To use PySide2 you must install pip and PySide2, on windows. I made a button to do that automaticly, and now you can even install your favorite modules from pip inside blender !
! open the console to watch the instalation of pip and PySide2 in **Window > Toogle System Console** > ! or make you a cofee and wait 5 minutes.

If pip and pyside2 are installed, pip instalation will be hiden
![](https://raw.githubusercontent.com/MatthisPralat/Blender-Addon/master/PySide2_material_asignement_utils/PySide2_documentation_Img/PysidePannel.PNG)


## QT designer interface

the interface is made with QT designer. You can find it in your PySide2 folder inside your blender instalation file 
...\Blender\2.80\python\lib\site-packages\PySide2

![](https://raw.githubusercontent.com/MatthisPralat/Blender-Addon/master/PySide2_material_asignement_utils/PySide2_documentation_Img/PyQt_Sample.PNG)


## QSS styleShett

You can customise your window style with Qss file, you can find samples in the style sheet folder inside this package
![](https://raw.githubusercontent.com/MatthisPralat/Blender-Addon/master/PySide2_material_asignement_utils/PySide2_documentation_Img/PySidePopUp_Styling.PNG)

## Example Buttons

**Itterative material replace**

if your importing multiples fbx with the same materials name this button can save time.

! warning : Be sur to have a good naming convention. 

replace each **material.xxx** iteration by **material** if it exists.

for exemple : all your object with materials named **yourMaterial.001 yourMaterial.002 yourMaterial.003** will be remplaced by **yourMaterial**
if yourMaterial exist.

![](http://www.matthispralat.fr/wp-content/uploads/2019/MaterialReplace/Itterative_Material_Replace.gif)

**Remove unused materials**

Clean up unused materials without reloading blender. 

![](http://www.matthispralat.fr/wp-content/uploads/2019/MaterialReplace/Remove_Unused_Materials.gif)

**Clean Material Slots**

 for each object Remap materials duplicates and remove unused materials slots

![](http://www.matthispralat.fr/wp-content/uploads/2019/MaterialReplace/CleanMaterialSlots.gif)

## Create Suzanne
Create a a Suzanne mesh
