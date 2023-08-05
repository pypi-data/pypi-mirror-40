import numpy as np
import cv2
import glob
import os
from ..util.py_utils import int_fun

def ave_mean_and_var(path):
    '''
    输入一个路径，求出路径下所有的图片的均值和方差
    '''
    meanl = []
    stdl = []
    for filename in os.listdir(path):
        if filename.split(".")[-1] in ["png", "jpg"]:
            im = cv2.imread(os.path.join(path, filename))
            meanl.append(np.mean(im))
            stdl.append(np.std(im))
        else:
            print(filename, "is not a image file")
    return sum(meanl) / len(meanl), sum(stdl) / len(stdl)


# draw bbox
def draw_box(_im, bbox, color_box=(0, 0, 0), thick_bbox=2, thick_circle=8):
    bbox = int_fun(bbox)
    im_box = cv2.rectangle(_im, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color=color_box, thickness=thick_bbox)
    im_box = cv2.circle(im_box, (bbox[0], bbox[1]), thick_circle, (0, 255, 0), -1)
    im_box = cv2.circle(im_box, (bbox[0], bbox[3]), thick_circle, (0, 255, 0), -1)
    im_box = cv2.circle(im_box, (bbox[2], bbox[1]), thick_circle, (0, 255, 0), -1)
    im_box = cv2.circle(im_box, (bbox[2], bbox[3]), thick_circle, (0, 255, 0), -1)

    im_box = cv2.circle(im_box, (bbox[0], bbox[1]), thick_circle, (0, 0, 0), 1)
    im_box = cv2.circle(im_box, (bbox[0], bbox[3]), thick_circle, (0, 0, 0), 1)
    im_box = cv2.circle(im_box, (bbox[2], bbox[1]), thick_circle, (0, 0, 0), 1)
    im_box = cv2.circle(im_box, (bbox[2], bbox[3]), thick_circle, (0, 0, 0), 1)
    return im_box
