import sys, os, struct

inFileName = sys.argv[1]

inFile = open(inFileName, "rb")

inFileName = inFileName.rstrip(".BIN").rstrip(".bin")

outFolder = os.makedirs(f"{inFileName}", exist_ok=True)

logFile = open(f"{inFileName}.txt", "w+", encoding="utf-8")

header = inFile.read(0x10)

identifier = b"PSP\x00"     # Seems to be the magic identifier for these files (50 53 50 00 in hex)

if header[0x00:0x04] != identifier:
    exit("File missing PSP identifier!")

unknown1 = struct.unpack("f", header[0x04:0x08])[0]    # Usually seems to be 00 00 80 3F which is 1 as a float

unknown2 = int.from_bytes(header[0x0C:0x10])    # Usually seems to be 00 00 00 00

fileCount = int.from_bytes(header[0x08:0x0C], byteorder="little")

files = []

for i in range(fileCount):          # First get all files' info

    fileInfo = inFile.read(0x08)

    fileOffset = int.from_bytes(fileInfo[0x00:0x04], byteorder="little")
    fileSize = int.from_bytes(fileInfo[0x04:0x08], byteorder="little")

    files.append([fileOffset, fileSize])

logFile.write(f"{inFileName}\t{fileCount}\t{unknown1}\t{unknown2}\n")

for i in range(fileCount):         # Then write all the files

    inFile.seek(files[i][0])
    outData = inFile.read(files[i][1])

    with open(f"{inFileName}//{inFileName}_{i}.bin", "wb") as outFile:
        outFile.write(outData)
    
    logFile.write(f"{inFileName}_{i}.bin\t{files[i][0]}\t{files[i][1]}\n")
    