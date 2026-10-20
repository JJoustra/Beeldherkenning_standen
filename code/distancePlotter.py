# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:55:00 2026

@author: Jelle J
"""

import cv2 
import numpy as np
from pathlib import Path
import pandas as pd
import seaborn as sns
import math

#functie opzet ================================================================
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

#globale variabelen ===========================================================
files = sorted(Path("test_fotos/training").rglob("*.jpg"))
if not files:
    raise SystemExit("No images found")
data = pd.dataFrame()
    
#main logica loop =============================================================
for idx in range(0, len(files)):
    
    #fetch paden voor voor- en zijaanzicht
    #deze logica heeft de meeste moeite gekost van dit hele project
    path = files[idx]
    if path.parent.name == "Zij":
        continue
    imageF = cv2.imread(path)           #front view
    imageS = cv2.imread(files[idx+200]) #side view
    print("reading:")
    print(path.parent.name)
    
    masked = skinmask(imageF)
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
        x1[i]= x     
        x2[i]= x + w    
        y1[i] = y
        y2[i] = y + h
        
    for i in range(1, len(x1)):
        
        