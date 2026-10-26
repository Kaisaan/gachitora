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

    logFile.write(f"{pspPath.stem}\t{fileCount}\t{unknown1}\t{unknown2}\n")

    for i in range(fileCount):         # Then write all the files

        pspFile.seek(files[i][0])
        outData = pspFile.read(files[i][1])

        with open(Path(outFolder / f"{pspPath.stem}_{i}.bin"), "wb") as outFile:
            outFile.write(outData)
        
        logFile.write(f"{pspPath.stem}_{i}.bin\t{files[i][0]}\t{files[i][1]}\n")

    print(f"{pspPath.name} extracted to {outFolder}")

def rebuild_psp(txtPath: Path):

    txtFile = open(txtPath, "r", encoding="utf-8")

    fileInfo = txtFile.readline().strip("\n").split()

    print(fileInfo)

    filePath = "work" / Path(fileInfo[0])
    print(filePath)
    fileCount = int(fileInfo[1])
    unknown1 = struct.pack('<f', float(fileInfo[2]))
    unknown2 = struct.pack('<i', int(fileInfo[3]))

    outFile = open(f"{filePath}_new.bin", "wb+")

    outFile.write(b"PSP\x00")
    outFile.write(unknown1)
    outFile.write(struct.pack('<i', fileCount))
    outFile.write(unknown2)

    fileoffset = ((fileCount * 8) + 16) # Each file has offset & size (two 4 byte int) and header is 16 bytes

    for i in range(fileCount):

        outFile.write(struct.pack('<i', fileoffset))
        filesize = os.path.getsize(Path(f"{filePath}\\{filePath.stem}_{i}.bin"))
        outFile.write(struct.pack('<i', filesize))
        padding = 16 - (filesize % 16)
        fileoffset = fileoffset + filesize + padding

    for i in range(fileCount):
        with open(f"{filePath}\\{filePath.stem}_{i}.bin", "rb") as txtFile:
            fileData = txtFile.read()
            outFile.write(fileData)

            padding = 16 - (len(fileData) % 16)
            outFile.write(bytes(padding))   
