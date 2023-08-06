from __future__ import print_function
import tigre
import numpy as np
import tigre.demos.Test_data.data_loader as data_loader
from matplotlib import pyplot as plt
import tigre
import tigre.algorithms as algs
from tigre.utilities.Ax import Ax
import matplotlib.gridspec as gridspec
from tigre.algorithms.iterative_recon_alg import IterativeReconAlg
# ---------------GEOMETRY---------------------------

geo = tigre.geometry_default(high_quality=False)
source_img = data_loader.load_head_phantom(number_of_voxels=geo.nVoxel)
geo.mode = 'cone'
# ---------------------ANGLES-------------------------

angles_1 = np.linspace(0, 2 * np.pi, 100, dtype=np.float32)
angles_2 = np.ones((100), dtype=np.float32) * np.array(np.pi / 4, dtype=np.float32)
angles_3 = np.zeros((100), dtype=np.float32)
angles = np.vstack((angles_1, angles_3, angles_3)).T

# --------------------PROJECTION----------------------
proj_1 = Ax(source_img, geo, angles, 'interpolated')

# --------------------BACK PROJECTION ----------------

algslist = ['sart',
           'sirt',
           'ossart',
           'iterativereconalg',
           'asd_pocs',
            'fdk']


def group_plot(list_of_algs):
    fig = plt.figure(figsize=(7, 9))
    gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[1, 1, 1])
