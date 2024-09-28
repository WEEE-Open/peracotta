import importlib.resources
import os
import sys

if "peracotta" in sys.modules:
    if sys.version_info >= (3, 9):
        basedir = importlib.resources.files(__package__)
    else:
        import importlib_resources  # backport for python 3.8, remove it when EOL

        basedir = importlib_resources.files(__package__)

else:  # in case it's being called without installing the package
    basedir = os.path.dirname(__file__)

URL = {
    "website": "https://weeeopen.polito.it",
    "source_code": "https://github.com/WEEE-Open/peracotta",
}

VERSION = "2.5.0"

PATH = {
    "UI": "assets/interface.ui",
    "TARALLOUPLOADDIALOG": "assets/uploadTaralloDialog.ui",
    "ERRORDIALOG": "assets/error.ui",
    "JSON": "copy_this_to_tarallo.json",
    "FEATURES": "features.json",
    "THEMES": "assets/themes/",
    "TMP_FILES": "tmp/",
    "ICON": "assets/ui/pear_emoji.png",
}
for k, v in PATH.items():
    PATH[k] = os.path.join(basedir, v)

ICON = {
    "case": "assets/toolbox/case.png",
    "ram": "assets/toolbox/ram.png",
    "cpu": "assets/toolbox/cpu.png",
    "graphics-card": "assets/toolbox/gpu.png",
    "odd": "assets/toolbox/odd.png",
    "hdd": "assets/toolbox/hdd.png",
    "ssd": "assets/toolbox/ssd.png",
    "motherboard": "assets/toolbox/motherboard.png",
    "wifi-card": "assets/toolbox/wifi-card.png",
    "psu": "assets/toolbox/psu.png",
    "monitor": "assets/toolbox/monitor.png",
    "keyboard": "assets/toolbox/keyboard.png",
    "mouse": "assets/toolbox/mouse.png",
}

for k, v in ICON.items():
    ICON[k] = os.path.join(basedir, v)
