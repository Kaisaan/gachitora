import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libgachitora.text import extract_zar

def extract_text():
    binFile = Path("work/LS01S01/LS01S01_109.bin")
    binPath = Path("work/LS01S01_109.bin")
    shutil.copy(binFile, binPath)
    
    extract_zar(binPath)