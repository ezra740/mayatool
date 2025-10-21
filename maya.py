import maya.cmds as cmds

#Don't use Caps at start for some reason
windowName = 'Simple Renamer Tool'

if cmds.window(windowName, exists=True):
    print('exists')
    cmds.deleteUI(windowName)
    cmds.windowPref(windowName, remove=True)

    

window = cmds.window(windowName, resizeToFitChildren=True, sizeable=False, widthHeight=(180,200))
cmds.columnLayout(adjustableColumn=True, rowSpacing=100)
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

cmds.button("Find all named:", command=findName)
ObjFind = cmds.textField(w=130)
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
ObjNewName = cmds.textField()
cmds.setParent('..')
    

row3 = cmds.rowLayout(numberOfColumns=2, columnWidth=(160, 200), adjustableColumn=2)
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

cmds.button("Remove 'pasted__'", w=220, command=deletePaste)
cmds.setParent('..')




#Adding Prefixes and Suffixes

