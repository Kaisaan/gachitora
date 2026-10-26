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
    extract_files()
    print("Done!")

    print("Extracting text...")
    extract_text()
    print("Done!")   


if __name__ == "__main__":
    main()
