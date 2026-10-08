# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:09:20 2026

@author: Jelle J
"""

import cv2 
import numpy as np
from pathlib import Path
import pandas as pd
import seaborn as sns


def nothing(x):
    pass


# Build the file list once
files = sorted(Path("test_fotos").rglob("*.jpg"))
if not files:
    raise SystemExit("No images found")
current = -1

data = pd.DataFrame()

# =============================================================================
# kernel1 = np.array([
#     [0,  0,  0],
#     [1, -2,  1],
#     [0,  0,  0]
# ], dtype=np.float32)
# 
# kernel2 = np.array([
#     [0,  0,  0,  0,  0],
#     [1, 1,  -4,  1,  1],
#     [0,  0,  0,  0,  0]
# ], dtype=np.float32)
# 
# kernel3 = np.array([
#     [0,0,0,0,0,0,0],
#     [1,1,1,-6,1,1,1],
#     [0,0,0,0,0,0,0]
# ], dtype=np.float32)
# =============================================================================
kernel = np.array([
    [0,0,0,0,0,0,0,0,0],
    [1,1,1,1,-8,1,1,1,1],
    [0,0,0,0,0,0,0,0,0]
], dtype=np.float32)

#init index telvariabel
idx=1
#vaste defines voor de masks en thresholding
thr = 38
hMin = 0
sMin = 0
vMin = 121
hMax = 255
sMax = 255
vMax = 255
BMin = 23
GMin = 54
RMin = 50
BMax = 255
GMax = 255
RMax = 255
ksize = 3
folder = 0
#main loop, bouwt het dataframe
for filepath in files:
    print("processing file:")
    print(filepath.parent.name)
    print(filepath.parent.parent.name)
    print(idx)
    idx = idx+1
    if folder != filepath.parent.name:
        folder = filepath.parent.name
        idx = 0
    image = cv2.imread(filepath)
    
    BGRlower = np.array([BMin, GMin, RMin])
    BGRupper = np.array([BMax, GMax, RMax])
    BGRmask = cv2.inRange(image, BGRlower, BGRupper)
    BGRresult = cv2.bitwise_and(image, image, mask=BGRmask)
    HSVlower = np.array([hMin, sMin, vMin])
    HSVupper = np.array([hMax, sMax, vMax])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    HSVmask = cv2.inRange(hsv, HSVlower, HSVupper)
    
    result = cv2.bitwise_and(BGRresult, BGRresult, mask=HSVmask)
    
    edges = cv2.Canny(result, thr, thr*3, 3)
    filtered = cv2.filter2D(edges, ddepth=-1, kernel=kernel)
    whitePix = np.sum(filtered == 255)

    imgData = pd.DataFrame({
        "index": idx,
        "folder": [filepath.parent.name],
        "vertCount": [whitePix]
    })
    data = pd.concat([data, imgData])
    
data.to_csv("out.csv", index=False)
print("done")



sns.violinplot(data=data, x="folder", y="vertCount", inner="quart")
    