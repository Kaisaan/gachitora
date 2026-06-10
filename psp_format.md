# PSP File Format
Files have a "PSP" header and I can't think of a better name.  
Would be useful to know if any other game has the same or similar format.  
All values are stored as 4 byte long, little endian integers unless otherwise specified.

# Header
Is the first 0x10 bytes of the file.

|Offset|Description|
|---|---|
|$00-$03|Always `53 50 53 00` or `PSP` in ASCII|
|$04-$07|Always `00 00 80 3F` or 1 as a float|
|$08-$0B|**File Count**|
|$0C-$0F|Always `00 00 00 00`|

# File Info
Always starts at `0x10` of the file.
Each file has its offset (absolute value of the file) then its filesize.

# File Data
The rest of the file it all the data.