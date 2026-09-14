import cv2
import numpy as np
from pathlib import Path


def nothing(_value):
    pass


image_path = (
    Path(__file__).resolve().parent.parent
    / "test_foto's"
    / "Shiko_Dachi"
    / "ezgif-frame-001.jpg"
)
image = cv2.imread(str(image_path))
if image is None:
    raise FileNotFoundError(f"Could not open image: {image_path}")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

cv2.namedWindow("Controls", cv2.WINDOW_NORMAL)
cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cv2.namedWindow("HSV mask", cv2.WINDOW_NORMAL)
cv2.namedWindow("RGB mask", cv2.WINDOW_NORMAL)
cv2.namedWindow("Combined", cv2.WINDOW_NORMAL)

cv2.resizeWindow("Controls", 420, 420)
for window in ("Original", "HSV mask", "RGB mask", "Combined"):
    cv2.resizeWindow(window, 500, 350)

trackbars = (
    ("HMin", 0, 179),
    ("SMin", 0, 255),
    ("VMin", 0, 255),
    ("HMax", 179, 179),
    ("SMax", 255, 255),
    ("VMax", 255, 255),
    ("RMin", 0, 255),
    ("GMin", 0, 255),
    ("BMin", 0, 255),
    ("RMax", 255, 255),
    ("GMax", 255, 255),
    ("BMax", 255, 255),
)
for name, default, maximum in trackbars:
    cv2.createTrackbar(name, "Controls", default, maximum, nothing)

while True:
    hsv_lower = np.array(
        [
            cv2.getTrackbarPos("HMin", "Controls"),
            cv2.getTrackbarPos("SMin", "Controls"),
            cv2.getTrackbarPos("VMin", "Controls"),
        ]
    )
    hsv_upper = np.array(
        [
            cv2.getTrackbarPos("HMax", "Controls"),
            cv2.getTrackbarPos("SMax", "Controls"),
            cv2.getTrackbarPos("VMax", "Controls"),
        ]
    )
    rgb_lower = np.array(
        [
            cv2.getTrackbarPos("RMin", "Controls"),
            cv2.getTrackbarPos("GMin", "Controls"),
            cv2.getTrackbarPos("BMin", "Controls"),
        ]
    )
    rgb_upper = np.array(
        [
            cv2.getTrackbarPos("RMax", "Controls"),
            cv2.getTrackbarPos("GMax", "Controls"),
            cv2.getTrackbarPos("BMax", "Controls"),
        ]
    )

    hsv_mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    rgb_mask = cv2.inRange(rgb, rgb_lower, rgb_upper)
    combined_mask = cv2.bitwise_and(hsv_mask, rgb_mask)

    cv2.imshow("Original", image)
    cv2.imshow("HSV mask", cv2.bitwise_and(image, image, mask=hsv_mask))
    cv2.imshow("RGB mask", cv2.bitwise_and(image, image, mask=rgb_mask))
    cv2.imshow("Combined", cv2.bitwise_and(image, image, mask=combined_mask))

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
