import numpy as np
from scipy.spatial.distance import pdist, squareform

def normal_vec_2d(r) :
    # D is matrix containing the distances from a point to all points in each row
    D = squareform(pdist(r))[:]
    D[D == 0] = 1


    vecs = np.array([i - r for i in r])

    vecsx = vecs[:,:,0]
    vecsy = vecs[:,:,1]

    # rx and ry are matrices contining the normalized vectors from a point to the rest in each row
    rx = np.divide(vecsx,D)
    ry = np.divide(vecsy,D)
    return rx, ry, D


def find_force(f, r) :
    rx, ry, D = normal_vec_2d(r)

    # Get the forces
    fx = np.multiply(np.abs(rx),f(D))
    fy = np.multiply(np.abs(ry),f(D))
    f = []
    for i in range(len(D)) :
        f += [[np.dot(rx[i],fx[i]),np.dot(ry[i],fy[i])]]
    f = np.array(f)
    return f


def leonard_jones(r) :
    return -4*(-(12./r**13) + (6./r**7))



def leonard_jones_potential(r) :
    return 4.*((1./r**12) - (1./r**6))

def newton(x, v, f, dt) :
    x = x + dt*v
    v = v + dt*f
    return x, v


def velocity_verlet(x, v, f, dt) :
    return x, v
