import sys, struct, os

txtName = sys.argv[1]

txtFile = open(f"{txtName}", "r", encoding="utf-8")

fileInfo = txtFile.readline().strip("\n").split()

print(fileInfo)

fileName = fileInfo[0]
fileCount = int(fileInfo[1])
unknown1 = struct.pack('<f', float(fileInfo[2]))
unknown2 = struct.pack('<i', int(fileInfo[3]))

outFile = open(f"{fileName}_new.bin", "wb+")

outFile.write(b"PSP\x00")
outFile.write(unknown1)
outFile.write(struct.pack('<i', fileCount))
outFile.write(unknown2)

fileoffset = ((fileCount * 8) + 16) # Each file has offset & size (two 4 byte int) and header is 16 bytes

for i in range(fileCount):

    outFile.write(struct.pack('<i', fileoffset))
    filesize = os.path.getsize(f"{fileName}\\{fileName}_{i}.bin")
    outFile.write(struct.pack('<i', filesize))
    padding = 16 - (filesize % 16)
    fileoffset = fileoffset + filesize + padding

for i in range(fileCount):
    with open(f"{fileName}\\{fileName}_{i}.bin", "rb") as binFile:
        fileData = binFile.read()
        outFile.write(fileData)

        padding = 16 - (len(fileData) % 16)
        outFile.write(bytes(padding))