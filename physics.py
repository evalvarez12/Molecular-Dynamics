import numpy as np
from scipy.spatial.distance import pdist, squareform


# TODO 2d and 3d funcs should be one generalized
def normal_vecs(r, L) :
    # TODO optimize min distance
    # D is matrix containing the distances from a point to all points in each row
    D = np.zeros((len(r),len(r)))
    vecs = np.zeros((len(r),len(r),2))

    for i in range(len(r)) :
        vecs[i] = r[i] - r
    # vecs = np.array([r - i for i in r])

    vecs = ( vecs + L/2. ) % L - L/2.
    vecs[vecs > L/2.] *= -1
    D = np.linalg.norm(vecs, axis = 2)

    D[D == 0] = 1

    # divides vectors by its distance by using python magic
    r_norm = np.einsum("ijk, ij -> ijk", vecs, 1./D)

    # r_norm normalized vectors from a point to the rest in each row
    return r_norm, D

def find_force(r_norm, D) :

    # Get the forces
    f = np.einsum("ijk, ij -> ijk", r_norm, leonard_jones(D))

    # Sum all components of each particle into a vector
    f = np.sum(f, axis = 1)

    return f


def leonard_jones(r) :
    return -4*(-(12./r**13) + (6./r**7))



def leonard_jones_potential(r) :
    return 4.*((1./r**12) - (1./r**6))
