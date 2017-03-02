import physics
import numpy as np

class system:
    def __init__(self,
                 initial_pos,
                 initial_vel,
                 box_size):
        self.state_pos = (initial_pos) % box_size
        self.state_vel = initial_vel
        self.box_size = box_size
        self.time = 0

        # initial force
        r_x, r_y, D = physics.normal_vec_2d(self.state_pos, self.box_size)
        self.forces = physics.find_force(r_x, r_y, D)

        # initial energies
        self.potential_energy =  physics.leonard_jones_potential(D).sum()
        self.kinetic_energy = np.sum(self.state_vel[:,0]**2) + np.sum(self.state_vel[:,1]**2)

    def step(self, dt):
        # Step uses velocity_verlet algoithm to evolve the system
        self.time += dt

        # update postion
        self.state_pos = (self.state_pos + dt*self.state_vel + dt**2*self.forces/2 ) % self.box_size

        r_x, r_y, D = physics.normal_vec_2d(self.state_pos, self.box_size)
        f = physics.find_force(r_x, r_y, D)

        # update velocities
        self.state_vel = self.state_vel + dt/2*(self.forces + f)
        # save force for next iteration
        self.forces = f

        # calculate the energies
        self.potential_energy =  physics.leonard_jones_potential(D).sum()
        self.kinetic_energy = np.sum(self.state_vel[:,0]**2) + np.sum(self.state_vel[:,1]**2)
