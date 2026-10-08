# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:45:59 2026

@author: Jelle J
"""


import cv2 
import numpy as np
from pathlib import Path

def pakmask(image):
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
    BGRlower = np.array([BMin, GMin, RMin])
    BGRupper = np.array([BMax, GMax, RMax])
    BGRmask = cv2.inRange(image, BGRlower, BGRupper)
    BGRresult = cv2.bitwise_and(image, image, mask=BGRmask)
    
    HSVlower = np.array([hMin, sMin, vMin])
    HSVupper = np.array([hMax, sMax, vMax])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    HSVmask = cv2.inRange(hsv, HSVlower, HSVupper)
    
    result = cv2.bitwise_and(BGRresult, BGRresult, mask=HSVmask)
    return (result)

def skinmask(image):
    hMin = 0
    sMin = 35
    vMin = 43
    hMax = 26
    sMax = 255
    vMax = 255
    BMin = 17
    GMin = 21
    RMin = 47
    BMax = 179
    GMax = 199
    RMax = 255
    BGRlower = np.array([BMin, GMin, RMin])
    BGRupper = np.array([BMax, GMax, RMax])
    BGRmask = cv2.inRange(image, BGRlower, BGRupper)
    BGRresult = cv2.bitwise_and(image, image, mask=BGRmask)
    HSVlower = np.array([hMin, sMin, vMin])
    HSVupper = np.array([hMax, sMax, vMax])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    HSVmask = cv2.inRange(hsv, HSVlower, HSVupper)
    
    result = cv2.bitwise_and(BGRresult, BGRresult, mask=HSVmask)
    return (result)


def nothing(x):
    pass


# Build the file list once
files = sorted(Path("test_fotos").rglob("*.jpg"))
if not files:
    raise SystemExit("No images found")
current = -1

# Create windows with small custom sizes
cv2.namedWindow('imgControls', cv2.WINDOW_NORMAL)
cv2.namedWindow('blurControls', cv2.WINDOW_NORMAL)
cv2.namedWindow('edgeControls', cv2.WINDOW_NORMAL)
cv2.namedWindow('Original', cv2.WINDOW_FREERATIO)
cv2.namedWindow('Masked', cv2.WINDOW_FREERATIO)
cv2.namedWindow('canny', cv2.WINDOW_FREERATIO)

#cv2.resizeWindow('Controls', 420, 200)
#cv2.resizeWindow('Original', 500, 350)
#cv2.resizeWindow('Masked', 500, 350)

# trackbar voor image selectie
cv2.createTrackbar("img", "imgControls", 0, len(files) - 1, nothing)
# Create trackbars for color change
cv2.createTrackbar('threshold', 'edgeControls', 0, 255, nothing)
# trackbar voor blur selectie
cv2.createTrackbar('Welke_blur', 'blurControls', 0, 3 , nothing)
# trackbars voor blur instellingen
cv2.createTrackbar('XBlur', 'blurControls', 1, 50, nothing)
cv2.createTrackbar('YBlur', 'blurControls', 1, 50, nothing)

while True:    
    welke_blur = cv2.getTrackbarPos('Welke_blur', 'blurControls')
## +1 want anders kan de blur onder 0 komen en dat geeft een error en *2 want anders kan de blur op een even getal komen en dat geeft een error bij median blur
    XBlur = cv2.getTrackbarPos('XBlur', 'blurControls') *2 + 1
    YBlur = cv2.getTrackbarPos('YBlur', 'blurControls') *2 + 1

    threshold = cv2.getTrackbarPos('threshold', 'edgeControls')

    idx = cv2.getTrackbarPos("img", "imgControls")

    if idx != current:
            image = cv2.imread(str(files[idx]))

            current = idx

    result = cv2.hconcat([pakmask(image), skinmask(image)])
    both = cv2.bitwise_or(pakmask(image), skinmask(image), mask=None)
    
    blimage = result
    if welke_blur == 1:
        blimage = cv2.GaussianBlur(result, (XBlur, YBlur), 0)
    elif welke_blur == 2:
        blimage = cv2.blur(result, (XBlur, YBlur))
    elif welke_blur == 3:
        blimage = cv2.medianBlur(result, XBlur)
    
    edges = cv2.Canny(blimage, threshold, threshold*3, 3)
    sobelx = cv2.Sobel(edges,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(edges,cv2.CV_64F,0,1,ksize=5)
    
    cv2.imshow('Original', image)
    cv2.imshow('Masked', both)
    cv2.imshow('canny', edges)
    cv2.imshow('x_sobel', edges)
    cv2.imshow('y_sobel', edges)
    cv2.imshow('blur', blimage)

    if cv2.waitKey(30) & 0xFF == 27:   # Esc to exit
        break

cv2.destroyAllWindows()
