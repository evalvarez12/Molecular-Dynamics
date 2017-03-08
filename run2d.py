import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model

# initial setup
rho = 2
T = 100

# set parameters
box_size = 5
n = int(np.sqrt(box_size**2*rho))
N = n**2

# initial positions in a equally spaced mesh
ipos = np.linspace(0, box_size - box_size/n,n)
m = np.meshgrid(ipos,ipos)
m = np.stack((m[0],m[1]), axis = 2)
m = np.concatenate((m[:]))
init_pos = m

# initial velocities
# init_vel = 10000*(1-2*np.random.random((N, 2)))
init_vel = np.random.normal(0,np.sqrt(T),(N,2))

# Storage for energy data
E_kin = np.array([])
E_pot = np.array([])
E_kin_var = np.array([])
E_pot_var = np.array([])


# initialize object system
system = model.system(init_pos, init_vel, box_size)
dt = 1. / 100000.


# set up figure and animation
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


    print("Total Energy = ",system.kinetic_energy + system.potential_energy)




    # particles.set_markersize(ms)
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
