import physics
import numpy as np

class system:
    def __init__(self, rho, T, dim) :
        # Initial setup
        self.time = 0
        self.dim = dim
        self.box_size = 10
        self.equilibrium = False
        n = int(round(((self.box_size**dim)*rho)**(1./dim)))
        self.N = n**dim
        self.T = T
        self.V = self.box_size**dim

        # Distribute velocities and positions
        self.state_pos = self.set_positions(n, dim)
        self.state_vel = np.random.normal(0,np.sqrt(2./3. * T),(self.N,dim))

        # initial force
        r_norm, D = physics.normal_vecs(self.N, self.state_pos, self.box_size)
        self.forces = physics.find_force(r_norm, D)

        # initial measurements
        self.get_quantities(D)



    def set_positions(self, n, dim) :
        # initial positions in a equally spaced mesh
        ipos = np.linspace(0, self.box_size - self.box_size/n,n)

        if dim == 2 :
            ipos = np.meshgrid(ipos, ipos)
            ipos = np.stack((ipos[:]), axis = dim)
            ipos = np.concatenate((ipos))

        if dim == 3 :
            ipos = np.meshgrid(ipos, ipos, ipos)
            ipos = np.stack((ipos[:]), axis = dim)
            ipos = np.concatenate((np.concatenate((ipos), axis = 1)))

        return ipos

    def step(self, dt) :
        # Step uses velocity_verlet algoithm to evolve the system
        self.time += dt

        # update postion
        self.state_pos = (self.state_pos + dt*self.state_vel + dt**2*self.forces/2 ) % self.box_size

        r_norm, D = physics.normal_vecs(self.N, self.state_pos, self.box_size)
        f = physics.find_force(r_norm, D)

        # update velocities
        self.state_vel = self.state_vel + dt/2*(self.forces + f)
        # save force for next iteration
        self.forces = f

        # calculate the macroscopic quantities
        self.get_quantities(D)


    def get_quantities(self, D) :
        self.potential_energy =  self.get_potential_energy(D)
        self.kinetic_energy = self.get_kinetic_energy()
        self.pressure = self.get_pressure(D)
        self.temperature = self.get_temperature()

    def equilibrate(self) :
        lamb = np.sqrt((self.N - 1) * self.T / self.kinetic_energy)
        self.state_vel = self.state_vel * lamb

    def get_kinetic_energy(self) :
        return  np.sum(self.state_vel**2)/2.

    def get_potential_energy(self, D) :
        E = physics.leonard_jones_potential(D)
        np.fill_diagonal(E, 0)
        return  np.sum(E)/2.

    def get_pressure(self, D) :
        f = physics.leonard_jones_force(D)
        virial = np.sum(np.triu(f)*D)
        return virial/(3* self.V * self.T) + self.N*self.T/self.V

    def get_temperature(self) :
        return np.average(np.linalg.norm(self.state_vel , axis = -1)**2)/self.dim
