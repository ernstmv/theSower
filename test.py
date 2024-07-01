import cv2
import numpy as np


def main():
    img = cv2.imread('tray.jpeg')
    h_original, w_original = img.shape[:2]
    new_w = w_original // 2
    new_h = h_original // 2

    inf = np.array([10, 50, 80])
    sup = np.array([20, 255, 255])

    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    b_mask = cv2.inRange(img_hsv, inf, sup)
    brown_mask = cv2.bitwise_and(img, img, mask=b_mask)
#     brown_mask = cv2.GaussianBlur(brown_mask, (3, 3), 0)
    img = cv2.GaussianBlur(img, (15, 15), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adaptive = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            21,
            1)

    cv2.imshow('img', img)
    cv2.imshow('thresh', adaptive)
    cv2.imshow('mask', brown_mask)
    cv2.waitKey(0)


main()
