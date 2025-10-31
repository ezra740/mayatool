print("Loading userSetup")

import maya.cmds as cmds

cmds.commandPort(name="127.0.0.1:5678", stp="python")
cmds.commandPort(name="127.0.0.1:7001", stp="mel")

print("Loading Simple Rename")

import maya.utils
import MayaTool.maya_ToolMenu as mToolMenu

def startTool():
    mToolMenu.CreateToolMenu()
    print ("Tool is ready!")
maya.utils.executeDeferred(startTool)