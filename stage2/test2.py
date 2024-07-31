from cv2 import rectangle, boundingRect, GaussianBlur, cvtColor, COLOR_RGB2HSV, inRange, findContours, RETR_EXTERNAL, CHAIN_APPROX_NONE, VideoCapture, waitKey, imshow, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, drawContours
from numpy import array 


def detect_holes(img):
    '''THIS METHOD APPLIES CV TECHNICHES FOR
    FINDING HOLES'''

    holes = []

# ----------------------FILTRO-DE-COLOR---------------
    inf = array([0, 0, 0])
    sup = array([90, 70, 120])

    img = GaussianBlur(img, (21, 21), 0)

    img_hsv = cvtColor(img, COLOR_RGB2HSV)

    b_mask = inRange(img_hsv, inf, sup)

# --------------FILTROS-DE-AREA-Y-FORMA----------------

    conts, _ = findContours(
        b_mask, RETR_EXTERNAL, CHAIN_APPROX_NONE)
    drawContours(img, conts, -1, (0, 255, 0), 0)

    for cont in conts:
        x, y, w, h = boundingRect(cont)
        area = w * h
        if not (area < 16000 and area > 7000):
            continue
        r = h / w
        if r > 0.8 and r < 1.2:
            holes.append(cont)
            rectangle(
                img, (x, y),
                (x+w, y+h), (0, 255, 0), -1)
    return img, img_hsv

cam = VideoCapture('/dev/video2')
cam.set(CAP_PROP_FRAME_WIDTH, 1280)
cam.set(CAP_PROP_FRAME_HEIGHT, 720)

while True:
    has, frame = cam.read()
    if not has: break
    frame, hsv = detect_holes(frame)
    imshow('hvs', frame)
    if waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
