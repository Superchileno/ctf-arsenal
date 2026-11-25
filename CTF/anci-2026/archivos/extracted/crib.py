from PIL import Image
import numpy as np, base64, itertools, os

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
need = n * 8
img = Image.open('stamp_scan.png').convert('RGB')
A = np.array(img).astype(int)

CRIB = b'flag{'
hits = []
schemes = 0

def test(bitstream, tag):
    global schemes
    schemes += 1
    bits = np.asarray(bitstream, dtype=np.uint8)
    m = len(bits) // 8 * 8
    if m < need:
        return
    by = np.packbits(bits[:m])
    # try every byte offset
    for off in range(0, min(len(by) - n, 300) + 1):
        key = by[off:off + n]
        p = np.bitwise_xor(np.frombuffer(ct,dtype=np.uint8), key)
        # quick crib check
        s = p.tobytes()
        if CRIB in s:
            hits.append((tag, off, s))
            print('HIT', tag, 'offset', off)
            print(s)

# --- sources of binary planes ---
band_mask = np.all(A == [255, 254, 232], axis=2)

# 1) band grid rows
rows_all = [r for r in range(band_mask.shape[0]) if band_mask[r].any()]
print('band rows', rows_all[0], rows_all[-1], len(rows_all))

row_sets = {
    'all_rows': rows_all,
}
for pitch in (2, 3):
    rs = rows_all[::pitch]
    row_sets['pitch%d' % pitch] = rs

cols = {
    'full': (0, 720),
    'inner': (40, 680),
}

for rname, rs in row_sets.items():
    for cname, (c0, c1) in cols.items():
        G = band_mask[np.ix_(rs, list(range(c0, c1)))].astype(np.uint8)
        for inv in (0, 1):
            H = (1 - G) if inv else G
            for order in ('row', 'col'):
                flat = H.reshape(-1) if order == 'row' else H.T.reshape(-1)
                for shift in range(8):
                    f = np.roll(flat, -shift)
                    test(f, '%s/%s/inv%d/%s/shift%d' % (rname, cname, inv, order, shift))

# 2) LSB planes of whole image
for ch, name in enumerate('RGB'):
    for bit in (0, 1, 2):
        plane = ((A[:, :, ch] >> bit) & 1).astype(np.uint8)
        for order in ('row',):
            flat = plane.reshape(-1)
            for shift in range(8):
                test(np.roll(flat, -shift), 'lsb%s_b%d/%s/shift%d' % (name, bit, order, shift))

print('schemes probed:', schemes, 'hits:', len(hits))
