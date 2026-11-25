line = "root:$1$aa$mI3wU4sOv2shpn9SHDOZt/:0:0:root:/root:/bin/sh\n"
s = line + "\n" * (80 - len(line))
print(len(line), len(s), repr(s))
print('C:', '"' + s.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n") + '"')
