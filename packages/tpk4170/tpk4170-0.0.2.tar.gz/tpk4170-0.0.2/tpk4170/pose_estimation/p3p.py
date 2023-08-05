import cv2 as cv
import numpy as np
from numpy import sqrt, dot, cross, vstack
from numpy.linalg import norm
from tpk4170.utils.transformations import unit_vector

# Implementaton of trilaterate taken from:
# https://stackoverflow.com/questions/1406375/finding-intersection-points-between-3-spheres


def trilaterate(P1, P2, P3, r1, r2, r3):
    '''
    Find the intersection of three spheres

    P1,P2,P3 are the centers, r1,r2,r3 are the radii
    '''
    temp1 = P2-P1
    e_x = temp1/norm(temp1)
    temp2 = P3-P1
    i = dot(e_x, temp2)
    temp3 = temp2 - i*e_x
    e_y = temp3/norm(temp3)
    e_z = cross(e_x, e_y)
    d = norm(P2-P1)
    j = dot(e_y, temp2)
    x = (r1*r1 - r2*r2 + d*d) / (2*d)
    y = (r1*r1 - r3*r3 - 2*i*x + i*i + j*j) / (2*j)
    temp4 = r1*r1 - x*x - y*y
    if temp4 < 0:
        raise Exception("The three spheres do not intersect!")
    z = sqrt(temp4)
    p_12_a = P1 + x*e_x + y*e_y + z*e_z
    p_12_b = P1 + x*e_x + y*e_y - z*e_z
    return vstack((p_12_a, p_12_b))


def solveP3P(obj_points, img_points, camera_matrix, dist_coeffs):
    '''
    Implementation of the solution to the P3P problem as presented in 
    Fischler and Bolles, Random Sample Consensus: A Paradigm for Model
    Fitting with Applications to Image Analysis and Automated Cartography.

    The function uses three object and image correspondences to compute a
    set of solutions. A fourth point is used as a control point. The first
    solution found is returned.
    '''

    obj_points = obj_points.reshape(-1, 3)

    img_points = cv.undistortPoints(img_points, camera_matrix, dist_coeffs)
    img_points = img_points.reshape(-1, 2)

    op = obj_points[:3].reshape(3, 3)
    ip = img_points[:3].reshape(3, 2)
    hip = np.hstack((ip, np.ones((3, 1))))

    # Compute cosines
    p, q, r = hip
    Cab = np.inner(unit_vector(p), unit_vector(q))
    Cac = np.inner(unit_vector(p), unit_vector(r))
    Cbc = np.inner(unit_vector(q), unit_vector(r))

    # Compute distances
    A, B, C = op
    Rab = np.linalg.norm(B-A)
    Rac = np.linalg.norm(C-A)
    Rbc = np.linalg.norm(C-B)

    # Compute coefficients
    K1 = Rbc**2 / Rac**2
    K2 = Rbc**2 / Rab**2
    G4 = (K1*K2-K1-K2)**2 - 4*K1*K2*Cbc**2
    G3 = 4*(K1*K2-K1-K2)*K2*(1-K1)*Cab + 4*K1 * \
        Cbc*((K1*K2-K1+K2)*Cac + 2*K2*Cab*Cbc)
    G2 = (2*K2*(1-K1)*Cab)**2 + 2*(K1*K2-K1-K2)*(K1*K2+K1-K2) + 4*K1 * \
        ((K1-K2)*Cbc**2 + K1*(1-K2)*Cac**2 - 2*(1+K1)*K2*Cab*Cac*Cbc)
    G1 = 4*(K1*K2+K1-K2)*K2*(1-K1)*Cab + 4*K1 * \
        ((K1*K2-K1+K2)*Cac*Cbc + 2*K1*K2*Cab*Cac**2)
    G0 = (K1*K2+K1-K2)**2 - 4*K1**2*K2*Cac**2

    # Solve for x
    xs = np.roots((G4, G3, G2, G1, G0))
    xs = np.real(xs[xs.imag < 1e-5])

    # Solve for lengths a, b, and c
    # Compute a and b
    as_ = Rab / np.sqrt(xs**2 - 2*xs*Cab + 1)
    bs = as_ * xs

    def y(x, a, b):
        m = 1-K1
        p = 2*(K1*Cac-x*Cbc)
        q = x**2-K1
        m_ = 1
        p_ = 2*(-x*Cbc)
        q_ = (x**2*(1-K2)+2*x*K2*Cab-K2)
        num = (p_*q - p*q_)
        den = (m*q_ - m_*q)
        return num / den

    # Compute c
    cs = y(xs, as_, bs) * as_

    # Concatenate a,b,c
    lengths = np.dstack((as_, bs, cs)).reshape(-1, 3)

    # Solve for T (the perspective center)
    Ts = []
    for (a, b, c) in lengths:
        Ts.append(trilaterate(A, B, C, a, b, c))
    Ts = np.array(Ts).reshape(-1, 3)

    # Compute lambdas
    lambdas = []
    hip_norm = np.linalg.norm(hip, axis=1)
    for T in Ts:
        lambdas.append(np.linalg.norm(op - T, axis=1) / hip_norm)
    lambdas = np.array(lambdas).reshape(-1, 3)

    # Compute R (rotation matrix)
    Rs = []
    for lambda_, T in zip(lambdas, Ts):
        V = hip.T * lambda_.reshape(3, 1)
        X = op.T - T.reshape(3, 1)
        R = V @ np.linalg.inv(X)
        Rs.append(R)

    # Return first correct solution
    rvecs = []
    tvecs = []
    cop = obj_points[3]
    cip = img_points[3]
    for R, t in zip(Rs, Ts):
        # x, y, z = (R @ cop.reshape(3, 1) + t.reshape(3, 1)).ravel()
        # if np.allclose(cip, (x/z, y/z)):
        rvecs.append(cv.Rodrigues(R)[0])
        tvecs.append(t.reshape(3, 1))

    return len(rvecs), rvecs, tvecs
