# Source - https://stackoverflow.com/a/59906154
# Posted by nathancy, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-07, License - CC BY-SA 4.0

import cv2
import numpy as np
from pathlib import Path


def nothing(x):
    pass

# Load image
image_path = Path("/Users/slashure/Downloads/Kokutsu_Dachi/ezgif-83c462515585d782-jpg/ezgif-frame-007.jpg")
image = cv2.imread(str(image_path))
if image is None:
    raise FileNotFoundError(f"Could not open image: {image_path}")

# Create windows with small custom sizes
cv2.namedWindow('Controls', cv2.WINDOW_NORMAL)
cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
cv2.namedWindow('Masked', cv2.WINDOW_NORMAL)
cv2.namedWindow('canny', cv2.WINDOW_NORMAL)

#cv2.resizeWindow('Controls', 420, 200)
#cv2.resizeWindow('Original', 500, 350)
#cv2.resizeWindow('Masked', 500, 350)

# Create trackbars for color change
cv2.createTrackbar('HMin', 'Controls', 0, 179, nothing)
cv2.createTrackbar('SMin', 'Controls', 0, 255, nothing)
cv2.createTrackbar('VMin', 'Controls', 0, 255, nothing)
cv2.createTrackbar('HMax', 'Controls', 0, 179, nothing)
cv2.createTrackbar('SMax', 'Controls', 0, 255, nothing)
cv2.createTrackbar('VMax', 'Controls', 0, 255, nothing)
cv2.createTrackbar('BMin', 'Controls', 0, 255, nothing)
cv2.createTrackbar('GMin', 'Controls', 0, 255, nothing)
cv2.createTrackbar('RMin', 'Controls', 0, 255, nothing)
cv2.createTrackbar('BMax', 'Controls', 0, 255, nothing)
cv2.createTrackbar('GMax', 'Controls', 0, 255, nothing)
cv2.createTrackbar('RMax', 'Controls', 0, 255, nothing)
cv2.createTrackbar('threshold', 'Controls', 0, 255, nothing)

cv2.createTrackbar('XBlur', 'Controls', 1, 100, nothing)
cv2.createTrackbar('YBlur', 'Controls', 1, 100, nothing)

# Set default value for Max HSV/RGB trackbars
cv2.setTrackbarPos('HMax', 'Controls', 179)
cv2.setTrackbarPos('SMax', 'Controls', 255)
cv2.setTrackbarPos('VMax', 'Controls', 255)
cv2.setTrackbarPos('BMax', 'Controls', 255)
cv2.setTrackbarPos('GMax', 'Controls', 255)
cv2.setTrackbarPos('RMax', 'Controls', 255)

while True:    
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'Controls')
    sMin = cv2.getTrackbarPos('SMin', 'Controls')
    vMin = cv2.getTrackbarPos('VMin', 'Controls')
    hMax = cv2.getTrackbarPos('HMax', 'Controls')
    sMax = cv2.getTrackbarPos('SMax', 'Controls')
    vMax = cv2.getTrackbarPos('VMax', 'Controls')
    BMin = cv2.getTrackbarPos('BMin', 'Controls')
    GMin = cv2.getTrackbarPos('GMin', 'Controls')
    RMin = cv2.getTrackbarPos('RMin', 'Controls')
    BMax = cv2.getTrackbarPos('BMax', 'Controls')
    GMax = cv2.getTrackbarPos('GMax', 'Controls')
    RMax = cv2.getTrackbarPos('RMax', 'Controls')

    XBlur = cv2.getTrackbarPos('XBlur', 'Controls') + 1
    YBlur = cv2.getTrackbarPos('YBlur', 'Controls') + 1

    threshold = cv2.getTrackbarPos('threshold', 'Controls')

    BGRlower = np.array([BMin, GMin, RMin])
    BGRupper = np.array([BMax, GMax, RMax])
    BGRmask = cv2.inRange(image, BGRlower, BGRupper)
    BGRresult = cv2.bitwise_and(image, image, mask=BGRmask)

    HSVlower = np.array([hMin, sMin, vMin])
    HSVupper = np.array([hMax, sMax, vMax])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    HSVmask = cv2.inRange(hsv, HSVlower, HSVupper)
    #HSVresult = cv2.bitwise_and(image, image, mask=HSVmask)
    
    result = cv2.bitwise_and(BGRresult, BGRresult, mask=HSVmask)
    

    blimage = cv2.blur(result, (XBlur, YBlur))
    edges = cv2.Canny(blimage, threshold, threshold*3, 3)

    cv2.imshow('Original', image)
    cv2.imshow('Masked', result)
    cv2.imshow('canny', edges)
    cv2.imshow('blur', blimage)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()