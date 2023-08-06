Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "C:\\Users\\user\\Desktop\\Dosie.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\\Users\\user\\Desktop\\Dosiebb\\Dosie\\Dosie.pyw"
oLink.IconLocation = "C:\\Users\\user\\Desktop\\Dosiebb\\Dosie\\icon.ico, 0"
oLink.Description = "Search Engine"
oLink.Save