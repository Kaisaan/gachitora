# ZAR File Format
Would be useful to know if any other game has the same or similar format.  
All values are stored as 4 byte long, little endian integers unless otherwise specified.

# Header
|Offset|Description|
|---|---|
|$00-$03|Always `5A 41 52 00` or `ZAR` in ASCII|
|$04-$07|Always `53 50 53 00` or `PSP` in ASCII|
|$08-$0B|Always `00 00 80 3F` or 1 as a float|
|$0C-$0F|Always `00 00 00 00`|

If the value at 0x40 is 0x10 then the text is encoded in Shift-JIS.  
If the value at 0x40 is 0x34 then the text is encoded in UTF-16 (Little Endian).