import maya.cmds as cmds

#importing regex 29/10/25
import re

#Don't use Caps at start for some reason
windowName = 'Simple Renamer Tool'

if cmds.window(windowName, exists=True):
    print('exists')
    cmds.deleteUI(windowName)
    cmds.windowPref(windowName, remove=True)

    

window = cmds.window(windowName, resizeToFitChildren=True, sizeable=True, widthHeight=(300,200))
cmds.columnLayout(adjustableColumn=False, rowSpacing=100)
form = cmds.formLayout()


row1 = cmds.rowLayout(numberOfColumns=3, columnWidth=(120, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachForm = [(row1, 'top', 10), (row1, 'left', 15)])

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
        cmds.textField(ObjFind, edit=True, text="")


cmds.button("Find all name:", command=findName, w=125)
ObjFind = cmds.textField(w=150)


cmds.setParent('..')


subRow = cmds.rowLayout(numberOfColumns=1, columnWidth=(160, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachControl = [(subRow,'top', 15, row1)], attachForm =[(subRow, 'left', 15)])

def bringOriginName(*args):
    selected = cmds.ls(selection=True, type='transform')
    for obj in selected:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=False) or []
        if shapes:
            shape = shapes[0]
            base = shape.replace('Shape', '')
            cmds.rename(obj, base)

cmds.button(label='Clear', command=bringOriginName)
cmds.setParent('..')

row2 = cmds.rowLayout(numberOfColumns=3, columnWidth=(160, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachControl = [(row2,'top', 10, row1)], attachForm =[(row2, 'left', 15)])

#Replacing the Name
def rename(*args):
    ObjRename = cmds.textField(ObjNewName, query=True, text=True)
    selected = cmds.ls(selection=True, type= 'transform')
    for i, obj in enumerate(selected, start=1):
        if len(selected) == 1:
            newName = cmds.rename(obj, ObjRename, ignoreShape=True) 
        else:
            newName = cmds.rename(obj, f"{ObjRename}_{i:02d}")
            print(f"Renamed: {obj} to {newName}")


cmds.button("Replace Selected with:", command=rename)
ObjNewName = cmds.textField(w=150)
cmds.iconTextButton(style='iconOnly', image1='Erase.png', ann= "Clear Text Box", command=lambda *_: cmds.textField(ObjNewName, edit=True, text=''))
cmds.setParent('..')
    

row3 = cmds.rowLayout(numberOfColumns=1, columnWidth=(160, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachControl = [(row3,'top', 10, row2)], attachForm =[(row3, 'left', 16)])

#Deleting the "pasted__"
def deletePaste(*args):
    pasted = cmds.ls('pasted__*', type = 'transform')
    if pasted:
        cmds.select(pasted)
    for obj in pasted:
        clearPaste = obj.replace('pasted__', '', 1)
        cmds.rename(obj, clearPaste)
        print("Removed all pasted__")

cmds.button("Remove 'pasted__'", w=440, command=deletePaste, h= 35)
cmds.setParent('..')


#Adding Prefixes and Suffixes
row4 = cmds.rowLayout(numberOfColumns=6, columnWidth=(160, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachControl = [(row4,'top', 10, row3)], attachForm =[(row4, 'left', 30)])
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


#Removes all duplicated/ empty underscores, unsure how to delete custom words behind or infront of it
subRow2 = cmds.rowLayout(numberOfColumns=1, columnWidth=(160, 200), adjustableColumn=2)
cmds.formLayout(form, edit = True, attachControl = [(subRow2,'top', 15, row4)], attachForm =[(subRow2, 'left', 15)])

'''
def clearDupeUnderscores(*args):
    selected = cmds.ls(selection=True, type = 'transform')
    for obj in selected:                                        #Normal method (Not regex)
        clearUnderscore = obj.strip('__')
        cmds.rename(obj, clearUnderscore)
'''

def cleanUnderscore(*args):
    selected = cmds.ls(type='transform')
    for obj in selected:
        if cmds.lockNode(obj, query=True, lock=True)[0] or obj in ['persp', 'top', 'front', 'side']:
            continue
        cleanUnderscores = re.sub(r'_+','_', obj)
        cleanUnderscores = re.sub(r'^_+|_+$', '', cleanUnderscores)
        cmds.rename(obj, cleanUnderscores)


cmds.button(label='Remove all duplicated Underscores (___)', w= 440, h=30, command = cleanUnderscore, ann= "Removes all duplicated underscores next to each other leaving at least 1")
cmds.setParent('..')

#Adding a selector for object type and sub-types

row5 = cmds.rowLayout(numberOfColumns=3, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(row5,'top', 60, row4)], attachForm =[(row5, 'left', 10)])

#Option 1 would be to select geometry & sub_types
def option1(selection):
    none = cmds.select(clear=True)
    geometry_child = cmds.ls(type='mesh')
    nurbs_child = cmds.ls(type='nurbsSurface')
    curves_child = cmds.ls(type='nurbsCurve')
    
    geometry = cmds.listRelatives(geometry_child, parent=True, fullPath=False) or []
    nurbs = cmds.listRelatives(nurbs_child, parent=True, fullPath=False) or []
    curves = cmds.listRelatives(curves_child, parent=True, fullPath=False) or []
#^^^Brings the shape nodes back to the transform nodes (Needed for the Revert function on line 36)^^^

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
cmds.formLayout(form, edit = True, attachControl = [(row6,'top', 10, row5)], attachForm =[(row6, 'left', 18)])

def autoSuffix(*args):
    geo = cmds.ls(type='mesh')
    nurbs = cmds.ls(type='nurbsSurface')
    curves = cmds.ls(type='nurbsCurve')
    lights = cmds.ls(type='light')
    geometry = list(set(cmds.listRelatives(geo, parent=True, fullPath=False) or []))
    nurbsSurf = list(set(cmds.listRelatives(nurbs, parent=True, fullPath=False) or []))
    nurbsCurve = list(set(cmds.listRelatives(curves, parent=True, fullPath=False) or []))
    lightings = list(set(cmds.listRelatives(lights, parent=True, fullPath=False) or []))    # Using an empty list if list relatives gives nothing
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


#Adding Positions Macros for Models

row7 = cmds.rowLayout(numberOfColumns=2, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(row7,'top', 10, row6)], attachForm =[(row7, 'left', 200)])

#Uses of class
class prefixButton():
    def __init__(self, label):
        self.prefix = label
        self.name = cmds.button(label, w=50, h=50, command = self.addPrefix)

    def addPrefix(self, *args):
        selected = cmds.ls(selection=True)
        for obj in selected:
            if not obj.startswith(self.prefix):
                addLeft = f"{self.prefix}{obj}"
                cmds.rename(obj, addLeft)

prefixButton('top_')
cmds.setParent('..')

row8 = cmds.rowLayout(numberOfColumns=11, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(row8,'top', 5, row7)], attachForm =[(row8, 'left', 200)])



prefixButton('upp_')
cmds.setParent('..')

row9 = cmds.rowLayout(numberOfColumns=15, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(row9,'top', 5, row8)], attachForm =[(row9, 'left', 23)])

