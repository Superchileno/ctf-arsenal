from PIL import Image
import numpy as np
A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
print('shape', A.shape)
cols, counts = np.unique(A.reshape(-1,3), axis=0, return_counts=True)
order = np.argsort(-counts)
for i in order[:25]:
    print(tuple(cols[i]), counts[i])
print('unique colors', len(cols))
