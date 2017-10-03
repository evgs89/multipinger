import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
icon_file = "ui/icons/paperplane.png"
buildOptions = dict(icon = icon_file)
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Pinger",
        version = "2.0",
        description = "MultiPinger",
        options = {"build_exe": build_exe_options},
        executables = [Executable("MultiPing.pyw", base=base)])

