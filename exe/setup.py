import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "random", "PIL", "pyautogui", "cv2", "pytesseract", "re", "keyboard", "time", "io", "sys", "threading"],
    "include_files": ["rare.png", "dupe.png", "fail.png", "no_res.png", "won_bid.png", "soft_banned.png", "team.png", "open_fifa.png", "launch_fifa.png", "in_fifa.png", "cont_local.png", "no_res_1080.png", "fail_1080.png", "won_bid_1080.png", "dupe_1080.png"]}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="YourScriptName",
    version="1.0",
    description="Description of your script",
    options={"build_exe": build_exe_options},
    executables=[Executable("main_for_exe_2.py", base=base)]
)








