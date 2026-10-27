# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 23:26:18 2026

@author: Jelle J
"""

import joblib
import cv2
import numpy as np
from pathlib import Path
import math


#functie opzet ================================================================
kernel = np.ones((5,5),np.uint8)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
color = ('b','g','r')
clf = joblib.load("GBDT_Classifier.joblib")
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

def countBones(image):
    both = cv2.bitwise_or(pakmask(image), skinmask(image), mask=None)
    both = cv2.cvtColor(both, cv2.COLOR_BGR2GRAY)
    both = np.where(both != 0, 255, 0).astype(np.uint8)

    blimage =  cv2.medianBlur(both, 85) # image,kernel size    
    image_gray = both
        # Threshold the image
    ret,image_gray = cv2.threshold(blimage, 127, 255, 0)

    # Step 1: Create an empty skeleton
    #size = np.size(image_gray)
    skel = np.zeros(image_gray.shape, np.uint8)

        # Repeat steps 2-4
    while True:
        #Step 2: Open the image
        open = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, element)
        #Step 3: Substract open from the original image
        temp = cv2.subtract(image_gray, open)
        #Step 4: Erode the original image and refine the skeleton
        erosion = cv2.erode(image_gray, element)
        skel = cv2.bitwise_or(skel,temp)
        image_gray = erosion.copy()
        # Step 5: If there are no white pixels left ie.. the image has been completely eroded, quit the loop

        if cv2.countNonZero(image_gray)==0:
            break
    whiteP = np.sum(skel==255)
    return (whiteP)

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

def getDistances(image):
    masked = skinmask(image)
    gray= cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY)  
    blimage =  cv2.medianBlur(gray, 63)
    edges= cv2.Canny(blimage, 50,200)
    
    contours, hierarchy= cv2.findContours(
        edges, 
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
    
    dist = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(1, len(x1)):
        dist[i] = pythagoras(x1[0],y1[0],x1[i],y1[i])
    for i in range(2, len(x1)):
        dist[i] = pythagoras(x1[1],y1[1],x1[i],y1[i])
    for i in range(3, len(x1)):
        dist[i] = pythagoras(x1[2],y1[2],x1[i],y1[i])
    for i in range(4, len(x1)):
        dist[i] = pythagoras(x1[3],y1[3],x1[i],y1[i])
    for i in range(5, len(x1)):
        dist[i] = pythagoras(x1[4],y1[4],x1[i],y1[i])
    
    avgDist = np.average(dist)
    highestDist = sorted(dist, reverse=True)[0]
    
    return (dist, avgDist, highestDist)

def nothing(x):
    pass
#directory
files = sorted(Path("test_fotos/validatie").rglob("*.jpg"))
if not files:
    raise SystemExit("No images found")
#windows
cv2.namedWindow("bars", cv2.WINDOW_NORMAL)
cv2.namedWindow("selected_image", cv2.WINDOW_FREERATIO)
cv2.createTrackbar("img", "bars", 0, len(files) - 1, nothing)

    
current = -1
while True:
    idx = cv2.getTrackbarPos("img", "bars")

    #check of een nieuwe foto is geselecteerd. 
    #laad dat en de andere invalshoek in
    if idx != current:
        imageF = cv2.imread(files[idx])
        imageS = cv2.imread(files[idx+9])
        if imageF is not None:
            images = cv2.hconcat(imageF, cv2.imread(files[idx+9]))
            cv2.imshow("loaded_image", images)
        current = idx   
    
    whiteF = countBones(imageF)
    whiteS = countBones(imageS)
    distF, avgF, highF = getDistances(imageF)
    distS, avgS, highS = getDistances(imageS)

    avgDiff = avgF - avgS
    topDiff = highF - highS
    skelDiff = whiteF - whiteS
    
    #
    X = ["gem_afstand_V","gem_afstand_Z","langste_V","langste_Z","verschil_gem","verschil_top","WittePixels_Voor","wittePixels_Zij","verschil_wittePixels"],
    [whiteF, whiteS, skelDiff, avgF, avgS, highF, highS, avgDiff, topDiff]
    y_pred = clf.predict(X)
    print(y_pred)
    
    while True:
        if cv2.waitKey(30) & 0xFF == 27:   # Esc to exit
            break
    
    if cv2.waitKey(30) & 0xFF == 27:   # Esc to exit
        break

cv2.destroyAllWindows()
    
    