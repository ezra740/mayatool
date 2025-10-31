from maya import cmds
import maya_Tool as mtool

def CreateToolMenu():
    menuName = "MyMayaTool"
    if cmds.menu(menuName, exists=True):
        cmds.deleteUI(menuName, menu=True)
    

    customTool = cmds.menu(menuName, label= "My Maya Tool", parent="MayaWindow", tearOff=True)

    cmds.menuItem(label="Launch Window", parent=customTool,command=lambda val: mtool.LaunchNonDockableWindow(),image="toolSettings.png")
