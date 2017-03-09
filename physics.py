import numpy as np
from scipy.spatial.distance import pdist, squareform


def kinetic_energy(vel) :
    return  np.sum(vel**2)/2.

def potential_energy(D) :
    E = leonard_jones_potential(D)
    np.fill_diagonal(E, 0)
    return  np.sum(E)/2.

def pressure(N, D, V, T) :
    f = leonard_jones_force(D)
    np.fill_diagonal(f, 0)
    virial = np.sum(f*D)/2.
    return virial/(3*V * T) + N*T/V

def temperature(vel) :
    # TODO The 3 is because dim = 3
    return np.average(np.linalg.norm(vel , axis = -1)**2)/3.

def normal_vecs(N, r, L) :
    # D is matrix containing the distances from a point to all points in each row
    D = np.zeros((N, N))
    vecs = np.zeros((N, N,r.shape[-1]))

    # TODO optimize this loop
    for i in range(N) :
        vecs[i] = r[i] - r
    # vecs = np.array([r - i for i in r])

    # Image distance calculations
    vecs = ( vecs + L/2. ) % L - L/2.
    vecs[vecs > L/2.] *= -1
    D = np.linalg.norm(vecs, axis = 2)

    # remove 0s from distance to be able to normalize
    D[D == 0] = 1

    # divides vectors by its distance by using python magic
    # r_norm normalized vectors from a point to the rest in each row
    r_norm = np.einsum("ijk, ij -> ijk", vecs, 1./D)

    return r_norm, D

def find_force(r_norm, D) :
    # Get the forces
    f = np.einsum("ijk, ij -> ijk", r_norm, leonard_jones_force(D))

    # Sum all components of each particle into a vector
    f = np.sum(f, axis = 1)

    return f


def leonard_jones_force(r) :
    return -4*(-(12./r**13) + (6./r**7))

def leonard_jones_potential(r) :
    return 4.*((1./r**12) - (1./r**6))
