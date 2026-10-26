import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libgachitora.archive import rebuild_psp

def rebuild_files(binFile: Path):

    oldBin = Path("work") / binFile.stem / binFile.name

    txtFile = Path("work") / (binFile.stem + ".txt")

    rebuild_psp(txtFile)

    newBin = Path("work") / (binFile.stem + "_new.bin")

    shutil.copy(newBin, oldBin)
    print(f"{newBin} has overwritten {oldBin}")