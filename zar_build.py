import sys, struct, shutil
from pathlib import Path


filepath = sys.argv[1]

filepath = Path(filepath).resolve()
filedir = filepath.parent
filename = filepath.name

origFile = open(filepath, "rb")

filename = filename[:filename.rfind(".bin")]

shutil.copy(filepath, filedir / f"{filename}_new.bin")

newFile = open(filedir / f"{filename}_new.bin", "r+b")

txtFile = open(filedir / f"{filename}.txt", "r", encoding="utf-8")

ZARmagic = b"ZAR\x00"
PSPmagic = b"PSP\x00"

if origFile.read(4) != ZARmagic:
    exit("ZAR missing")

if origFile.read(4) != PSPmagic:
    exit("PSP missing")

fileInfo = txtFile.readline().strip("\n").split()

encode = fileInfo[0]

if (encode in ["utf_16", "shiftjis"]):
    pass
else:
    exit(f"Encoding {fileInfo[0]} not supported")    

lineCount = int(fileInfo[1], base=10)
offset1 = int(fileInfo[2], base=16)
offset2 = int(fileInfo[3], base=16)
offset3 = int(fileInfo[4], base=16)

lineInfo = []

for i in range(lineCount):
    line = txtFile.readline().strip("\n")
    line = line.replace("\\n", "\n")

    if encode == "utf_16":
        linedata = bytearray(line.encode(encoding=encode))
        linedata = linedata[2:]

        if linedata == b'':
            line = ""
        else:
            line = linedata.decode(encoding=encode)

    lineSize = len(line)

    if encode == "utf_16":
        lineSize = len(line) * 2

    if i == lineCount-1:
        paddingSize = 0
    else:
        paddingSize = 32 - (lineSize % 32)
    if (lineSize % 32) < 3:
        paddingSize = paddingSize + 32
    if lineSize == 0:
        paddingSize = 32

    lineInfo.append([line, lineSize, paddingSize, linedata])

newFile.seek(offset1 + offset2)
newFile.read(8)

totalOffset = offset2 + offset3

for i in range(lineCount):
    newFile.read(2)
    size = len(lineInfo[i][0]) + 1
    
    newFile.write(size.to_bytes(2, byteorder="little"))
    print(f"{totalOffset:X}")
    newFile.write(totalOffset.to_bytes(4, byteorder="little"))
    
    totalOffset = totalOffset + lineInfo[i][1] + lineInfo[i][2]
    

newFile.seek(offset2 + offset3 + offset2)

for i in range(lineCount):
    
    newFile.write(lineInfo[i][3])
    if i != lineCount - 1:
    
        newFile.write(bytes(lineInfo[i][2]))


