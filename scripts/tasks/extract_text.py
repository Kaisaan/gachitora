import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libgachitora.text import extract_zar

def extract_text(binFile: Path):

    binPath = Path("work") / binFile.name
    shutil.copy(binFile, binPath)
    
    extract_zar(binPath)