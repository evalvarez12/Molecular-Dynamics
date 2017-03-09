import matplotlib.pyplot as plt
import numpy as np


# load arrays

E_kin = np.load("data/KE.npy")
E_pot = np.load("data/U.npy")
pressure = np.load("data/P.npy")
D = np.load("data/D.npy")

print(E_kin)

x = np.linspace(0,len(E_kin),len(E_kin))

plt.figure()
plt.subplot(211)
plt.plot(x, E_kin, 'b', x, E_pot, 'r')

plt.subplot(212)
plt.plot(x, pressure, 'b')
plt.show()

D_flat = D.flatten()

# plt.hist(D_flat, bins=100)
# plt.show()

D_hist, D_hist_edges = np.histogram(D_flat, bins = 100)

sp = np.fft.fft(D_hist)
freq = np.fft.fftfreq(D_hist.shape[-1])
plt.plot(freq[2:50],sp.real[2:50])
plt.show()
