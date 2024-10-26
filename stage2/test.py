import cv2

cam = cv2.VideoCapture('/dev/video2')
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cam.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    cv2.imshow('camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

