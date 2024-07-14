import cv2
from numpy import array

camera = cv2.VideoCapture('/dev/video2')
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    has, img = camera.read()
    if not has: break

    inf = array([0, 0, 0])
    sup = array([90, 70, 120])

    # img = cv2.GaussianBlur(img, (21, 21), 0)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    b_mask = cv2.inRange(img_hsv, inf, sup)

    conts, _ = cv2.findContours(
        b_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    conts = [cont for cont in conts if cv2.contourArea(cont) > 3000]
    conts = [cont for cont in conts if cv2.contourArea(cont) < 12000]

    for cont in conts:
        x, y, w, h = cv2.boundingRect(cont)

        r = h / w 

    #    if r > 0.8 and r < 1.2:
    #            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), -1)

    cv2.imshow('img0', img)
    #cv2.imshow('img1', img_hsv)
    #cv2.imshow('img2', b_mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
