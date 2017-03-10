import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model

# initial setup
rho = 0.8
dim = 3
n = 9
T = 1
dt = .004
N = n ** dim

# Storage for energy data
E_kin = np.array([])
E_pot = np.array([])
pressure = np.array([])
temps = np.array([])
E_kin_var = np.array([])
E_pot_var = np.array([])


# initialize object system
system = model.system(n, rho, T, dim)
print("N = ", system.N)
print("box_size = ", system.box_size)

for j in range(100) :
    for i in range(5) :
        system.step(dt)
    system.equilibrate()


for i in range(30) :
    system.step(dt)
    system.set_quantities()
    E_kin = np.append(E_kin, system.kinetic_energy)
    E_pot = np.append(E_pot, system.potential_energy)

    # E_kin_var = np.append(E_kin_var,np.var(E_kin))
    # E_pot_var = np.append(E_pot_var,np.var(E_pot))

    pressure = np.append(pressure, system.pressure)
    temps = np.append(temps, system.temperature)

D = system.D
np.fill_diagonal(D, 0)

# Save data
# np.save("data/KE.npy", E_kin)
# np.save("data/U.npy", E_pot)
# np.save("data/P.npy", pressure)
# np.save("data/D.npy", D)



print("P = ", np.average(pressure)/rho)
print("T = ", np.average(temps))

# x = np.linspace(0,len(E_kin),len(E_kin))
#
# plt.figure()
# plt.subplot(211)
# plt.plot(x, E_kin, 'b', x, E_pot, 'r')
#
# plt.subplot(212)
# plt.plot(x, pressure, 'b', temps, 'r')
# plt.show()
#
#
# D_flat = D.flatten()
#
# plt.hist(D_flat, bins=200)
# plt.show()
#
# D_hist, D_hist_edges = np.histogram(D_flat, bins = 200)
#
# sp = np.fft.fft(D_hist)
# freq = np.fft.fftfreq(D_hist.shape[-1])
# plt.plot(freq[1:],sp.real[1:])
# plt.show()
