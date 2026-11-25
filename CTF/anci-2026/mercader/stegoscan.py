import numpy as np, itertools, re
from PIL import Image

def bits_of(im, bit):
    a=im.astype(np.uint8)
    return ((a>>bit)&1)

def tobytes(bits):
    n=len(bits)//8*8
    return np.packbits(bits[:n]).tobytes()

def score(b):
    if not b: return 0,0
    printable=sum(1 for x in b if 32<=x<127 or x in (9,10,13))
    return printable/len(b), printable

for f in ['acertijo.png','cofres.png']:
    im=np.array(Image.open('extract/%s'%f).convert('RGB'))
    print('=====',f,im.shape)
    H,W,_=im.shape
    for bit in range(4):
        b=bits_of(im,bit)
        # channel orders
        for order in [(0,1,2),(2,1,0),(1,0,2),(0,2,1)]:
            seq=b[:,:,list(order)].ravel()
            data=tobytes(seq)
            p,_=score(data)
            head=data[:80]
            print(' bit',bit,'order',order,'printable%',round(p*100,1), head[:40])
        # single channel
        for c in range(3):
            data=tobytes(b[:,:,c].ravel())
            p,_=score(data)
            print(' bit',bit,'ch',c,'printable%',round(p*100,1), data[:40])

