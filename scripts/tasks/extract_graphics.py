import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libgachitora.graphics import extract_gim

def extract_graphics(binFile: Path, type: int):

    binPath = Path("work") / binFile.stem
    binPath = Path(binPath).with_suffix(".gim")
    shutil.copy(binFile, binPath)
    
    extract_gim(binPath, f"-gachi{type}")