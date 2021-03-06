import numpy as np
from scipy.spatial.distance import pdist, squareform




def get_force(N, r, L) :
    # D is matrix containing the distances from a point to all points in each row
    D = np.zeros((N, N))
    vecs = np.zeros((N, N,r.shape[-1]))

    # TODO optimize this loop
    for i in range(N) :
        vecs[i] = r[i] - r
    # vecs = np.array([r - i for i in r])

    # Image distance calculations
    vecs = ( vecs + L/2. ) % L - L/2.
    # vecs[vecs > L/2.] *= -1
    D = np.linalg.norm(vecs, axis = 2)

    # remove 0s from distance to be able to normalize
    D[D == 0] = 1

    # divides vectors by its distance by using python magic
    # r_norm normalized vectors from a point to the rest in each row
    f = np.einsum("ijk, ij -> ijk", vecs, leonard_jones_force_norm(D))

    # Sum all components of each particle into a vector
    f = np.sum(f, axis = 1)

    return f, D


def leonard_jones_force(r) :
    return 4*((12./r**13) - (6./r**7))

def leonard_jones_force_norm(r) :
    return 4*((12./r**14) - (6./r**8))

def leonard_jones_potential(r) :
    return 4.*((1./r**12) - (1./r**6))
