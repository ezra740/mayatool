import maya.cmds as cmds

windowName = 'Simple Renamer Tool'

if cmds.window(windowName, ex=True):
    print('exists')
    cmds.deleteUI(windowName, window=True)

window = cmds.window(windowName)
cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
form = cmds.formLayout()
row = cmds.rowLayout(numberOfColumns=2, columnWidth=(80, 200), columnAlign=(1, "left"))
cmds.formLayout(form, edit = True, attachForm = [(row, 'top', 0)])

#Finding the Name
def findName(*args):
    #print(f"text field = {ObjFind}")
    ObjName = cmds.textField(ObjFind, query=True, text=True)
    #print(f"input = {ObjName}")
    matched = cmds.ls(f"*{ObjName}*", type = 'transform')
    #print(matched)
    if matched:
        cmds.select(matched)
    else:
        cmds.warning(f"Object '{ObjName}' does not exist")
    
    
cmds.button("Find all named:", command=findName)
ObjFind = cmds.textField()

#Replacing the Name
def rename(*args):
    cmds.button("Replace selected with:", command=rename)
    



cmds.showWindow(window)
