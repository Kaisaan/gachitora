# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "hacktools[psp]"
# ]
# ///
import os
import shutil
import sys
from pathlib import Path
from hacktools import psp
from tasks.rebuild_files import rebuild_files
from tasks.rebuild_text import rebuild_text
from tasks.rebuild_graphics import rebuild_graphics
from extract_iso import FILES, TEXTS, GRAPHICS

FILES = [
    Path("extracted/PSP_GAME/USRDIR/DATA/layout/01/LS01S01.BIN"),
    Path("extracted/PSP_GAME/USRDIR/DATA/2D/STG0001.BIN")
]

TEXTS = [
    Path("work/LS01S01/LS01S01_109.bin")
]

GRAPHICS = {
    Path("work/STG0001/STG0001_0.bin") : 1
}

def main():

    print("Rebuilding graphics...")
    for graphic, type in GRAPHICS.items():
        rebuild_graphics(graphic, type)
    print("Done!")

    print("Rebuilding text...")
    for text in TEXTS:
        rebuild_text(text)    
    print("Done!")

    print("Rebuilding files...")
    os.makedirs("work", exist_ok=True)
    for file in FILES:
        rebuild_files(file)
    print("Done!")

    print("Rebuilding iso...") 
    psp.repackIso("gachitora.iso", "english.iso", "translated/")
    print("Done!")

if __name__ == "__main__":
    main()
