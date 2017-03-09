import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model

# initial setup
rho = .88
T = 1.
dim = 3
dt = .004

# Storage for energy data
E_kin = np.array([])
E_pot = np.array([])
pressure = np.array([])
E_kin_var = np.array([])
E_pot_var = np.array([])


# initialize object system
system = model.system(rho, T, dim)

for i in range(3) :
    for j in range(200) :
        system.step(dt)
    system.equilibrate()

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
    global box, rect, dt, ax, E_kin, E_pot, E_kin_var, E_pot_var, pressure, fig
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


    # pressure = np.append(pressure, system.pressure)

    return particles, rect


ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=10, blit=True, init_func=init)


plt.show()


r_norm, D = physics.normal_vecs(system.state_pos, box_size)
print(E_kin)
# Save data
np.save("data/KE.npy", E_kin)
np.save("data/U.npy", E_pot)
np.save("data/P.npy", pressure)
np.save("data/D.npy", D)
