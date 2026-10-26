import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libgachitora.archive import extract_psp

def extract_files(binFile: Path):

    binPath = Path("work") / binFile.name
    shutil.copy(binFile, binPath)
    
    extract_psp(binPath)