import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libgachitora.graphics import rebuild_gim

def rebuild_graphics(binFile: Path, type: int):

    pngPath = Path("work") / binFile.stem
    pngPath = Path(pngPath).with_suffix(".png")
    
    rebuild_gim(pngPath, f"-gachi{type}")

    gimPath = pngPath.parent / (pngPath.stem + "_new.gim")
    binPath = gimPath.with_suffix(".bin")
    shutil.copy(gimPath, binPath)