import numpy as np
from tpk4170.forward_kinematics import Jacobian


def ik_analytical_ur5(trf, shoulder=-1, elbow=1, wrist=-1):

    a = [0.00000, -0.42500, -0.39225,  0.00000,  0.00000,  0.0000]
    d = [0.089159,  0.00000,  0.00000,  0.10915,  0.09465,  0.0823]

    Te = trf
    ne, se, ae, pe = Te[:3, :].T

    d1, _, _, d4, d5, d6 = d
    _, a2, a3, _, _, _ = a

    L2 = a2
    L3 = a3

    p5 = pe - d6 * ae
    p5x, p5y, _ = p5

    psi5 = np.arctan2(shoulder * p5y, shoulder * p5x)
    offset1 = np.arctan2(d4, np.sqrt(p5x*p5x + p5y*p5y - d4*d4))

    q1 = psi5 + shoulder * offset1

    x1 = np.array([np.cos(q1), np.sin(q1), 0])
    y1 = np.array([0, 0, 1])
    z1 = np.array([np.sin(q1), -np.cos(q1), 0])

    z4 = wrist * shoulder * np.cross(z1, ae)
    z4 /= np.linalg.norm(z4)
    y4 = z1
    x4 = np.cross(y4, z4)

    q5 = np.arctan2(np.inner(-ae, x4), np.inner(ae, y4))

    q6 = np.arctan2(np.inner(-z4, ne), np.inner(-z4, se))

    p3x, p3y, p3z = p5 - d5 * z4 - d4 * z1

    pv = p3z - d1
    ph = shoulder * np.sqrt(p3x*p3x + p3y*p3y)

    q234 = np.arctan2(np.inner(z4, x1), np.inner(z4, -y1))

    c3 = (ph*ph + pv*pv - L2*L2 - L3*L3) / (2 * L2 * L3)
    s3 = elbow * np.sqrt(1.0 - c3*c3)
    q3 = np.arctan2(s3, c3)

    c2 = (ph * (L2 + L3*c3) + pv*L3*s3) / (L2*L2 + L3*L3 + 2*L2*L3*c3)
    s2 = (pv * (L2 + L3*c3) - ph*L3*s3) / (L2*L2 + L3*L3 + 2*L2*L3*c3)
    q2 = np.arctan2(s2, c2)

    q4 = q234 - (q2 + q3)
    if q4 > np.pi:
        q4 -= 2 * np.pi

    return np.array([q1, q2, q3, q4, q5, q6])


def ik_iterative(trf, fk, q0=np.array([1, 1, 1, 1, 1, 1])):
    Rd = trf[:3, :3]
    qk = q0
    qs = []
    for i in range(1000):
        Ts = fk(qk)
        Tk = Ts[5]
        Jk = Jacobian(Ts)
        Rk = Tk[:3, :3]
        Re = Rd @ Rk.T
        ep = trf[:3, 3] - Tk[:3, 3]
        eo = np.array([Re[2, 1] - Re[1, 2],
                       Re[0, 2] - Re[2, 0],
                       Re[1, 0] - Re[0, 1]]) * 0.5

        e = np.array((ep, eo)).reshape(6, 1)

        K = 0.1
        dq = K * np.dot(np.linalg.pinv(Jk), e).ravel()
        qk = qk + dq
        qs.append(qk)

        if np.linalg.norm(e) < 1e-6:
            break
    return qk
