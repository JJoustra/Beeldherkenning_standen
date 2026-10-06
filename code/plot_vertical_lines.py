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

i=1
thr = 34
for filepath in files:
    print("processing file:")
    print(filepath.parent.name)
    print(i)
    i = i+1
    image = cv2.imread(filepath)
    edges = cv2.Canny(image, thr, thr*3, 3)
    filtered = cv2.filter2D(edges, ddepth=-1, kernel=kernel)
    whitePix = np.sum(filtered == 255)

    imgData = pd.DataFrame({
        "folder": [filepath.parent.name],
        "vertCount": [whitePix]
    })
    data = pd.concat([data, imgData])
    
print("done")
sns.violinplot(data=data, x="folder", y="vertCount", inner="quart")
    