import os
from glob import glob
import numpy as np
import cv2 as cv


def load_images(mask='./data/images/image??.png'):
    '''Load images in sorted order based on filename'''
    img_names = glob(mask)
    img_names.sort(key=lambda s: int(os.path.basename(s)[5:-4]))
    img_list = [cv.imread(img_name, 0) for img_name in img_names]
    return img_list


def load_rob_poses(mask='./data/poses/pose??.txt'):
    '''Load poses in sorted order based on filename'''
    pose_names = glob(mask)
    pose_names.sort(key=lambda s: int(os.path.basename(s)[4:-4]))
    rob_pose_list = [np.loadtxt(pose_name) for pose_name in pose_names]
    return rob_pose_list
