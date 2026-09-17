# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:57:18 2026

@author: Jelle J
"""

from pathlib import Path
import cv2 as cv

def nothing(x):
    pass

# Build the file list once
files = sorted(Path("test_fotos").rglob("*.jpg"))
if not files:
    raise SystemExit("No images found")

cv.namedWindow("bars", cv.WINDOW_NORMAL)
cv.namedWindow("loaded_image", cv.WINDOW_NORMAL)
cv.createTrackbar("img", "bars", 0, len(files) - 1, nothing)

current = -1
while True:
    idx = cv.getTrackbarPos("img", "bars")

    if idx != current:
        image = cv.imread(str(files[idx]))
        if image is not None:
            cv.imshow("loaded_image", image)
        current = idx

    if cv.waitKey(30) & 0xFF == 27:   # Esc to exit
        break

cv.destroyAllWindows()
    