from maya import cmds
import MayaTool.maya_Tool as mtool

def CreateToolMenu():
    menuName = "MyMayaTool"
    if cmds.menu(menuName, exists=True):
        cmds.deleteUI(menuName, menu=True)

    customTool = cmds.menu(menuName, label= "{~CustomScripts~}", parent="MayaWindow", tearOff=True)

    cmds.menuItem(label="Launch Simple Rename (Not Dockable)", parent=customTool,command=lambda val: mtool.LaunchNonDockableWindow(),image="pythonFamily.png")
