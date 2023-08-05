import numpy as np

I = np.eye(3)


def vec(a, b, c):
    return np.array([[a], [b], [c]])


def skew(v):
    return np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]])


def vee(S):
    return vec([S[2, 1], S[0, 2], S[1, 0]])


def exp(v):
    angle = np.linalg.norm(v)
    S = skew(v / angle)
    return I + np.sin(angle) * S + (1 - np.cos(angle)) * S @ S
