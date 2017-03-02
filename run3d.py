import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model

# initial setup

n = 7
N = n**3
# np.random.seed(0)
box_size = 5
ipos = np.linspace(0, box_size - 1,n)
m = np.meshgrid(ipos,ipos,ipos)
m = np.stack((m[:]), axis = 3)
m = np.concatenate(np.concatenate((m), axis = 1))
# m= np.meshgrid(ipos,ipos)
# init_pos = np.reshape(np.stack((m[0],m[1]), axis = 2),(N,2))
init_pos = m
init_vel = 10000*np.random.random((N, 3))


system = model.system(init_pos, init_vel, box_size)
dt = 1. / 1000000.


# set up figure and animation
while 1 :
    system.step(dt)
    print(system.kinetic_energy + system.potential_energy)
