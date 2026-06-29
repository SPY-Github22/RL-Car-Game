import cv2

# 1. Read the image in grayscale
img = cv2.imread('track2.png', cv2.IMREAD_GRAYSCALE)

# 2. Invert the image (black becomes white 255, white becomes black 0)
_, mask = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

# 3. Save the mask
cv2.imwrite('track_mask.png', mask)
