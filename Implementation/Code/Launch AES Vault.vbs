Option Explicit

Dim shell, filesystem, projectPath, pythonPath, command
Set shell = CreateObject("WScript.Shell")
Set filesystem = CreateObject("Scripting.FileSystemObject")
projectPath = filesystem.GetParentFolderName(WScript.ScriptFullName)
pythonPath = shell.ExpandEnvironmentStrings("%LocalAppData%") & "\Programs\Python\Python313\pythonw.exe"

If Not filesystem.FileExists(pythonPath) Then
    pythonPath = "pythonw.exe"
End If

shell.CurrentDirectory = projectPath
command = """" & pythonPath & """" & " -m aes_tool.app"
shell.Run command, 0, False
