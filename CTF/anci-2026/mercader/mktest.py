import zipfile, os
os.makedirs(r'ANCI\mercader\t', exist_ok=True)
p=r'ANCI\mercader\t\test.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('hola.txt', b'contenido de prueba '*50)
# python zipfile cannot write encrypted; use system? skip
print('created', p)
