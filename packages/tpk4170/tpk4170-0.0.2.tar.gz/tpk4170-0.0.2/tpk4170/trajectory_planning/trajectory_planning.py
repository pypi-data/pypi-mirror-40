import numpy as np
import matplotlib.pyplot as plt


def plot_trajectory(trajectory, title=''):
    qs, dqs, ddqs, ts = trajectory
    f, axarr = plt.subplots(3, sharex=True)
    axarr[0].plot(ts, qs, color='red')
    axarr[0].set_title(title)
    axarr[0].set_ylabel('position')
    axarr[1].plot(ts, dqs, color='green')
    axarr[1].set_ylabel('velocity')
    axarr[2].plot(ts, ddqs, color='blue')
    axarr[2].set_ylabel('acceleration')
    axarr[2].set_xlabel('time [s]')


def quintic_trajectory(current_position, target_position,
                       current_velocity, target_velocity,
                       current_acceleration, target_acceleration,
                       duration_in_seconds):
    trajectories = []
    t = duration_in_seconds
    xs = np.linspace(0, t)
    for qi, qf, dqi, dqf, ddqi, ddqf in zip(current_position, target_position,
                                            current_velocity, target_velocity,
                                            current_acceleration, target_acceleration):
        A = np.array(
            [[0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
             [t**5, t**4, t**3, t**2, t, 1.0],
             [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
             [5. * t**4, 4. * t**3, 3. * t**2, 2. * t, 1., 0.0],
             [0.0, 0.0, 0.0, 2.0, 0.0, 0.0],
             [20. * t**3, 12. * t**2, 6. * t, 2., 0.0, 0.0]])

        b = np.array([qi, qf, dqi, dqf, ddqi, ddqf])
        x = np.linalg.solve(A, b)

        qs = np.polyval(x, xs)
        dqs = np.polyval(
            [5. * x[0], 4. * x[1], 3. * x[2], 2. * x[3], x[4]], xs)
        ddqs = np.polyval([20. * x[0], 12. * x[1], 6. * x[2], 2. * x[3]], xs)

        trajectories.append((qs, dqs, ddqs, xs))
    return trajectories


def cubic_trajectory(current_position, target_position,
                     current_velocity, target_velocity,
                     duration_in_seconds):
    trajectories = []
    t = duration_in_seconds
    ts = np.linspace(0, t)
    for qi, qf, dqi, dqf in zip(current_position, target_position,
                                current_velocity, target_velocity):
        A = np.array([[0.0, 0.0, 0.0, 1.0],
                      [t**3, t**2, t, 1.],
                      [0.0, 0.0, 1.0, 0.0],
                      [3.0 * t**2, 2*t, 1.0, 0.0]])

        b = np.array([qi, qf, dqi, dqf])
        x = np.linalg.solve(A, b)

        qs = np.polyval(x, ts)
        dqs = np.polyval([3. * x[0], 2. * x[1], x[2]], ts)
        ddqs = np.polyval([6. * x[0], 2. * x[1]], ts)

        trajectories.append((qs, dqs, ddqs, ts))
    return trajectories


class LSPBError(Exception):
    pass


def lspb_trajectory(current_position, target_position,
                    duration_in_seconds, cruise_velocity=None):

    q0 = current_position
    q1 = target_position
    tf = duration_in_seconds
    V = cruise_velocity

    ts = np.linspace(0.0, tf)

    if V is None:
        V = (q1-q0)/tf * 1.5
    else:
        V = np.abs(V) * np.sign(q1-q0)
        if np.abs(V) < np.abs(q1-q0)/tf:
            raise LSPBError('V too small')
        elif np.abs(V) > 2 * np.abs(q1-q0)/tf:
            raise LSPBError('V too big')

    if np.allclose(q0, q1):
        s = np.ones(len(ts)) * q0
        sd = np.zeros(len(ts))
        sdd = np.zeros(len(ts))
        return (s, sd, sdd)

    tb = (q0 - q1 + V*tf)/V
    a = V/tb

    p = []
    pd = []
    pdd = []

    for tt in ts:
        if tt <= tb:
            # Initial blend
            p.append(q0 + a/2*tt*tt)
            pd.append(a*tt)
            pdd.append(a)
        elif tt <= (tf - tb):
            p.append((q1+q0-V*tf)/2 + V*tt)
            pd.append(V)
            pdd.append(0.0)
        else:
            p.append(q1 - (a/2*tf*tf) + a*tf*tt - a/2*tt*tt)
            pd.append(a*tf - a*tt)
            pdd.append(-a)

    return (p, pd, pdd, ts)
