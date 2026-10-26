import os, struct
from pathlib import Path

PSP_MAGIC = b"PSP\x00"

def readint(b: bytes) -> int:
    return int.from_bytes(b, byteorder="little")

def extract_psp(pspPath: Path):

    pspFile = open(pspPath, "rb")

    outFolder = (pspPath.parent / pspPath.stem)
    os.makedirs(outFolder, exist_ok=True)

    logFile = open((pspPath.parent / f"{pspPath.stem}.txt"), "w+", encoding="utf-8")
    
    header = pspFile.read(0x10)

    identifier = b"PSP\x00"     # Seems to be the magic identifier for these files (50 53 50 00 in hex)

    if header[0x00:0x04] != identifier:
        exit("File missing PSP identifier!")

    unknown1 = struct.unpack("f", header[0x04:0x08])[0]    # Usually seems to be 00 00 80 3F which is 1 as a float

    unknown2 = readint(header[0x0C:0x10])    # Usually seems to be 00 00 00 00

    fileCount = readint(header[0x08:0x0C])

    files = []

    for i in range(fileCount):          # First get all files' info

        fileInfo = pspFile.read(0x08)

        fileOffset = int.from_bytes(fileInfo[0x00:0x04], byteorder="little")
        fileSize = int.from_bytes(fileInfo[0x04:0x08], byteorder="little")

        files.append([fileOffset, fileSize])

    logFile.write(f"{pspPath.name}\t{fileCount}\t{unknown1}\t{unknown2}\n")

    for i in range(fileCount):         # Then write all the files

        pspFile.seek(files[i][0])
        outData = pspFile.read(files[i][1])

        with open(Path(outFolder / f"{pspPath.stem}_{i}.bin"), "wb") as outFile:
            outFile.write(outData)
        
        logFile.write(f"{pspFile}_{i}.bin\t{files[i][0]}\t{files[i][1]}\n")

    print(f"{pspPath.name} extracted to {outFolder}")
        
