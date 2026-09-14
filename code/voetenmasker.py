# Source - https://stackoverflow.com/a/59906154
# Posted by nathancy, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-07, License - CC BY-SA 4.0

import cv2
import numpy as np
from pathlib import Path


def nothing(x):
    pass

# Load image
image_path = Path("test_fotos/KokutsuDachiF/ezgif-frame-001.jpg")
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
cv2.createTrackbar('threshold', 'Controls', 0, 255, nothing)

# Set default value for Max HSV trackbars
cv2.setTrackbarPos('HMax', 'Controls', 179)
cv2.setTrackbarPos('SMax', 'Controls', 255)
cv2.setTrackbarPos('VMax', 'Controls', 255)

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0

while True:
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'Controls')
    sMin = cv2.getTrackbarPos('SMin', 'Controls')
    vMin = cv2.getTrackbarPos('VMin', 'Controls')
    hMax = cv2.getTrackbarPos('HMax', 'Controls')
    sMax = cv2.getTrackbarPos('SMax', 'Controls')
    vMax = cv2.getTrackbarPos('VMax', 'Controls')
    threshold = cv2.getTrackbarPos('threshold', 'Controls')

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    
    blimage = cv2.blur(result, (3,3))
    edges = cv2.Canny(blimage, threshold, threshold*3, 3)

    cv2.imshow('Original', image)
    cv2.imshow('Masked', result)
    cv2.imshow('canny', edges)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()