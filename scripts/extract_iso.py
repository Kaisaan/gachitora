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
from tasks.extract_files import extract_files
from tasks.extract_text import extract_text
from tasks.exctract_graphics import extract_graphics

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
    print("Copy the original .iso next to this script and rename it to gachitora.iso")

    print("Extracting iso...")
    if os.path.exists("extracted"):
        shutil.rmtree("extracted")  
    psp.extractIso("gachitora.iso", "extracted/")
    
    if os.path.exists("translated"):
        shutil.rmtree("translated")
    shutil.copytree("extracted", "translated")
    print("Done!")

    print("Extracting files...")
    os.makedirs("work", exist_ok=True)
    for file in FILES:
        extract_files(file)
    print("Done!")

    print("Extracting text...")

    for text in TEXTS:
        extract_text(text)
    
    print("Done!")

    print("Extracting graphics...")

    for graphic, type in GRAPHICS.items():
        extract_graphics(graphic, type)

    print("Done!")


if __name__ == "__main__":
    main()
