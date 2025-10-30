import maya.cmds as cmds

cmds.commandPort(name="127.0.0.1:5678", stp="python")
cmds.commandPort(name="127.0.0.1:7001", stp="mel")