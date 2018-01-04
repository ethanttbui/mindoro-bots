import numpy as np
import cv2
import math

# Load the image and convert it to HSV
image = cv2.imread("img2.jpg", 1)
hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

###################
# DETECTION TASKS #
###################

# Obtain the color mask
lower = np.array([176, 100, 100], dtype = np.uint8)
upper = np.array([179, 255, 255], dtype = np.uint8)
mask = cv2.inRange(hsvImage, lower, upper)

# lower2 = np.array([0, 0, 0], dtype = np.uint8)
# upper2 = np.array([7, 255, 255], dtype = np.uint8)
# mask2 = cv2.inRange(hsvImage, lower2, upper2)
# mask = cv2.bitwise_or(mask1, mask2)
# kernel = np.ones((5,5), np.uint8)
# mask = cv2.dilate(mask, kernel, iterations = 2)

# Find and draw contours
img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
points = []
for cnt in contours:
	if (cv2.contourArea(cnt) >= 100 and cv2.contourArea(cnt) <= 1000):
		(x, y), radius = cv2.minEnclosingCircle(cnt)
		center = (int(x), int(y))
		radius = int(radius)
		cv2.circle(image, center, radius, (255, 0, 0), 10)
		points.append(center)

####################
# EXTRACTION TASKS #
####################

if (len(points) >= 2):
	# Construct the rectangle
	(dx, dy) = (points[1][0] - points[0][0], points[1][1] - points[0][1])
	dl = math.sqrt(dx**2 + dy**2)
	(ox, oy) = (int(points[0][0] + dx/2), int(points[0][1] + dy/2))
	vertices = []
	vertices.append(points[0])
	vertices.append((ox + dy*dl/(2*math.sqrt(dx**2 + dy**2)), oy - dx*dl/(2*math.sqrt(dx**2 + dy**2))))
	vertices.append(points[1])
	vertices.append((ox - dy*dl/(2*math.sqrt(dx**2 + dy**2)), oy + dx*dl/(2*math.sqrt(dx**2 + dy**2))))
	vertices = np.array(vertices, np.int32)
	vertices = vertices.reshape((-1,1,2))
	cv2.polylines(image, [vertices], True, (0,255,255), 10)

	# Crop and save the image
	rows, cols, *_ = image.shape
	rotationAngle = 45 - math.acos((points[1][0] - points[0][0]) / dl)*180 / math.pi
	rotationMatrix = cv2.getRotationMatrix2D((cols/2, rows/2), rotationAngle, 1)
	newCenter = rotationMatrix.dot(np.array([ox, oy, 1]))
	(newOx, newOy) = (int(newCenter[0]), int(newCenter[1]))
	rotatedImage = cv2.warpAffine(image, rotationMatrix, (cols, rows))
	halfWidth = int(math.sqrt(dl**2/2)/2)
	croppedImage = rotatedImage[newOy-halfWidth:newOy+halfWidth, newOx-halfWidth:newOx+halfWidth]
	cv2.imwrite("output.jpg", croppedImage)

else:
	print("No laser point found!")

# Display the result
result = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
concat = np.concatenate((image, result), axis=1)
cv2.namedWindow( "Window", cv2.WINDOW_NORMAL); 
cv2.imshow("Window", concat)

cv2.waitKey(0)
cv2.destroyAllWindows()