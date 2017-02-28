import numpy as np
from scipy.spatial.distance import pdist, squareform

# def find_min_tor(r, L) :
#     z = np.zeros(len(r))
#     l = np.ones(len(r)) * L
#
#     r2 = r + np.stack((z,l),axis = -1)
#     r3 = r - np.stack((z,l),axis = -1)
#     r4 = r + np.stack((l,z),axis = -1)
#     r5 = r - np.stack((l,z),axis = -1)
#
#
#     D = squareform(pdist(r))[:]
#     D2 = squareform(pdist(r2))[:]
#     D3 = squareform(pdist(r3))[:]
#     D4 = squareform(pdist(r4))[:]
#     D5 = squareform(pdist(r5))[:]
#
#     D = np.min(np.stack((D, D2, D3, D4, D5), axis = -1), axis = 2)
#
#     D[D == 0] = 1
#     return D



def normal_vec_2d(r, L) :
    # D is matrix containing the distances from a point to all points in each row
    D = np.zeros((len(r),len(r)))
    vecs = np.zeros((len(r),len(r),2))

    temp = np.zeros((9,len(r),2))
    virtual = np.array([[0,L],[0,-L],[L,0],[-L,0],[L,L],[L,-L],[-L,L],[-L,-L]])


    for i in range(len(r)) :
        vecs[i] = r[i] - r
        # D[i] = np.linalg.norm(vecs[i], axis = 1)
        for v in range(len(virtual)) :
            temp[v] = vecs[i] + virtual[v]
        temp[-1] = vecs[i]
        D[i] = np.min(np.linalg.norm(temp, axis = 2), axis = 0 )
    # vecs = np.array([i - r for i in r])
    D[D == 0] = 1
    vecsx = vecs[:,:,0]
    vecsy = vecs[:,:,1]

    # rx and ry are matrices contining the normalized vectors from a point to the rest in each row
    rx = np.divide(vecsx,D)
    ry = np.divide(vecsy,D)
    return rx, ry, D


def find_force(f_func, r, L) :
    rx, ry, D = normal_vec_2d(r, L)

    # Get the forces
    fx = np.multiply(np.abs(rx),f_func(D))
    fy = np.multiply(np.abs(ry),f_func(D))
    f = []
    for i in range(len(D)) :
        f += [[np.dot(rx[i],fx[i]),np.dot(ry[i],fy[i])]]
    f = np.array(f)
    return f


def leonard_jones(r) :
    return -4*(-(12./r**13) + (6./r**7))



def leonard_jones_potential(r) :
    return 4.*((1./r**12) - (1./r**6))

def newton(x, v, L, dt, f_func) :
    f = find_force(f_func, x, L)
    x = x + dt*v
    v = v + dt*f
    return x, v


def velocity_verlet(x, v, L, dt, f_func = leonard_jones) :
    f = find_force(f_func, x, L)
    x = x + dt*v + dt**2*f
    f_new = find_force(f_func, x, L)
    v = v + dt/2*(f_new + f)
    return x, v
