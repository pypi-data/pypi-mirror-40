#!/usr/bin/env python
# Copyright (c) NTNU, Norwegian University of Science and Technology
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from setuptools import setup, find_packages

setup(name='tpk4170',
      version='0.0.3',
      description='Python modules for the course TPK4170 Robotics at NTNU ',
      author='Lars Tingelstad',
      author_email='lars.tingelstad@ntnu.no',
      url='',
      download_url='https://github.com/tingelst/tpk4170-robotics/archive/master.zip',
      packages=find_packages(),
      install_requires=[
          'numpy>=1.15.0',
          'matplotlib>=3.0.0',
          'pycollada>=0.4.1',
          'pythreejs>=2.0.0',
          'opencv-python>=3.4.4',
          'mypy>=0.630',
          'typing_extensions>=3.6.6'
      ],
      data_files=[
          ('share/tpk4170/models/ur5/visual/',
           [
               'tpk4170/models/ur5/visual/base.dae',
               'tpk4170/models/ur5/visual/forearm.dae',
               'tpk4170/models/ur5/visual/shoulder.dae',
               'tpk4170/models/ur5/visual/upperarm.dae',
               'tpk4170/models/ur5/visual/wrist1.dae',
               'tpk4170/models/ur5/visual/wrist2.dae',
               'tpk4170/models/ur5/visual/wrist3.dae',
           ]),
          ('share/tpk4170/models/kr6r900sixx/visual/',
           [
               'tpk4170/models/kr6r900sixx/visual/base_link.dae',
               'tpk4170/models/kr6r900sixx/visual/link_1.dae',
               'tpk4170/models/kr6r900sixx/visual/link_2.dae',
               'tpk4170/models/kr6r900sixx/visual/link_3.dae',
               'tpk4170/models/kr6r900sixx/visual/link_4.dae',
               'tpk4170/models/kr6r900sixx/visual/link_5.dae',
               'tpk4170/models/kr6r900sixx/visual/link_6.dae',
           ]),
          ('share/tpk4170/models/kr16_2/visual/',
           [
               'tpk4170/models/kr16_2/visual/base_link.dae',
               'tpk4170/models/kr16_2/visual/link_1.dae',
               'tpk4170/models/kr16_2/visual/link_2.dae',
               'tpk4170/models/kr16_2/visual/link_3.dae',
               'tpk4170/models/kr16_2/visual/link_4.dae',
               'tpk4170/models/kr16_2/visual/link_5.dae',
               'tpk4170/models/kr16_2/visual/link_6.dae',
           ]),
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
