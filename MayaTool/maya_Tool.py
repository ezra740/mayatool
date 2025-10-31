from maya import cmds

#importing regex
import re

#All Functions
#Finding the Name
def findName(*args):
    ObjName = cmds.textField(ObjFind, query=True, text=True).lower()
    allObj = cmds.ls(type = 'transform')
    matched = []
    for obj in allObj:
               if ObjName.lower() in obj.lower(): #If Capital or lower capital
                    if obj not in ['persp', 'top', 'front', 'side']: #Make sure theyre not in the default cams
                        if not cmds.lockNode(obj, query=True, lock=True)[0]: #If object is Not locked, then it can continue
                            matched.append(obj)

    if matched:
        cmds.select(matched)
        cmds.textField(ObjFind, edit=True, text="")

#A button to bring the original names back
def bringOriginName(*args):
    selected = cmds.ls(type='transform')
    for obj in selected:
        if cmds.lockNode(obj, query=True, lock=True)[0] or obj in ['persp', 'top', 'front', 'side']: #Ignores the viewports
            continue
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=False)
        if shapes:
            shape = shapes[0]
            base = shape.replace('Shape', '') #Replaces Shape with nothing
            cmds.rename(obj, base)

#Replacing the Name
def rename(*args):
    ObjRename = cmds.textField(ObjNewName, query=True, text=True)
    selected = cmds.ls(selection=True, type= 'transform')
    for i, obj in enumerate(selected, start=1):
        if len(selected) == 1:
            newName = cmds.rename(obj, ObjRename, ignoreShape=True) 
        else:
            newName = cmds.rename(obj, f"{ObjRename}{i:01d}", ignoreShape=True)
            print(f"Renamed: {obj} to {newName}")


#Sorting the names from top to bottom by its number (using regex)
def order(*args):
    for nodeType in ['mesh', 'nurbsSurface', 'nurbsCurve', 'light']: #All nodes in 1
        node = cmds.listRelatives(cmds.ls(type=nodeType), parent=True, fullPath=False) or[] #mesh so that it can only move the polys
        node = [n for n in node if n not in ['persp', 'top', 'front', 'side'] and not cmds.lockNode(n, q=True, lock=True)[0]] #Does not reorder above the read only nodes
        node.sort(key=lambda x: (re.sub(r'\d+', '', x), int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0))
#      ^^^Removes the numbers so it can compare the objects names alphabetically. Then it uses the object's numbers to compare, lowest to highest. Then puts it together and sorts^^^ 

        for n in node:
            cmds.reorder(n, back=True)

#Deleting the "pasted__"
def deletePaste(*args):
    pasted = cmds.ls('pasted__*', type = 'transform')
    if pasted:
        cmds.select(pasted)
    for obj in pasted:
        clearPaste = obj.replace('pasted__', '', 1)
        cmds.rename(obj, clearPaste)
        print("Removed all pasted__")

#Adding Prefixes and Suffixes
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

#Adding a selector for object type and sub-types
#Option 1 would be to select what Shelf Tab is in the scene
def option1(selection):
    none = cmds.select(clear=True)
    geometryShape = cmds.ls(type='mesh')
    nurbsShape = cmds.ls(type='nurbsSurface')
    curvesShape = cmds.ls(type='nurbsCurve')
    lightsShape = cmds.ls(type='light')
    
    geometry = cmds.listRelatives(geometryShape, parent=True, fullPath=False) or []
    nurbs = cmds.listRelatives(nurbsShape, parent=True, fullPath=False) or []
    curves = cmds.listRelatives(curvesShape, parent=True, fullPath=False) or []
    lights = cmds.listRelatives(lightsShape, parent=True, fullPath=False) or []
    if selection == "NONE":
        cmds.select(none)
    elif selection == "GEO":
        cmds.select(geometry)

    elif selection == "NURBS":
        cmds.select(nurbs)

    elif selection == "CURVES":
        cmds.select(curves)

    elif selection == "LIGHTS":
        cmds.select(lights)

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

#Auto Apply Identity Suffixes 
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
        cmds.rename(obj, clearLight, ignoreShape=True)
    cmds.select(clear=True)

#Adding Positions Macros for Models
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

#Removes Positions 
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


def LaunchNonDockableWindow():
    myWindow = 'Maya_UI'
    if cmds.window(myWindow, ex=True):
        cmds.deleteUI(myWindow, window = True)

    cmds.window(myWindow, title= 'Simple Renamer Tool', resizeToFitChildren=True, sizeable=True, widthHeight=(300,200))

    
    BuildWindowUI()

    cmds.showWindow(myWindow)

