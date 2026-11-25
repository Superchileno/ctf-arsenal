import numpy as np
from scipy.io import wavfile
from scipy import signal

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
print("rate", rate)

def band_energy(x, a, b):
    seg = x[int(a*rate):int(b*rate)]
    f, P = signal.welch(seg, fs=rate, nperseg=4096)
    bands = [(0,300),(300,1000),(1000,2500),(2500,4500),(4500,8000),(8000,12000),(12000,16000),(16000,22000)]
    out = []
    for lo, hi in bands:
        m = (f>=lo)&(f<hi)
        out.append((f"{lo}-{hi}", float(10*np.log10(P[m].mean()+1e-20))))
    return out

for a,b,label in [(0.0,0.5,"intro 0-0.5s"), (0.6,1.4,"texto inicio"), (3.0,4.6,"texto fin"), (4.9,7.2,"cola 4.9-7.2")]:
    print(label, [(n, round(v,1)) for n,v in band_energy(x,a,b)])

# espectro del tramo "silencioso" 0-0.5s
seg = x[:int(0.5*rate)]
f, P = signal.welch(seg, fs=rate, nperseg=8192)
print("\nTop picos 0-0.5s (Hz, dB):")
idx = np.argsort(P)[::-1][:15]
print(sorted([(round(f[i]), round(10*np.log10(P[i]+1e-20),1)) for i in idx]))

# ¿es ruido o tonos? planitud espectral
print("mediana dB:", round(10*np.log10(np.median(P)+1e-20),1))

# guardar 0-0.5s amplificado
wavfile.write("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/intro_x50.wav", rate, np.int16(np.clip(x[:int(0.5*rate)]*50, -32768, 32767)))
print("escrito intro_x50.wav")

# comparar LSB y estructura del tramo silencioso
segq = x[:int(0.5*rate)].astype(np.int16)
print("intro min/max", segq.min(), segq.max(), "valores unicos", len(np.unique(segq)))
print("primeros 40:", segq[:40].tolist())
lsb = (segq & 1)
print("LSB ratio intro:", lsb.mean(), "transiciones:", np.abs(np.diff(lsb)).sum())
# ver si el tramo silencioso es un tono
f2, t2, S2 = signal.spectrogram(x[:int(0.5*rate)], fs=rate, nperseg=2048, noverlap=1536)
P2 = 10*np.log10(S2+1e-20)
print("spec intro shape", P2.shape, "max", P2.max(), "min", P2.min())
