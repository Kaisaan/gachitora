import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libgachitora.archive import extract_zar

# TODO: Make Files into a dict (orig path -> work path)

def extract_files():
    binFile = Path("extracted/PSP_GAME/USRDIR/DATA/layout/01/LS01S01.BIN")
    binPath = Path("work/LS01S01.BIN")
    shutil.copy(binFile, binPath)
    
    extract_zar(binPath)