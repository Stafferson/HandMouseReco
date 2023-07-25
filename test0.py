import cv2

for i in range(100):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    if ret:
         print(i)