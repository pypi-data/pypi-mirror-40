import numpy as np
import ipywidgets

from tpk4170.visualization.viewer import Viewer
from tpk4170.forward_kinematics import fk_kr6r900sixx
from tpk4170.models import kr6r900sixx as kr6
from tpk4170.models import Grid, Ball


class Visualizer:
    def __init__(self, base_link, link_1, link_2,
                 link_3, link_4, link_5, link_6, fk, interact=False):
        self.viewer = Viewer()
        self.grid = Grid()
        self.viewer.add(self.grid)

        self.base_link = base_link
        self.link_1 = link_1
        self.link_2 = link_2
        self.link_3 = link_3
        self.link_4 = link_4
        self.link_5 = link_5
        self.link_6 = link_6

        self.viewer.add(self.base_link)
        self.viewer.add(self.link_1)
        self.viewer.add(self.link_2)
        self.viewer.add(self.link_3)
        self.viewer.add(self.link_4)
        self.viewer.add(self.link_5)
        self.viewer.add(self.link_6)

        self._fk = fk

        if interact:
            self.interact()

        self.show(np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

    def show(self, q, show_trajectory=False):
        T01, T02, T03, T04, T05, T06 = self._fk(q)
        self.link_1(T01)
        self.link_2(T02)
        self.link_3(T03)
        self.link_4(T04)
        self.link_5(T05)
        self.link_6(T06)

        if show_trajectory:
            ball = Ball(color='white', radius=0.01)
            ball.position = T06[:3, 3].tolist()
            self.viewer.add(ball)

    def interact(self):
        def f(q1, q2, q3, q4, q5, q6):
            q = np.array([q1, q2, q3, q4, q5, q6])
            self.show(q)

        ipywidgets.interact(f,
                            q1=(np.deg2rad(-180), np.deg2rad(180)),
                            q2=(np.deg2rad(-180), np.deg2rad(180)),
                            q3=(np.deg2rad(-180), np.deg2rad(180)),
                            q4=(np.deg2rad(-180), np.deg2rad(180)),
                            q5=(np.deg2rad(-180), np.deg2rad(180)),
                            q6=(np.deg2rad(-180), np.deg2rad(180)))


class Kr6R900SixxVisualizer(Visualizer):
    def __init__(self, interact=False, show_trajectory=False):
        Visualizer.__init__(self,
                            kr6.BaseLink(),
                            kr6.Link1(),
                            kr6.Link2(),
                            kr6.Link3(),
                            kr6.Link4(),
                            kr6.Link5(),
                            kr6.Link6(),
                            fk_kr6r900sixx,
                            interact)
