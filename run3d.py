import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import physics
import model

# initial setup

n = 7
N = n**3
box_size = 5

# initialize in mesh
ipos = np.linspace(0, box_size - 1,n)
m = np.meshgrid(ipos,ipos,ipos)
m = np.stack((m[:]), axis = 3)
m = np.concatenate(np.concatenate((m), axis = 1))

# initial pos and vel
init_pos = m
init_vel = 10000*(1-2*np.random.random((N, 3)))


system = model.system(init_pos, init_vel, box_size)
dt = 1. / 100000000.


# set up figure and animation
while 1 :
    system.step(dt)
    print(system.kinetic_energy + system.potential_energy)
