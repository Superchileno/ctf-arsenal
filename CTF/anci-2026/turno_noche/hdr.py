d=open("ANCI/turno_noche/night_shift","rb").read()
print(len(d), d[:20])
print("ELF" if d[:4]==b"\x7fELF" else "not elf")
import struct
if d[:4]==b"\x7fELF":
    print("class",d[4],"endian",d[5],"type",struct.unpack("<H",d[16:18])[0],"machine",struct.unpack("<H",d[18:20])[0])
