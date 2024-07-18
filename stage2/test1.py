from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, imshow, waitKey

camera = VideoCapture('/dev/video2')
camera.set(CAP_PROP_FRAME_WIDTH, 1280)
camera.set(CAP_PROP_FRAME_HEIGHT, 720)

while True:

    has, frame = camera.read()

    if not has:
        break

    if waitKey(1) & 0xFF == ord('q'):
        break

    imshow('img', frame)

camera.release()
