
import cv2 
import time
import random

video = cv2.VideoCapture('./2509.mp4')
# video = cv2.VideoCapture('./warehouse_stacking.mp4')

threashold = 100

width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

no_of_division = 12


width_diff = width/no_of_division
height_diff = height/no_of_division

print('width_diff: ', width_diff)
print('height_diff: ', height_diff)

print('width: ', width)
print('height: ', height)

# coordinates are in format x1,y1,x2,y2
total_coordinates =[]

for i in range(int(width_diff),int(width)-2*int(width_diff),int(width_diff)):
	for j in range(int(width_diff),int(height)-1*int(width_diff),int(height_diff)):
		total_coordinates.append([i,j,i+int(width_diff),j+int(height_diff)])

# no_of_division = 4
# for i in range(0,int(width),int(width_diff)):
# 	for j in range(int(height_diff),int(height)-int(height_diff),int(height_diff)):
# 		total_coordinates.append([i,j,i+int(width_diff),j+int(height_diff)])
# 		print(i,j,i+int(width_diff),j+int(height_diff))

# for i in range(0,int(width),int(width_diff)):
# 	for j in range(0,int(height),int(height_diff)):
# 		total_coordinates.append([i,j,i+int(width_diff),j+int(height_diff)])
# 		# print(i,j,i+int(width_diff),j+int(height_diff))

fps = video.get(cv2.CAP_PROP_FPS)
# print("fps: "+str(fps))


# processing at 5 fps
frame_rate = 5
frame_skip = int(fps/frame_rate)

frame_count = 0
while True:
	ret, frame = video.read()
	if not ret:
		break
	if frame_count % frame_skip == 0:
		# variance = cv2.Laplacian(frame, cv2.CV_64F).var()
		# if variance < threasold: 
		# 	text = "blurry"
		# else:
		# 	text = "not blurry"
		# for line in range(0,int(width),int(width_diff)):
		# 	cv2.line(frame,(line,0),(line,int(height)),(0,255,0),thickness=1)
		
		# for line in range(0,int(height),int(height_diff)):
		# 	cv2.line(frame,(0,line),(int(width),line),(0,255,0),thickness=1)

		# temporary minimum variance
		temp_threshold = 340
		temp_threshold_coordinates = [0,0,0,0]

		for i in range(len(total_coordinates)):
			cv2.rectangle(frame, (total_coordinates[i][0], total_coordinates[i][1]), (total_coordinates[i][2], total_coordinates[i][3]), (0,255,0),1)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			variance = cv2.Laplacian(gray[total_coordinates[i][1]:total_coordinates[i][3],total_coordinates[i][0]:total_coordinates[i][2]], cv2.CV_64F).var()


			if variance < temp_threshold: 
				text = "blurry"
			else:
				text = "not blurry"
			
			if variance < temp_threshold:
				temp_threshold = variance
				temp_threshold_coordinates = (total_coordinates[i][0], total_coordinates[i][1], total_coordinates[i][2], total_coordinates[i][3])
				# print('temp_threshold_coordinates: ', temp_threshold_coordinates)
			
				cv2.rectangle(frame, (total_coordinates[i][0], total_coordinates[i][1]), (total_coordinates[i][2], total_coordinates[i][3]), (0, 0, 255), 3)
			cv2.putText(frame, "{}: {:.2f}".format(text, variance), (total_coordinates[i][0]+5, total_coordinates[i][1]+12),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
		cv2.rectangle(frame, (temp_threshold_coordinates[0], temp_threshold_coordinates[1]), (temp_threshold_coordinates[2], temp_threshold_coordinates[3]), (0, 0, 255), 3)
		cv2.imshow('frame', frame)
		time.sleep(0.10)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


	frame_count += 1

video.release()
cv2.destroyAllWindows()


