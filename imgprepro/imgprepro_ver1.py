import numpy as np
import cv2

# Load the image and convert it to HSV
image = cv2.imread("img1.jpg", 1)
hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Obtain the color mask
lower1 = np.array([165, 0, 0], dtype = np.uint8)
upper1 = np.array([179, 255, 255], dtype = np.uint8)
mask1 = cv2.inRange(hsvImage, lower1, upper1)

lower2 = np.array([0, 0, 0], dtype = np.uint8)
upper2 = np.array([7, 255, 255], dtype = np.uint8)
mask2 = cv2.inRange(hsvImage, lower2, upper2)

mask = cv2.bitwise_or(mask1, mask2)

# Perform morphological close operation to connect the laser lines
kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations = 15)

# Subtract red lazer beams from the image
channels = cv2.split(image)
maskDilation = cv2.dilate(mask, kernel, iterations = 5)
maskInverse = cv2.bitwise_not(maskDilation)
redChannel = cv2.bitwise_and(channels[2], maskInverse)
image = cv2.merge([channels[0], channels[1], redChannel])
image = cv2.inpaint(image, maskDilation, 3, cv2.INPAINT_TELEA)

# Find and draw contours
image2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
	if (cv2.contourArea(cnt) >= 10000 and cv2.contourArea(cnt) <= 3000000):
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(image, [box], 0, (255,0,0), 50)
# cv2.drawContours(image, contours, -1, (0,255,0), 5)

# Display the result
result = cv2.cvtColor(redChannel, cv2.COLOR_GRAY2BGR)
concat = np.concatenate((image, result), axis=1)
cv2.namedWindow( "Window", cv2.WINDOW_NORMAL); 
cv2.imshow('Window', concat)

cv2.waitKey(0)
cv2.destroyAllWindows()