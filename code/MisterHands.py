# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 14:09:48 2026

@author: Jelle J
"""

import cv2
import numpy as np
from pathlib import Path

def skinmask(image):
    hMin = 0
    sMin = 38
    vMin = 54
    hMax = 255
    sMax = 255
    vMax = 255
    
    HSVlower = np.array([hMin, sMin, vMin])
    HSVupper = np.array([hMax, sMax, vMax])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    HSVmask = cv2.inRange(hsv, HSVlower, HSVupper)
    
    result = cv2.bitwise_and(image, image, mask=HSVmask)
    return (result)


def pakmask(image):
    hMin = 0
    sMin = 0
    vMin = 135
    hMax = 255
    sMax = 24
    vMax = 255
    
    HSVlower = np.array([hMin, sMin, vMin])
    HSVupper = np.array([hMax, sMax, vMax])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    HSVmask = cv2.inRange(hsv, HSVlower, HSVupper)
    
    HSVupper = np.array([hMax, sMax, vMax])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    HSVmask = cv2.inRange(hsv, HSVlower, HSVupper)
    
    result = cv2.bitwise_and(image, image, mask=HSVmask)
    
    return (result)

def nothing(x):
    pass



files = sorted(Path("test_fotos").rglob("*.jpg"))
if not files:
    raise SystemExit("No images found")
    
cv2.namedWindow("bars", cv2.WINDOW_FREERATIO)
cv2.namedWindow("loaded_image", cv2.WINDOW_FREERATIO)
cv2.namedWindow("edges", cv2.WINDOW_FREERATIO)
cv2.namedWindow("line_on_big_shape", cv2.WINDOW_FREERATIO)
cv2.createTrackbar("img", "bars", 0, len(files) - 1, nothing)

current = -1
while True:
    idx = cv2.getTrackbarPos("img", "bars")

    if idx != current:
        image = cv2.imread(str(files[idx]))
        if image is not None:
            cv2.imshow("loaded_image", image)
        current = idx
    
    # TODO: VIND GROOTSTE CONTOUR EN ZET ALLE PIXELS ERBUITEN OP 0
    #voeg beide maskers samen
    both = cv2.bitwise_or(pakmask(image), skinmask(image), mask=None)
    

    masked = skinmask(image)
    gray= cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY)  
    blimage =  cv2.medianBlur(gray, 63)
    edges= cv2.Canny(blimage, 50,200)
    
    contours, hierarchy= cv2.findContours(
        edges.copy(), 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_NONE
        )
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    
    item1= sorted_contours[0]
    M= cv2.moments(item1)

    x,y,w,h= cv2.boundingRect(item1)    
    x1= x     
    x2= x + w    
    y1 = y
    y2 = y + h
    cv2.line(masked, (x1, y1), (x2, y2),(0,255,0),2)
    cv2.line(masked, (x1, y1), (x2, y1),(0,255,0),2)
    cv2.line(masked, (x2, y1), (x2, y2),(0,255,0),2)
    cv2.line(masked, (x2, y2), (x1, y2),(0,255,0),2)
    cv2.line(masked, (x1, y2), (x1, y1),(0,255,0),2)
    
    cv2.imshow("edges", edges)
    cv2.imshow("line_on_big_shape", masked)

    if cv2.waitKey(30) & 0xFF == 27:   # Esc to exit
        break

cv2.destroyAllWindows()