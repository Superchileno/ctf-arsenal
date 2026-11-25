import numpy as np
from scipy.io import wavfile
from scipy import signal

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)

def ascii_spec(lo, hi, nrows, ncols, t0, t1, gamma=1.0):
    a, b = int(t0*rate), int(t1*rate)
    seg = x[a:b]
    nper = 1024
    f, t, S = signal.spectrogram(seg, fs=rate, nperseg=nper, noverlap=nper-220,
                                 window="hann", scaling="spectrum")
    Sdb = 10*np.log10(S+1e-20)
    m = (f >= lo) & (f <= hi)
    Sdb = Sdb[m]
    # interpolar a nrows y ncols
    fi = np.linspace(0, Sdb.shape[0]-1, nrows)
    ti = np.linspace(0, Sdb.shape[1]-1, ncols)
    FI, TI = np.meshgrid(fi, ti, indexing="ij")
    from scipy.ndimage import map_coordinates
    Z = map_coordinates(Sdb, [FI, TI], order=1)
    # normalizar por columna (quita la envolvente temporal)
    Z = Z - np.median(Z, axis=0, keepdims=True)
    Z = Z - Z.min()
    Z = Z/ (Z.max()+1e-9)
    Z = Z**gamma
    chars = " .:-=+*#%@"
    idx = (Z*(len(chars)-1)).astype(int)
    lines = []
    for r in range(nrows-1, -1, -1):
        frow = lo + (hi-lo)*r/(nrows-1)
        lines.append(f"{frow:6.0f} |" + "".join(chars[i] for i in idx[r]))
    return "\n".join(lines)

print("=== 2000-5000 Hz ===")
print(ascii_spec(2000, 5000, 56, 230, 0.5, 4.8))
