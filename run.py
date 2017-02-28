import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model

# initial setup


N = 2
# np.random.seed(0)
box_size = 5
init_pos = 10*np.random.random((N, 2))
init_vel = 0*np.random.random((N, 2))


system = model.system(init_pos, init_vel, box_size, physics.velocity_verlet, physics.leonard_jones)
dt = 1. / 100.


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
    global box, rect, dt, ax, fig
    system.step(dt)

    ms = int(fig.dpi * 2 * box_size * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])

    # update pieces of the animation
    rect.set_edgecolor('k')
    particles.set_data(system.state_pos[:, 0], system.state_pos[:, 1])
    # particles.set_markersize(ms)
    return particles, rect

ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=10, blit=True, init_func=init)


plt.show()
