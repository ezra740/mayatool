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


#Adding Prefixes and Suffixes#
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


#Adding a automatic namer for their Node Type


