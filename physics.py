import numpy as np
from scipy.spatial.distance import pdist, squareform


def normal_vec_2d(r, L) :
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
    vecsx = vecs[:,:,0]
    vecsy = vecs[:,:,1]

    # rx and ry are matrices contining the normalized vectors from a point to the rest in each row
    rx = np.divide(vecsx,D)
    ry = np.divide(vecsy,D)
    return rx, ry, D


def find_force(r_x, r_y, D) :

    # Get the forces
    f_x = np.multiply(r_x,leonard_jones(D))
    f_y = np.multiply(r_y,leonard_jones(D))

    # Sum all components of each particle into a vector
    f = []
    for i in range(len(D)) :
        f += [[np.sum(f_x[i]),np.sum(f_y[i])]]
    f = np.array(f)

    return f


def leonard_jones(r) :
    return -4*(-(12./r**13) + (6./r**7))



def leonard_jones_potential(r) :
    return 4.*((1./r**12) - (1./r**6))
