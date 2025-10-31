print("Loading userSetup")

import maya.cmds as cmds

cmds.commandPort(name="127.0.0.1:5678", stp="python")
cmds.commandPort(name="127.0.0.1:7001", stp="mel")

print("Loading Simple Rename")

import maya.utils

def startTool():
    import maya_Tool as renameTool
    renameTool.CreateToolMenu()
    print ("Tool is ready!")
maya.utils.executeDefferred(startTool)