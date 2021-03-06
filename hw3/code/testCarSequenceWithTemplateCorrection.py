import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
# write your script here, we recommend the above libraries for making your animation
from LucasKanade import LucasKanade as LK

parser = argparse.ArgumentParser()
parser.add_argument('--num_iters', type=int, default=1e4,
                    help='number of iterations of Lucas-Kanade')
parser.add_argument('--threshold', type=float, default=1e-2,
                    help='dp threshold of Lucas-Kanade for terminating optimization')
parser.add_argument('--template_threshold', type=float, default=5,
                    help="threshold for template correction")
parser.add_argument('--visualize', action='store_true')
args = parser.parse_args()
num_iters = args.num_iters
threshold = args.threshold
template_threshold = args.template_threshold

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.axis('off')

# OUT_DIR = "../result/q1-4_carseq"
# if not os.path.exists(OUT_DIR):
#     os.makedirs(OUT_DIR)

with open("../result/carseqrects.npy", 'rb') as f:
    carseqrects = np.load(f)

#
# MAIN ------------
seq = np.load("../data/carseq.npy")
car_rects = np.zeros((seq.shape[2], 4))
capture = [1, 100, 200, 300, 400]

T0 = seq[:, :, 0]
rect0 = [59., 116., 145., 151.]

T = seq[:, :, 0]
rect = [59., 116., 145., 151.]

pn_ = np.zeros(2)
pn_1 = np.zeros(2)

car_rects[0] = rect
for i in range(1, seq.shape[2]):

    # Perform gradient descent starting at p = pn-1
    # pn = minp sum[In(W(x:p)) - Tn(x)]**2 
    pn = LK(T, seq[:, :, i], rect, threshold, num_iters, pn_1)

    # pn_s = minp sum[In(W(x:p)) - T1(x)]**2   with p = pn
    pn_[0] = rect[0] + pn[0] - rect0[0]
    pn_[1] = rect[1] + pn[1] - rect0[1]
    pn_s = LK(T0, seq[:, :, i], rect0, threshold, num_iters, pn_)
    # print(f"pn {pn} pn* {pn_s}")

    if np.linalg.norm(pn_s - pn_) <= template_threshold:
        # Similar to q1.3: Update template and set p = 0
        T = seq[:, :, i]
        pn_1[:] = 0.0
        
        # Correct drift 
        pn_s[0] = rect0[0] + pn_s[0] - rect[0]
        pn_s[1] = rect0[1] + pn_s[1] - rect[1]

        rect[0] += pn_s[0]
        rect[1] += pn_s[1]
        rect[2] += pn_s[0]
        rect[3] += pn_s[1]
    else:
        # Only accumulate distance
        pn_1 = pn

    car_rects[i, :] = rect

    # Save images falling in this condition
    if i in capture:
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        tcr = plt.Rectangle((rect[0], rect[1]),
                          height=h, width=w, ec='r', lw=3, fill=False)
        
        rect_ = carseqrects[i]
        w = rect_[2] - rect_[0]
        h = rect_[3] - rect_[1]
        r = plt.Rectangle((rect_[0], rect_[1]),
                          height=h, width=w, ec='b', lw=3, fill=False)

        plt.imshow(seq[:, :, i], cmap='gray')
        ax.add_patch(r)
        ax.add_patch(tcr)
        plt.pause(0.2)
        plt.draw()
        plt.savefig(f"../result/carseqwcrt_{i}.png",
                    bbox_inches='tight', pad_inches=0)
        r.remove()
        tcr.remove()

plt.close()

with open("../result/carseqrects-wcrt.npy", "wb") as f:
    np.save(f, car_rects)

#
# SANITY CHECK -----------------------------------------------------------------
if args.visualize:
    with open("../result/carseqrects-wcrt.npy", 'rb') as f:
        tc_rects = np.load(f)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for i in range(seq.shape[2]):
        rect = tc_rects[i]
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        tcr = plt.Rectangle((rect[0], rect[1]),
                            height=h, width=w, ec='r', lw=2, fill=False)
        ax.add_patch(tcr)

        rect = carseqrects[i]
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        r = plt.Rectangle((rect[0], rect[1]),
                          height=h, width=w, ec='b', lw=2, fill=False)
        ax.add_patch(r)
        plt.imshow(seq[:, :, i], cmap='gray')
        plt.pause(0.01)
        plt.draw()
        r.remove()
        tcr.remove()
    plt.close()
