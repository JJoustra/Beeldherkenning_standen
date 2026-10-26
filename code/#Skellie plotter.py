#Skellie plotter
from unittest import result

import cv2 
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import math

#functie opzet ================================================================
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
#define the skimask values
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

kernel = np.ones((5,5),np.uint8)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
color = ('b','g','r')


        
#globale variabelen ===========================================================
files = sorted(Path("/Users/slashure/Documents/Karate stands test fotos").rglob("*.jpg"))
if not files:
    raise SystemExit("No images found")
data = pd.DataFrame()
    
#main logica loop ==============================================================
for idx in range(0, len(files)):
    
    #fetch paden voor voor- en zijaanzicht
    #deze logica heeft de meeste moeite gekost van dit hele project
    path = files[idx]
    if path.parent.name == "Zij":
        continue
    imageF = cv2.imread(path)           #front view
    #imageS = cv2.imread(files[idx+200]) #side view
      
    print("reading:")
    print(path.parent.parent.name)
            # avgDiff = avgF - avgS
            # topDiff = highF - highS


    both = cv2.bitwise_or(pakmask(imageF), skinmask(imageF), mask=None)
    both = cv2.cvtColor(both, cv2.COLOR_BGR2GRAY)
    both = np.where(both != 0, 255, 0).astype(np.uint8)

    blimage =  cv2.medianBlur(both, 85) # image,kernel size    
    image_gray = both
        # Threshold the image
    ret,image_gray = cv2.threshold(blimage, 127, 255, 0)

    # Step 1: Create an empty skeleton
    size = np.size(image_gray)
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
        whiteP = np.sum(skel==255)
        if cv2.countNonZero(image_gray)==0:
            break
    
    imgData = pd.DataFrame({
        "label": [path.parent.parent.name],
        "index": idx,
        "WittePixels": whiteP,
    })
    data = pd.concat([data, imgData])
    
data.to_csv("out.csv", index=False)
print("done")
    
sns.violinplot(data=data, x="label", y="WittePixels")