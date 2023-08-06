import shutil
import os
def CreateDirectory(Path, RemoveifExist=True):
    if os.path.isdir(Path) and RemoveifExist:
        shutil.rmtree(Path)
    if not os.path.isdir(Path):
        os.mkdir(Path)