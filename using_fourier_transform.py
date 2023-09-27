import cv2 
import time
import numpy as np
import random

threshold = 10
size = 60

video = cv2.VideoCapture('./2509.mp4')
fps = video.get(cv2.CAP_PROP_FPS)
print("fps: "+str(fps))

width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

cX, cY = int(width / 2), int(height / 2)

# processing at 5 fps
frame_rate = 5
frame_skip = int(fps/frame_rate)

frame_count = 0
while True:
	ret, frame = video.read()
	if not ret:
		break
	if frame_count % frame_skip == 0:
		img = frame.copy()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		fft = np.fft.fft2(frame)
		fftshift = np.fft.fftshift(fft)
		fftshift[cY - size:cY + size, cX - size:cX + size] = 0
		fftshift = np.fft.ifftshift(fftshift)
		recon = np.fft.ifft2(fftshift)

		magnitude = 20 * np.log(np.abs(recon))
		mean = np.mean(magnitude)
		isblurry = mean < threshold
		
		text = "output"
		time.sleep(0.30)
		cv2.putText(img, "{}: {:.2f} : {}".format(text, mean, isblurry), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
		cv2.imshow('frame', img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


	frame_count += 1

video.release()
cv2.destroyAllWindows()

