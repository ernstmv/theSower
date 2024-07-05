import cv2
from Autoset import Autoset
from camera import Camera


def main():
    IP = "10.12.211.68"
    camera = Camera(IP)
    auto = Autoset()
    stop = False
    while 1:
        img = camera.get_image()
        auto.set_image(img)
        if auto.detect_tray():
            stop = True
        img = auto.get_image()
        cv2.imshow("tray", img)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord('p') or stop:
            cv2.waitKey()
            stop = False


if __name__ == '__main__':
    main()
