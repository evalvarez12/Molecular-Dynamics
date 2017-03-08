import physics
import numpy as np

class system:
    def __init__(self, rho, T, dim) :
        # Initial setup
        self.time = 0
        self.box_size = 5
        self.equilibrium = False
        n = int(np.sqrt(self.box_size**2*rho))
        self.N = n**2
        self.T = T

        # Distribute velocities and positions
        self.state_pos = self.set_positions(n, dim)
        self.state_vel = np.random.normal(0,np.sqrt(2./3. * T),(self.N,dim))

        # initial force
        r_norm, D = physics.normal_vecs(self.state_pos, self.box_size)
        self.forces = physics.find_force(r_norm, D)

        # initial energies
        self.potential_energy =  physics.leonard_jones_potential(D).sum()
        self.kinetic_energy = np.sum(self.state_vel[:,0]**2) + np.sum(self.state_vel[:,1]**2)



    def set_positions(self, n, dim) :
        # initial positions in a equally spaced mesh
        ipos = np.linspace(0, self.box_size - self.box_size/n,n)

        if dim == 2 :
            ipos = np.meshgrid(ipos, ipos)

        if dim == 3 :
            ipos = np.meshgrid(ipos, ipos, ipos)

        ipos = np.stack((ipos[:]), axis = dim)
        return np.concatenate((ipos[:]))

    def step(self, dt) :
        # Step uses velocity_verlet algoithm to evolve the system
        self.time += dt

        # update postion
        self.state_pos = (self.state_pos + dt*self.state_vel + dt**2*self.forces/2 ) % self.box_size

        r_norm, D = physics.normal_vecs(self.state_pos, self.box_size)
        f = physics.find_force(r_norm, D)

        # update velocities
        self.state_vel = self.state_vel + dt/2*(self.forces + f)
        # save force for next iteration
        self.forces = f

        # calculate the energies
        self.potential_energy =  np.sum(physics.leonard_jones_potential(D))
        self.kinetic_energy = np.sum(self.state_vel**2)

    def equilibrate(self, dt) :

        Ks = []
        for i in range(1000) :
            self.step(dt)

        lamb = np.sqrt((self.N - 1) * self.T / self.kinetic_energy)

        self.state_vel = self.state_vel * lamb
