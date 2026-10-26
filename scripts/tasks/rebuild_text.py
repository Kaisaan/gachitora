import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libgachitora.text import rebuild_zar

def rebuild_text(binFile: Path):

    txtPath = Path("work") / binFile.name
    txtPath = Path(txtPath).with_suffix(".txt")

    newBin = txtPath.parent / (txtPath.stem + "_new.bin")
    shutil.copy(binFile, newBin)
    
    rebuild_zar(txtPath)

    