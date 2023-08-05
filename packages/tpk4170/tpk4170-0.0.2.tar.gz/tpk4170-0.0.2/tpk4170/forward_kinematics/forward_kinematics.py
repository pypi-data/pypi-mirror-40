import numpy as np


def dh(a, alpha, d, theta):
    ct = np.cos(theta)
    st = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    return np.array([[ct, -st * ca,  st * sa, a * ct],
                     [st,  ct * ca, -ct * sa, a * st],
                     [0.0,      sa,       ca, d],
                     [0.0,     0.0,      0.0, 1.0]])


def fk_dh(dh_a, dh_alpha, dh_d, q_zero_offset, q):
    A1 = dh(dh_a[0], dh_alpha[0], dh_d[0], q[0] + q_zero_offset[0])
    A2 = dh(dh_a[1], dh_alpha[1], dh_d[1], q[1] + q_zero_offset[1])
    A3 = dh(dh_a[2], dh_alpha[2], dh_d[2], q[2] + q_zero_offset[2])
    A4 = dh(dh_a[3], dh_alpha[3], dh_d[3], q[3] + q_zero_offset[3])
    A5 = dh(dh_a[4], dh_alpha[4], dh_d[4], q[4] + q_zero_offset[4])
    A6 = dh(dh_a[5], dh_alpha[5], dh_d[5], q[5] + q_zero_offset[5])
    T01 = A1
    T02 = A1 @ A2
    T03 = A1 @ A2 @ A3
    T04 = A1 @ A2 @ A3 @ A4
    T05 = A1 @ A2 @ A3 @ A4 @ A5
    T06 = A1 @ A2 @ A3 @ A4 @ A5 @ A6
    return (T01, T02, T03, T04, T05, T06)


def Jacobian(Ts):
    p0 = np.array([0, 0, 0])
    z0 = np.array([0, 0, 1])
    pn = Ts[5][:3, 3]
    J = np.zeros((6, 6))
    J[:3, 0] = np.cross(z0, pn-p0)
    J[3:, 0] = z0
    for i in range(5):
        T = Ts[i]
        zi = T[:3, 2]
        pi = T[:3, 3]
        J[:3, i+1] = np.cross(zi, pn-pi)
        J[3:, i+1] = zi
    return J


def fk_ur5(q):
    a = [0.00000, -0.42500, -0.39225,  0.00000,  0.00000,  0.0000]
    d = [0.089159,  0.00000,  0.00000,  0.10915,  0.09465,  0.0823]
    alpha = [1.570796327, 0, 0, 1.570796327, -1.570796327, 0]
    q_zero_offset = [0, 0, 0, 0, 0, 0]
    return fk_dh(a, alpha, d, q_zero_offset, q)


def fk_kr6r900sixx(q):
    a = [0.025, 0.455, 0.035, 0.0, 0.0, 0.0]
    alpha = [-np.pi/2, 0.0, -np.pi/2, np.pi/2, -np.pi/2, 0.0]
    d = [0.4, 0.0, 0.0, 0.42, 0.0, 0.08]
    q_zero_offset = [0.0, 0.0, -np.pi/2, 0.0, 0.0, 0.0]
    joint_direction = [-1, 1, 1, -1, 1, -1]
    return fk_dh(a, alpha, d, q_zero_offset, q)
