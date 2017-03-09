import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model

# initial setup
rho = .5
T = 1.
dim = 3
dt = 1. / 1000.

# Storage for energy data
E_kin = np.array([])
E_pot = np.array([])
E_kin_var = np.array([])
E_pot_var = np.array([])


# initialize object system
system = model.system(rho, T, dim)

system.equilibrate(dt)
system.equilibrate(dt)
system.equilibrate(dt)
system.equilibrate(dt)

# set up figure and animation
box_size = 5
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
    global box, rect, dt, ax, E_kin, E_pot, E_kin_var, E_pot_var, fig
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

    return particles, rect


ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=10, blit=True, init_func=init)


plt.show()

x = np.linspace(0,len(E_kin),len(E_kin))

plt.figure(2)
plt.subplot(211)
plt.plot(x, E_kin, 'b', x, E_pot, 'r')

plt.subplot(212)
plt.plot(x, E_kin_var, 'b', x, E_pot_var, 'r')
plt.show()

r_norm, D = physics.normal_vecs(system.state_pos, box_size)
D = D.flatten()

plt.hist(D, bins=100)
plt.show()

D_hist, D_hist_edges = np.histogram(D, bins = 100)
# print(D_hist)

sp = np.fft.fft(D_hist)
freq = np.fft.fftfreq(D_hist.shape[-1])
plt.plot(freq[2:50],sp.real[2:50])
plt.show()