def BuildWindowUI(parent = None):

    global ObjFind, prefixBox, suffixBox, ObjNewName #Temporary

    myWindow = "Renamer Window UI"
    if cmds.window(myWindow, exists=True):
        cmds.deleteUI(myWindow, window=True)

    cmds.columnLayout(adjustableColumn=False, rowSpacing=100)
    form = cmds.formLayout()


    row1 = cmds.rowLayout(numberOfColumns=4, columnWidth=(120, 200), adjustableColumn=2)
    cmds.formLayout(form, edit = True, attachForm = [(row1, 'top', 10), (row1, 'left', 15)])


    cmds.button("Find all name:", command=findName, w=125)
    ObjFind = cmds.textField(w=150)

    cmds.separator(width=45, style='none')


    cmds.button(label='Revert all names to Original', bgc=[0.7,0.2,0.2], command=bringOriginName, ann="Warning: Brings everything back to its original name. (e.g, Box --> pCube1)")
    cmds.setParent('..')

    row2 = cmds.rowLayout(numberOfColumns=6, columnWidth=(160, 200), adjustableColumn=2)
    cmds.formLayout(form, edit = True, attachControl = [(row2,'top', 10, row1)], attachForm =[(row2, 'left', 15)])


    cmds.button("Replace Selected with:", command=rename)
    ObjNewName = cmds.textField(w=150)
    cmds.iconTextButton(style='iconOnly', image1='Erase.png', ann= "Clear Text Box", command=lambda *_: cmds.textField(ObjNewName, edit=True, text=''))
    cmds.separator(w=8, style='none')


    cmds.button(label = "Reorginize Outline", w=152, command = order, ann="Reorginizes names in the outline to follow Number or Alphabetical order")
    cmds.setParent('..')
        

    row3 = cmds.rowLayout(numberOfColumns=1, columnWidth=(160, 200), adjustableColumn=2)
    cmds.formLayout(form, edit = True, attachControl = [(row3,'top', 10, row2)], attachForm =[(row3, 'left', 16)])


    cmds.button("Remove 'pasted__'", w=478, command=deletePaste, h= 35)
    cmds.setParent('..')

    row4 = cmds.rowLayout(numberOfColumns=6, columnWidth=(160, 200), adjustableColumn=2)
    cmds.formLayout(form, edit = True, attachControl = [(row4,'top', 10, row3)], attachForm =[(row4, 'left', 30)])
    cmds.button(label="Add prefix__:",w=100, command=lambda *args:addPrefix())
    prefixBox = cmds.textField()
    cmds.text(label="(Object)", w=50, backgroundColor=(0.3,0.3,0.3), font="boldLabelFont", ann="Your Selected Object")
    suffixBox = cmds.textField()
    cmds.button(label="Add :__suffix",w=100, command=lambda *args:addSuffix())
    cmds.setParent('..')


    subRow2 = cmds.rowLayout(numberOfColumns=1, columnWidth=(160, 200), adjustableColumn=2)
    cmds.formLayout(form, edit = True, attachControl = [(subRow2,'top', 15, row4)], attachForm =[(subRow2, 'left', 15)])



    cmds.button(label='Remove all duplicated Underscores ___', w= 478, h=30, command = cleanUnderscore, ann= "Removes all duplicated underscores next to each other leaving at least 1")
    cmds.setParent('..')


    row5 = cmds.rowLayout(numberOfColumns=3, columnWidth=(160, 200), adjustableColumn=True)
    cmds.formLayout(form, edit = True, attachControl = [(row5,'top', 60, row4)], attachForm =[(row5, 'left', 10)])

    cmds.optionMenu(label="Select Shelf Tab type, in Scene:", changeCommand=option1)
    cmds.menuItem(label="NONE")
    cmds.menuItem(label="GEO")
    cmds.menuItem(label="NURBS")
    cmds.menuItem(label="CURVES")
    cmds.menuItem(label="LIGHTS")

    cmds.separator(width=5, style='none')

    cmds.optionMenu(label="Select all type of Lights:", changeCommand=option2, w=240)
    cmds.menuItem(label="NONE")
    cmds.menuItem(label="Ambient Light")
    cmds.menuItem(label="Directional Light")
    cmds.menuItem(label="Point Light")
    cmds.menuItem(label="Spot Light")
    cmds.menuItem(label="Area Light")
    cmds.menuItem(label="Volume Light")
    cmds.setParent('..')


    row6 = cmds.rowLayout(numberOfColumns=3, columnWidth=(160, 200), adjustableColumn=True)
    cmds.formLayout(form, edit = True, attachControl = [(row6,'top', 10, row5)], attachForm =[(row6, 'left', 30)])




    cmds.button("Add Naming Type Suffixes",command=autoSuffix, w=220, h=50, ann= "Adds all Naming Conventions Type" )
    cmds.separator(width=5, style='none')
    cmds.button("Remove Naming Type Suffixes", command = removeSuffix, w=220, h=50, ann= "Removes all Naming Conventions Type")
    cmds.setParent('..')


    row7 = cmds.rowLayout(numberOfColumns=2, columnWidth=(160, 200), adjustableColumn=True)
    cmds.formLayout(form, edit = True, attachControl = [(row7,'top', 10, row6)], attachForm =[(row7, 'left', 230)])

    prefixButton('top_')
    cmds.setParent('..')

    row8 = cmds.rowLayout(numberOfColumns=11, columnWidth=(160, 200), adjustableColumn=True)
    cmds.formLayout(form, edit = True, attachControl = [(row8,'top', 5, row7)], attachForm =[(row8, 'left', 230)])



    prefixButton('upp_')
    cmds.setParent('..')

    row9 = cmds.rowLayout(numberOfColumns=15, columnWidth=(160, 200), adjustableColumn=True)
    cmds.formLayout(form, edit = True, attachControl = [(row9,'top', 5, row8)], attachForm =[(row9, 'left', 53)])

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
    cmds.formLayout(form, edit = True, attachControl = [(row10,'top', 5, row9)], attachForm =[(row10, 'left', 230)])

    prefixButton('lwr_')
    cmds.setParent('..')

    row11 = cmds.rowLayout(numberOfColumns=2, columnWidth=(160, 200), adjustableColumn=True)
    cmds.formLayout(form, edit = True, attachControl = [(row11,'top', 5, row10)], attachForm =[(row11, 'left', 230)])

    prefixButton('btm_')


    cmds.setParent('..')

    row12 = cmds.rowLayout(numberOfColumns=2, columnWidth=(160, 200), adjustableColumn=True)
    cmds.formLayout(form, edit = True, attachControl = [(row12,'top', 30, row6)], attachForm =[(row12, 'left', 55)])

    cmds.button('Delete All Position Prefixes', command = removePosSuffix, w= 155, h= 55)
    cmds.setParent('..')

