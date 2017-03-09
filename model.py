import physics
import numpy as np

class system:
    def __init__(self, rho, T, dim) :
        # Initial setup
        self.time = 0
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
        self.potential_energy =  physics.potential_energy(D)
        self.kinetic_energy = physics.kinetic_energy(self.state_vel)
        self.pressure = physics.pressure(D, self.V, self.T)




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
        self.potential_energy =  physics.potential_energy(D)
        self.kinetic_energy = physics.kinetic_energy(self.state_vel)
        self.pressure = physics.pressure(D, self.V, self.T)


    def equilibrate(self) :
        lamb = np.sqrt((self.N - 1) * self.T / self.kinetic_energy)
        self.state_vel = self.state_vel * lamb
