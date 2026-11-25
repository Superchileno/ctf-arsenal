import numpy as np
from PIL import Image

for f in ['acertijo.png','cofres.png']:
    im=np.array(Image.open(r'ANCI\mercader\extract\%s'%f).convert('RGB'))
    bits=im&1
    print('==',f,im.shape, 'lsb ones overall %', round(bits.mean()*100,3))
    for c in range(3):
        print('  ch',c,'ones%', round(bits[:,:,c].mean()*100,3))
    p=bits.ravel()
    for order in ['msb','lsb']:
        b=p[:8000*8]
        by=np.packbits(b if order=='msb' else b[::-1])
        s=by.tobytes()
        printable=sum(32<=x<127 for x in s)
        print('  ',order,'printable%',round(printable/len(s)*100,2), s[:80])
