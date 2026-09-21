import cv2 
import numpy as np
from pathlib import Path


def nothing(x):
    pass


# Build the file list once
files = sorted(Path("test_fotos").rglob("*.jpg"))
if not files:
    raise SystemExit("No images found")
current = -1

# Create windows with small custom sizes
cv2.namedWindow('imgControls', cv2.WINDOW_NORMAL)
cv2.namedWindow('maskControls', cv2.WINDOW_NORMAL)
cv2.namedWindow('blurControls', cv2.WINDOW_NORMAL)
cv2.namedWindow('edgeControls', cv2.WINDOW_NORMAL)
cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
cv2.namedWindow('Masked', cv2.WINDOW_NORMAL)
cv2.namedWindow('canny', cv2.WINDOW_NORMAL)

#cv2.resizeWindow('Controls', 420, 200)
#cv2.resizeWindow('Original', 500, 350)
#cv2.resizeWindow('Masked', 500, 350)

# trackbar voor image selectie
cv2.createTrackbar("img", "imgControls", 0, len(files) - 1, nothing)
# Create trackbars for color change
cv2.createTrackbar('HMin', 'maskControls', 0, 179, nothing)
cv2.createTrackbar('SMin', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('VMin', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('HMax', 'maskControls', 0, 179, nothing)
cv2.createTrackbar('SMax', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('VMax', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('BMin', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('GMin', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('RMin', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('BMax', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('GMax', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('RMax', 'maskControls', 0, 255, nothing)
cv2.createTrackbar('threshold', 'edgeControls', 0, 255, nothing)
# trackbar voor blur selectie
cv2.createTrackbar('Welke_blur', 'blurControls', 0, 3 , nothing)
# trackbars voor blur instellingen
cv2.createTrackbar('XBlur', 'blurControls', 1, 50, nothing)
cv2.createTrackbar('YBlur', 'blurControls', 1, 50, nothing)

# Set default value for Max HSV/RGB trackbars
cv2.setTrackbarPos('HMax', 'maskControls', 179)
cv2.setTrackbarPos('SMax', 'maskControls', 255)
cv2.setTrackbarPos('VMax', 'maskControls', 255)
cv2.setTrackbarPos('BMax', 'maskControls', 255)
cv2.setTrackbarPos('GMax', 'maskControls', 255)
cv2.setTrackbarPos('RMax', 'maskControls', 255)

while True:    
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'maskControls')
    sMin = cv2.getTrackbarPos('SMin', 'maskControls')
    vMin = cv2.getTrackbarPos('VMin', 'maskControls')
    hMax = cv2.getTrackbarPos('HMax', 'maskControls')
    sMax = cv2.getTrackbarPos('SMax', 'maskControls')
    vMax = cv2.getTrackbarPos('VMax', 'maskControls')
    BMin = cv2.getTrackbarPos('BMin', 'maskControls')
    GMin = cv2.getTrackbarPos('GMin', 'maskControls')
    RMin = cv2.getTrackbarPos('RMin', 'maskControls')
    BMax = cv2.getTrackbarPos('BMax', 'maskControls')
    GMax = cv2.getTrackbarPos('GMax', 'maskControls')
    RMax = cv2.getTrackbarPos('RMax', 'maskControls')

    welke_blur = cv2.getTrackbarPos('Welke_blur', 'blurControls')
## +1 want anders kan de blur onder 0 komen en dat geeft een error en *2 want anders kan de blur op een even getal komen en dat geeft een error bij median blur
    XBlur = cv2.getTrackbarPos('XBlur', 'blurControls') *2 + 1
    YBlur = cv2.getTrackbarPos('YBlur', 'blurControls') *2 + 1

    threshold = cv2.getTrackbarPos('threshold', 'edgeControls')

    idx = cv2.getTrackbarPos("img", "imgControls")

    if idx != current:
            image = cv2.imread(str(files[idx]))

            current = idx

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
    
    blimage = result
    if welke_blur == 1:
        blimage = cv2.GaussianBlur(result, (XBlur, YBlur), 0)
    elif welke_blur == 2:
        blimage = cv2.blur(result, (XBlur, YBlur))
    elif welke_blur == 3:
        blimage = cv2.medianBlur(result, XBlur)
    
    edges = cv2.Canny(blimage, threshold, threshold*3, 3)

    cv2.imshow('Original', image)
    cv2.imshow('Masked', result)
    cv2.imshow('canny', edges)
    cv2.imshow('blur', blimage)

    if cv2.waitKey(30) & 0xFF == 27:   # Esc to exit
        break

cv2.destroyAllWindows()