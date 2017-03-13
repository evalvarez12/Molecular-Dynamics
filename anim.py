import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model


# initial setup
rho = 1.2
T = .4
dim = 3
n = 6
dt = .004
N = n ** dim

# Storage for energy data
E_kin = np.array([])
E_pot = np.array([])
pressure = np.array([])
temps = np.array([])
E_kin_var = np.array([])
E_pot_var = np.array([])
D = np.zeros((N, N))

evols = 0
# initialize object system
system = model.system(n, rho, T, dim)
print("N = ", system.N)
print("box_size = ", system.box_size)

for j in range(500) :
    for i in range(5) :
        system.step(dt)
    system.equilibrate()

for i in range(1000) :
    system.step(dt)

print("T = ", system.temperature)

# set up figure and animation
box_size = system.box_size
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(0, box_size), ylim=(0, box_size))

# particles holds the locations of the particles
particles, = ax.plot([], [], 'bo', ms=6)

# rect is the box edge
rect = plt.Rectangle((0, 0), box_size, box_size, ec='none', lw=2, fc='none')
ax.add_patch(rect)

def init():
    global system, rect
    particles.set_data([], [])
    rect.set_edgecolor('none')
    return particles, rect

def animate(i):
    global box, rect, dt, ax, E_kin, E_pot, E_kin_var, E_pot_var, pressure, fig, D, evols
    system.step(dt)

    ms = int(fig.dpi * 2 * box_size * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])

    # update pieces of the animation
    rect.set_edgecolor('k')
    particles.set_data(system.state_pos[:, 0], system.state_pos[:, 1])

    E_kin = np.append(E_kin, system.kinetic_energy)
    E_pot = np.append(E_pot, system.potential_energy)

    E_kin_var = np.append(E_kin_var,np.var(E_kin))
    E_pot_var = np.append(E_pot_var,np.var(E_pot))

    D = D + system.D
    evols += 1
    # pressure = np.append(pressure, system.pressure)

    return particles, rect


ani = animation.FuncAnimation(fig, animate, frames=600, interval=10, blit=True, init_func=init)
plt.show()


D = D/evols
np.fill_diagonal(D, 0)
# D = np.triu(D)
D = D.flatten()
D = D[ D != 0]

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

# Prints coordinates to console, for copying into pgfplots hist
# print('Correlation function data')
# for i in range(len(hist)) :
#     print('('+ str(bins[i]) + ', ' + str(hist[i]), ')')


plt.bar(bins[:-1], hist, width = rmax/n_bins, edgecolor = "r")

# D_hist, D_hist_edges = np.histogram(D, bins = 200)
#
# sp = np.fft.fft(D_hist)
# freq = np.fft.fftfreq(D_hist.shape[-1])
# plt.plot(freq[1:],sp.real[1:])
plt.show()
