import subprocess
import os

configPath = os.path.dirname(__file__)

cmd = (configPath+'/shortcut.vbs')
with open(configPath+'/shortcut.vbs','w+') as shortcut:
    SCtext = 'Set oWS = WScript.CreateObject("WScript.Shell")\nsLinkFile = "'+os.path.expanduser("~")+'\\Desktop\\Dosie.lnk"\nSet oLink = oWS.CreateShortcut(sLinkFile)\noLink.TargetPath = "'+configPath+'\\Dosie.pyw"\noLink.IconLocation = "'+configPath+'\\icon.ico, 0"\noLink.Description = "Search Engine"\noLink.Save'
    SCtext = SCtext.replace('\\','\\\\')
    shortcut.write(SCtext)
subprocess.call(['cscript.exe', cmd], shell=True)
