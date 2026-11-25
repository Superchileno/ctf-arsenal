import numpy as np
from scipy.io import wavfile
from scipy import signal

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)

# envolvente robusta
w = int(0.004*rate)
env = np.abs(x)
env = np.convolve(env, np.ones(w)/w, mode="same")

thr = env.max()*0.02
on = env > thr
# run lengths
changes = np.flatnonzero(np.diff(on.astype(int)) != 0) + 1
runs = []
prev = 0
for c in changes:
    runs.append((on[prev], (c-prev)/rate, prev/rate))
    prev = c
runs.append((on[prev], (len(on)-prev)/rate, prev/rate))

print("umbral", round(thr,1), "max env", round(env.max(),1))
print("\nRacha  Duracion(s)  inicio(s)")
for state, dur, t0 in runs:
    if dur < 0.005: continue
    print(("ON " if state else "off"), f"{dur:7.3f}", f"{t0:7.3f}")

# repeticion de patrones?
print("\ntotal ON:", round(sum(d for s,d,_ in runs if s),2), "s")
