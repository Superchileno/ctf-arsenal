import os, time
root = r"C:\Users\<usuario>\OneDrive - dipreca.cl\Agentes IA\AUDITORIA_IA_V2"
cutoff = time.time() - 45*60
hits = []
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', '__pycache__', '.agents')]
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            m = os.path.getmtime(p)
        except OSError:
            continue
        if m > cutoff:
            hits.append((m, os.path.getsize(p), p))
hits.sort(reverse=True)
for m, sz, p in hits[:60]:
    print(time.strftime('%H:%M:%S', time.localtime(m)), sz, os.path.relpath(p, root))
print('total', len(hits))
