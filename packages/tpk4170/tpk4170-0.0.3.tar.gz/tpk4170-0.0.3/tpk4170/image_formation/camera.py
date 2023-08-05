import numpy as numpy


def project(obj_points, rvec, tvec, camera_matrix, dist_coeffs):
    obj = np.vstack((obj_points.T, np.ones(len(obj_points))))
    T = np.eye(4)
    T[:3, :3] = cv.Rodrigues(rvec)[0]
    T[:3, 3] = tvec.ravel()
    P = np.eye(3, 4)
    K = camera_matrix
    hom = (K @ P @ T @ obj).T
    return np.array([(u/w, v/w) for u, v, w in hom])


def hom(p):
    '''Homogenous form of p'''
    return np.vstack((p.T, np.ones(len(p))))


def distort(img_points, camera_matrix, dist_coeffs):
    '''Apply distortion to image points'''
    k1, k2, p1, p2, k3 = dist_coeffs.ravel()
    ones = np.ones(len(img_points))
    p = np.vstack((img_points.T, ones))
    x = np.linalg.inv(camera_matrix) @ p
    u, v = x[:2, :]
    r = np.sqrt(u**2 + v**2)
    delta_u = u * (k1*r**2 + k2*r**4 + k3*r**6) + \
        2.*p1*u*v + p2*(r**2 + 2.*u**2)
    delta_v = v * (k1*r**2 + k2*r**4 + k3*r**6) + \
        p1*(r**2 + 2.*v**2) + 2*p2*u*v
    ud = u + delta_u
    vd = v + delta_v
    xd = np.vstack((ud, vd, ones))
    pd = camera_matrix @ xd
    return pd.T[:, :2]