prefixButton('L_')
cmds.separator(width=5, style='none')
prefixButton('fnt_')
cmds.separator(width=5, style='none')
prefixButton('int_')
cmds.separator(width=5, style='none')
prefixButton('cntr_')
cmds.separator(width=5, style='none')
prefixButton('ext_')
cmds.separator(width=5, style='none')
prefixButton('bck_')
cmds.separator(width=5, style='none')
prefixButton('R_')
cmds.setParent('..')


row10 = cmds.rowLayout(numberOfColumns=11, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(row10,'top', 5, row9)], attachForm =[(row10, 'left', 200)])

prefixButton('lwr_')
cmds.setParent('..')

row11 = cmds.rowLayout(numberOfColumns=2, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(row11,'top', 5, row10)], attachForm =[(row11, 'left', 200)])

prefixButton('btm_')

def removePosSuffix(*args):

    top = cmds.ls('*top_*', type= 'transform')
    if top:
        cmds.select(top)
        for obj in top:
            clearTop = obj.replace('top_', '', 1)
            cmds.rename(obj, clearTop)

    upper = cmds.ls('*upp_*', type= 'transform')
    if upper:
        cmds.select(upper)
        for obj in upper:
            clearUpper = obj.replace('upp_', '', 1)
            cmds.rename(obj, clearUpper)

    left = cmds.ls('*L_*', type='transform')
    if left:
        cmds.select(left)
    for obj in left:
        clearLeft = obj.replace('L_', '', 1)
        cmds.rename(obj, clearLeft)
    
    front = cmds.ls('*fnt_*', type= 'transform')
    if front:
        cmds.select(front)
        for obj in front:
            clearFront = obj.replace('fnt_', '', 1)
            cmds.rename(obj, clearFront)
    
    interior = cmds.ls('*int_*', type= 'transform')
    if interior:
        cmds.select(interior)
        for obj in interior:
            clearInt = obj.replace('int_', '', 1)
            cmds.rename(obj, clearInt)
    
    center = cmds.ls('*cntr_*', type= 'transform')
    if center:
        cmds.select(center)
        for obj in center:
            clearCent = obj.replace('cntr_', '', 1)
            cmds.rename(obj, clearCent)

    exterior = cmds.ls('*ext_*', type= 'transform')
    if exterior:
        cmds.select(exterior)
        for obj in exterior:
            clearExt = obj.replace('ext_', '', 1)
            cmds.rename(obj, clearExt)

    back = cmds.ls('*bck_*', type= 'transform')
    if back:
        cmds.select(back)
        for obj in back:
            clearBack = obj.replace('bck_', '', 1)
            cmds.rename(obj, clearBack)

    right = cmds.ls('*R_*', type= 'transform')
    if right:
        cmds.select(right)
        for obj in right:
            clearRight = obj.replace('R_', '', 1)
            cmds.rename(obj, clearRight)

    lower = cmds.ls('*lwr_*', type= 'transform')
    if lower:
        cmds.select(lower)
        for obj in lower:
            clearLower = obj.replace('lwr_', '', 1)
            cmds.rename(obj, clearLower)

    bottom = cmds.ls('*btm_*', type= 'transform')
    if bottom:
        cmds.select(bottom)
        for obj in bottom:
            clearBottom = obj.replace('btm_', '', 1)
            cmds.rename(obj, clearBottom)

cmds.setParent('..')

subRow11 = cmds.rowLayout(numberOfColumns=2, columnWidth=(160, 200), adjustableColumn=True)
cmds.formLayout(form, edit = True, attachControl = [(subRow11,'top', 30, row6)], attachForm =[(subRow11, 'left', 25)])

cmds.button('Delete All Position Prefixes', command = removePosSuffix, w= 155, h= 55)
cmds.setParent('..')





cmds.showWindow()


