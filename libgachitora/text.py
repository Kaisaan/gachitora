import struct
from pathlib import Path
from libgachitora.archive import PSP_MAGIC, readint

ZAR_MAGIC = b"ZAR\x00"

def extract_zar(zarPath: Path):

    zarFile = open(zarPath, "rb")

    outFile = open(zarPath.parent / f"{zarPath.stem}.txt", "w", encoding="utf-8")


    if zarFile.read(4) != ZAR_MAGIC:
        exit("ZAR missing")

    if zarFile.read(4) != PSP_MAGIC:
        exit("PSP missing")

    test1 = struct.unpack("f", zarFile.read(4))[0]
    if test1 != 1.0:
        print(test1)

    test2 = readint(zarFile.read(4))
    if test2 != 1:
        print(test2)

    offset1 = readint(zarFile.read(4))
    if offset1 != 0x20:
        print(offset1)

    offset2 = readint(zarFile.read(4))
    if offset2 != 0x80:
        print(offset2)

    zarFile.seek(0x40)
    encodingValue = readint(zarFile.read(1))

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

    zarFile.seek(offset1 + offset2)

    zarFile.read(2)

    lineCount = readint(zarFile.read(2))

    offset3 = readint(zarFile.read(4))

    lineInfo1 = []
    for i in range(lineCount):
        
        FFtest = zarFile.read(2)
        if FFtest != b"\xFF\xFF":
            print(f"{FFtest}")
        
        charCount = readint(zarFile.read(2))
        lineOffset = readint(zarFile.read(4))
        lineOffset = lineOffset + offset2

        lineInfo1.append([charCount, lineOffset])

    print(lineInfo1)

    lineInfo2 = []

    zarFile.seek(offset2 + offset3)

    for i in range(lineCount):
        unknown1 = readint(zarFile.read(4))
        unknown2 = readint(zarFile.read(4))
        unknown3 = readint(zarFile.read(4))
        unknown4 = readint(zarFile.read(4))

        lineInfo2.append([unknown1, unknown2, unknown3, unknown4])

    outFile.write(f"{encode}\t{lineCount}\t{offset1:X}\t{offset2:X}\t{offset3:X}\n")

    print(lineInfo2)

    for i in range(lineCount):

        zarFile.seek(lineInfo1[i][1])
        line = zarFile.read((lineInfo1[i][0] - 1) * charSize)
        line = line.decode(encoding=encode, errors="backslashreplace")
        line = line.replace("\n", "\\n")
        print(f"{lineInfo1[i][1]:X}\t{line}")
        #outFile.write(f"{lineInfo2[i][0]:X}\t{lineInfo2[i][1]:X}\t{lineInfo2[i][2]:X}\t{lineInfo2[i][3]:X}\t{lineInfo1[i][0]:X}\t{lineInfo1[i][1]:X}\t\t{line}\n")
        outFile.write(f"{line}\n")


