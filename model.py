import physics
import numpy as np

class system:
    def __init__(self,
                 initial_pos,
                 initial_vel,
                 box_size):
        self.state_pos = initial_pos
        self.state_vel = initial_vel
        self.box_size = box_size
        self.time = 0

    def step(self, dt):
        self.time += dt

        # update state
        self.state_pos, self.state_vel, self.potential_energy = physics.velocity_verlet(self.state_pos, self.state_vel, self.box_size, dt)
        self.kinetic_energy = np.sum(self.state_vel[:,0]**2) + np.sum(self.state_vel[:,1]**2)
        # correct position for box_size
        self.state_pos = self.state_pos % self.box_size
