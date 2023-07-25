import cv2

def list_cameras():
    num_cameras = 0
    while True:
        cap = cv2.VideoCapture(num_cameras, cv2.CAP_DSHOW)
        if not cap.isOpened():
            break
        else:
            print(f"Camera {num_cameras}:")
            print(f"  Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
            print(f"  Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
            cap.release()
        num_cameras += 1

list_cameras()
