import maya.cmds as cmds

#Don't use Caps at start for some reason
windowName = 'Simple Renamer Tool'

if cmds.window(windowName, exists=True):
    print('exists')
    cmds.deleteUI(windowName)
    cmds.windowPref(windowName, remove=True)

    

window = cmds.window(windowName, resizeToFitChildren=True, sizeable=True, widthHeight=(300,200))
cmds.columnLayout(adjustableColumn=False, rowSpacing=100)
form = cmds.formLayout()


row1 = cmds.rowLayout(numberOfColumns=2, columnWidth=(120, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachForm = [(row1, 'top', 10)])

#Finding the Name
def findName(*args):
    #print(f"text field = {ObjFind}")
    ObjName = cmds.textField(ObjFind, query=True, text=True).lower()
    #print(f"input = {ObjName}")
    allObj = cmds.ls(type = 'transform')
    matched = [obj for obj in allObj if ObjName in obj.lower() and obj not in ['persp', 'top', 'front', 'side'] and not cmds.lockNode(obj,query=True, lock=True)[0]]
    #print(matched)
    if matched:
        cmds.select(matched)
    else:
        cmds.warning(f"Object '{ObjName}' does not exist")
    cmds.textField(ObjFind, edit=True, text="")

cmds.button("Find all named:", command=findName, w=125)
ObjFind = cmds.textField(w=150)
cmds.setParent('..')



row2 = cmds.rowLayout(numberOfColumns=2, columnWidth=(160, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachControl = [(row2,'top', 10, row1)], attachForm =[(row2, 'left', 0)])

#Replacing the Name
def rename(*args):
    ObjRename = cmds.textField(ObjNewName, query=True, text=True)
    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning("No Objects to be renamed")
        return
    if not ObjRename.strip():
        cmds.warning("Enter a new name")
        return
    for i, obj in enumerate(selected, start=1):
        if len(selected) == 1:
            newName = cmds.rename(obj, ObjRename)
        else:
            newName = cmds.rename(obj, f"{ObjRename}_{i:02d}")
            print(f"Renamed: {obj} to {newName}")
    cmds.textField(ObjNewName, edit=True, text="")

cmds.button("Replace Selected with:", command=rename)
ObjNewName = cmds.textField(w=150)
cmds.setParent('..')
    

row3 = cmds.rowLayout(numberOfColumns=1, columnWidth=(160, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachControl = [(row3,'top', 45, row1)], attachForm =[(row3, 'left', 0)])

#Deleting the "pasted__"
def deletePaste(*args):
    pasted = cmds.ls('pasted__*', type = 'transform')
    if pasted:
        cmds.select(pasted)
    for obj in pasted:
        clearPaste = obj.replace('pasted__', '', 1)
        cmds.rename(obj, clearPaste)
        print("Removed all pasted__")

cmds.button("Remove 'pasted__'", w=400, command=deletePaste)
cmds.setParent('..')

cmds.showWindow()


#Adding Prefixes and Suffixes
row4 = cmds.rowLayout(numberOfColumns=5, columnWidth=(160, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachControl = [(row4,'top', 80, row1)], attachForm =[(row4, 'left', 0)])
cmds.button(label="Add prefix__:", command=lambda *args:addPrefix())
prefixBox = cmds.textField()
cmds.text(label="(Object)", w=50, backgroundColor=(0.3,0.3,0.3), font="boldLabelFont", ann="Your Selected Object")
suffixBox = cmds.textField()
cmds.button(label="Add :__suffix", command=lambda *args:addSuffix())
cmds.setParent('..')

def addPrefix(*args):
    prefix = cmds.textField(prefixBox, query=True, text=True)
    selected = cmds.ls(selection=True)
    for obj in selected:
        cmds.rename(obj, f"{prefix}_{obj}")
    cmds.textField(prefixBox, edit=True, text="")

def addSuffix(*args):
    suffix = cmds.textField(suffixBox, query=True, text=True)
    selected = cmds.ls(selection=True)
    for obj in selected:
        cmds.rename(obj, f"{obj}_{suffix}")
    cmds.textField(suffixBox, edit=True, text="")


#Adding a selector for object type and sub-types

row5 = cmds.rowLayout(numberOfColumns=3, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(row5,'top', 115, row1)], attachForm =[(row5, 'left', 0)])

#Option 1 would be geometry & sub_types
def option1(selection):
    none = cmds.select(clear=True)
    geometry = cmds.ls(type='mesh')
    nurbs = cmds.ls(type='nurbsSurface')
    curves = cmds.ls(type='nurbsCurve')
    if selection == "NONE":
        cmds.select(none)
    elif selection == "GEO":
        cmds.select(geometry)
    elif selection == "NURBS":
        
        cmds.select(nurbs)
    elif selection == "CURVES":
        cmds.select(curves)

#Option 2 is for lights because they all have different type names
def option2(selection):
    cmds.select(clear=True)
    amLight = cmds.ls(type='ambientLight')
    dLight = cmds.ls(type='directionalLight')
    pLight = cmds.ls(exactType='pointLight') #named it "exactType" because for some reason pointlight is the parent of volumelight
    sLight = cmds.ls(type='spotLight')
    arLight = cmds.ls(type ='areaLight')
    vLight = cmds.ls(type = 'volumeLight')
    if selection == "Ambient Light":
        cmds.select(amLight)
    elif selection == "Directional Light":
        cmds.select(dLight)
    elif selection == "Point Light":
        cmds.select(pLight)
    elif selection == "Spot Light":
        cmds.select(sLight)
    elif selection == "Area Light":
        cmds.select(arLight)
    elif selection == "Volume Light":
        cmds.select(vLight)


cmds.optionMenu(label="Select Geo sub-type:", changeCommand=option1)
cmds.menuItem(label="NONE")
cmds.menuItem(label="GEO")
cmds.menuItem(label="NURBS")
cmds.menuItem(label="CURVES")

cmds.separator(width=5, style='none')

cmds.optionMenu(label="Select Light sub-type:", changeCommand=option2)
cmds.menuItem(label="NONE")
cmds.menuItem(label="Ambient Light")
cmds.menuItem(label="Directional Light")
cmds.menuItem(label="Point Light")
cmds.menuItem(label="Spot Light")
cmds.menuItem(label="Area Light")
cmds.menuItem(label="Volume Light")
cmds.setParent('..')


#Auto Apply Identity Suffixes 
row6 = cmds.rowLayout(numberOfColumns=3, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(row6,'top', 155, row1)], attachForm =[(row6, 'left', 0)])

def autoSuffix(*args):
    geo = cmds.ls(type='mesh')
    nurbs = cmds.ls(type='nurbsSurface')
    curves = cmds.ls(type='nurbsCurve')
    lights = cmds.ls(type='light')
    geometry = list(set(cmds.listRelatives(geo, parent=True, fullPath=False)))
    nurbsSurf = list(set(cmds.listRelatives(nurbs, parent=True, fullPath=False)))
    nurbsCurve = list(set(cmds.listRelatives(curves, parent=True, fullPath=False)))
    lightings = list(set(cmds.listRelatives(lights, parent=True, fullPath=False)))
    for obj in geometry:
        if not obj.endswith("_GEO"):
            addGeo = f"{obj}_GEO"
            cmds.rename(obj, addGeo)
    for obj in nurbsSurf:
        if not obj.endswith("_NURBS"):
            addNurbs = f"{obj}_NURBS"
            cmds.rename(obj, addNurbs)
    for obj in nurbsCurve:
        if not obj.endswith("_CRV"):
            addCurve = f"{obj}_CRV"
            cmds.rename(obj, addCurve)
    for obj in lightings:
        if not obj.endswith("_LIGHT"):
            addLight = f"{obj}_LIGHT"
            cmds.rename(obj, addLight)

def removeSuffix(*args):
    geo = cmds.ls('*_GEO', type='transform')
    if geo:
        cmds.select(geo)
    for obj in geo:
        clearGeo = obj.replace('_GEO', '', 1)
        cmds.rename(obj, clearGeo)

    nurbs = cmds.ls('*_NURBS', type='transform')
    if nurbs:
        cmds.select(nurbs)
    for obj in nurbs:
        clearNurbs = obj.replace('_NURBS', '', 1)
        cmds.rename(obj, clearNurbs)

    curves = cmds.ls('*_CRV', type='transform')
    if curves:
        cmds.select(curves)
    for obj in curves:
        clearCurves = obj.replace('_CRV', '', 1)
        cmds.rename(obj, clearCurves)

    lights = cmds.ls('*_LIGHT', type='transform')
    if lights:
        cmds.select(lights)
    for obj in lights:
        clearLight = obj.replace('_LIGHT', '', 1)
        cmds.rename(obj, clearLight)
    cmds.select(clear=True)




cmds.button("Add Naming Type Suffixes",command=autoSuffix, w=200, h=50, ann= "Adds all Naming Conventions Type" )
cmds.separator(width=5, style='none')
cmds.button("Remove Naming Type Suffixes", command = removeSuffix, w=200, h=50, ann= "Removes all Naming Conventions Type")
cmds.setParent('..')

cmds.showWindow()


