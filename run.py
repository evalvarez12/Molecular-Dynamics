import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model

# initial setup
rho = .25
T = 1.
dim = 3
n = 8
dt = .004
N = n ** dim
evols = 2000

# Storage for energy data
E_kin = np.array([])
E_pot = np.array([])
pressure = np.array([])
temps = np.array([])
E_kin_var = np.array([])
E_pot_var = np.array([])
D = np.zeros((N, N))
pos = np.zeros((evols, N, 3))

# initialize object system
system = model.system(n, rho, T, dim)
print("N = ", system.N)
print("box_size = ", system.box_size)

for j in range(200) :
    for i in range(10) :
        system.step(dt)
    print(j)
    system.equilibrate()

# for i in range(1000) :
#     system.step(dt)
system.set_quantities()
E0 = system.kinetic_energy + system.potential_energy
for i in range(evols) :
    system.step(dt)
    system.set_quantities()
    E_kin = np.append(E_kin, E0- system.kinetic_energy - system.potential_energy)

    # E_kin_var = np.append(E_kin_var,np.var(E_kin))
    # E_pot_var = np.append(E_pot_var,np.var(E_pot))

    pressure = np.append(pressure, system.pressure)
    temps = np.append(temps, system.temperature)
    D = D + system.D
    pos[i] = system.state_pos

D = D/evols
np.fill_diagonal(D, 0)
D = np.triu(D)
D = D.flatten()
D = D[ D != 0]
# print(D)
# Save data
# np.save("data/KE.npy", E_kin)
# np.save("data/U.npy", E_pot)
# np.save("data/P.npy", pressure)
# np.save("data/D.npy", D)
np.save("data/D4.npy", D)
np.save("data/pos4.npy", pos)

diff = np.average(np.std(pos, axis = 0), axis = 1)
print("diff = ", np.max(diff))
print("P = ", np.average(pressure)/rho)
print("T = ", np.average(temps))



x = np.linspace(0,len(E_kin),len(E_kin))

plt.figure()
plt.subplot(211)
plt.plot(x, E_kin, 'b')

plt.subplot(212)
plt.plot(x, temps, 'r')
plt.show()


n_bins = 100
plt.hist(D, bins = n_bins)
plt.show()
rmax = np.sqrt(system.dim)*system.box_size/2.

hist, bins = np.histogram(D, bins = n_bins, range=(0, rmax))
# hist, bins = np.histogram(D, bins = 200)
print(bins[1]  )
r = bins[:-1] + bins[1]/2.
print(len(r))
factor = system.box_size**3 / (system.N * (system.N - 1) * 2 * np.pi * bins[1])
# hist = factor * hist
hist = factor * hist/(r**2)

np.save("data/hist4.npy", hist)
np.save("data/bins4.npy", bins)
