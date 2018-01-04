import cv2

vidcap = cv2.VideoCapture('video.mp4')
count = 0
while True:
	vidcap.set(1, count)
	success, image = vidcap.read()
	if success:
		cv2.imwrite("images/%d.jpg" % count, image)
		count += 100
	else:
		break