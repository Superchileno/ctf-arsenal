d=bytearray(open("ANCI/turno_noche/night_shift","rb").read())
print("before:",d[0x1278:0x1280].hex())
assert d[0x127b]==0x75
d[0x127b]=0x90; d[0x127c]=0x90
open("ANCI/turno_noche/night_shift_patched","wb").write(d)
print("patched written")
