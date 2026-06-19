import sys, struct
from pathlib import Path

filepath = sys.argv[1]

filepath = Path(filepath).resolve()
filedir = filepath.parent
filename = filepath.name

inFile = open(filepath, "rb")

filename = filename[:filename.rfind(".bin")]

input_dir = filedir / filename

outFile = open(filedir / f"{filename}.txt", "w", encoding="utf-8")

ZARmagic = b"ZAR\x00"
PSPmagic = b"PSP\x00"

if inFile.read(4) != ZARmagic:
    exit("ZAR missing")

if inFile.read(4) != PSPmagic:
    exit("PSP missing")

test1 = struct.unpack("f", inFile.read(4))[0]
if test1 != 1.0:
    print(test1)

test2 = int.from_bytes(inFile.read(4), byteorder="little")
if test2 != 1:
    print(test2)

offset1 = int.from_bytes(inFile.read(4), byteorder="little")
if offset1 != 0x20:
    print(offset1)

offset2 = int.from_bytes(inFile.read(4), byteorder="little")
if offset2 != 0x80:
    print(offset2)

inFile.seek(0x40)
encodingValue = int.from_bytes(inFile.read(1), byteorder="little")

encode = ""
charSize = 0
if encodingValue == 0x34:
    encode = "shiftjis"
    charSize = 1
elif encodingValue == 0x10:
    encode = "utf_16"
    charSize = 2
else:
    exit(f"encoding value: {encodingValue}")
print(encode)

inFile.seek(offset1 + offset2)

inFile.read(2)

lineCount = int.from_bytes(inFile.read(2), byteorder="little")

offset3 = int.from_bytes(inFile.read(4), byteorder="little")

lineInfo1 = []
for i in range(lineCount):
    
    FFtest = inFile.read(2)
    if FFtest != b"\xFF\xFF":
        print(f"{FFtest}")
    
    charCount = int.from_bytes(inFile.read(2), byteorder="little")
    lineOffset = int.from_bytes(inFile.read(4), byteorder="little")
    lineOffset = lineOffset + offset2

    lineInfo1.append([charCount, lineOffset])

print(lineInfo1)

lineInfo2 = []

inFile.seek(offset2 + offset3)

for i in range(lineCount):
    unknown1 = int.from_bytes(inFile.read(4), byteorder="little")
    unknown2 = int.from_bytes(inFile.read(4), byteorder="little")
    unknown3 = int.from_bytes(inFile.read(4), byteorder="little")
    unknown4 = int.from_bytes(inFile.read(4), byteorder="little")

    lineInfo2.append([unknown1, unknown2, unknown3, unknown4])

outFile.write(f"{encode}\t{lineCount}\t{offset1:X}\t{offset2:X}\t{offset3:X}\n")

print(lineInfo2)

for i in range(lineCount):

    inFile.seek(lineInfo1[i][1])
    line = inFile.read((lineInfo1[i][0] - 1) * charSize)
    line = line.decode(encoding=encode, errors="backslashreplace")
    line = line.replace("\n", "\\n")
    print(f"{lineInfo1[i][1]:X}\t{line}")
    #outFile.write(f"{lineInfo2[i][0]:X}\t{lineInfo2[i][1]:X}\t{lineInfo2[i][2]:X}\t{lineInfo2[i][3]:X}\t{lineInfo1[i][0]:X}\t{lineInfo1[i][1]:X}\t\t{line}\n")
    outFile.write(f"{line}\n")


