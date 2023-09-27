import cv2 
import time

threasold = 100

video = cv2.VideoCapture('./2509.mp4')
fps = video.get(cv2.CAP_PROP_FPS)
print("fps: "+str(fps))

# processing at 5 fps
frame_rate = 5
frame_skip = int(fps/frame_rate)

frame_count = 0
while True:
	ret, frame = video.read()
	if not ret:
		break
	if frame_count % frame_skip == 0:
		variance = cv2.Laplacian(frame, cv2.CV_64F).var()
		if variance < threasold: 
			text = "blurry"
		else:
			text = "not blurry"
		
		time.sleep(0.30)
		cv2.putText(frame, "{}: {:.2f}".format(text, variance), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


	frame_count += 1

video.release()
cv2.destroyAllWindows()

