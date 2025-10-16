import maya.cmds as cmds

cmds.commandPort(name="localhost:5678", stp="python")
cmds.commandPort(name="localhost:7001", stp="mel")