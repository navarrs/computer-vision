'''
Q4.1:
    1. Integrating everything together.
    2. Loads necessary files from ../data/ and visualizes 3D reconstruction using scatter
'''
from submission import (
    eightpoint,
    essentialMatrix, 
    triangulate
)
from helper import (
    displayEpipolarF,
    epipolarMatchGUI,
    camera2
)
import numpy as np
import cv2
import os 

OUTDIR = "../out/"
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

I1 = cv2.imread("../data/im1.png")
I2 = cv2.imread("../data/im2.png")

# Find the fundamental matrix
M = max(I1.shape[0], I1.shape[1])
with np.load("../data/some_corresp.npz") as data:
    pts1 = data['pts1']
    pts2 = data['pts2']


F = eightpoint(pts1=pts1, pts2=pts2, M=M)
np.savez(os.path.join(OUTDIR, "F.npz"), F=F)
print(f"F:\n{F}")

I1 = I1[::, ::, ::-1]
I2 = I2[::, ::, ::-1]

displayEpipolarF(I1, I2, F)