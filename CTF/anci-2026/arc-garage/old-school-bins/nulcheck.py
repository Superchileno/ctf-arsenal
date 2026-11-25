import gdb, struct
gdb.execute('set pagination off'); gdb.execute('set confirm off')
gdb.execute('break idx_cmp_qsort')
gdb.execute('run < /tmp/nul.txt')
garage=int(gdb.parse_and_eval('(unsigned long)&garage'))
c=int(gdb.parse_and_eval('(unsigned long)garage[4]')) if False else struct.unpack('<Q', gdb.selected_inferior().read_memory(garage+8*4,8).tobytes())[0]
m=struct.unpack('<Q', gdb.selected_inferior().read_memory(c,8).tobytes())[0]
mem=gdb.selected_inferior().read_memory(m,32).tobytes()
print('car4',hex(c),'model',hex(m))
print('bytes:',mem.hex())
print('repr :',repr(mem))
