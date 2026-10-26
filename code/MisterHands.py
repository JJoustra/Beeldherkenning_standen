# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 14:09:48 2026

@author: Jelle J
"""

import cv2
import numpy as np
from pathlib import Path
import math

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

def pythagoras(x1, x2, y1, y2):
    if x1 > x2:
        a = x1 - x2
    else:
        a = x2 - x1
        
    if y1 > y2:
        b = y1 - y2
    else:
        b = y2 - y1
    c = math.sqrt(a**2 + b**2)
    return (c)

files = sorted(Path("test_fotos/training").rglob("*.jpg"))
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
    
    #check of er genoeg contours in de foto zijn, voor als een hand/voet buiten beeld was
    if len(contours) > 6:
        num = 6
    else:
        num = len(contours)            
    
    #pak de coördinaten van alle uiterste punten van de vorm
    #doet dit voor iedere contour of max de 6 grootste contours
    x1 = np.array([0, 0, 0, 0, 0, 0])
    x2 = np.array([0, 0, 0, 0, 0, 0])
    y1 = np.array([0, 0, 0, 0, 0, 0])
    y2 = np.array([0, 0, 0, 0, 0, 0])
    for i in range(0, num):
        x,y,w,h= cv2.boundingRect(sorted_contours[i])    
        x1[i] = x     
        x2[i] = x + w    
        y1[i] = y
        y2[i] = y + h
        cv2.line(masked, (x1[i], y1[i]), (x2[i], y2[i]),(0,255,0),2)
        cv2.line(masked, (x1[i], y1[i]), (x2[i], y1[i]),(0,255,0),2)
        cv2.line(masked, (x2[i], y1[i]), (x2[i], y2[i]),(0,255,0),2)
        cv2.line(masked, (x2[i], y2[i]), (x1[i], y2[i]),(0,255,0),2)
        cv2.line(masked, (x1[i], y2[i]), (x1[i], y1[i]),(0,255,0),2)
    
    for i in range(1, len(x1)):
        cv2.line(masked, (x1[0], y1[0]), (x1[i], y1[i]), (0,0,255),1)
        print(pythagoras(x1[0], y1[0], x1[i], y1[i]))
    cv2.imshow("edges", edges)
    cv2.imshow("line_on_big_shape", masked)

    if cv2.waitKey(30) & 0xFF == 27:   # Esc to exit
        break

cv2.destroyAllWindows()