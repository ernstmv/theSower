from cv2 import cvtColor, imdecode
from requests import get
from numpy import array, uint8
from imutils import resize


class Camera():
    def __init__(self, ip):
        self.ip = ip
        self.url = 'http://' + self.ip + ':8080/shot.jpg'

    def get_image(self):
        img_resp = get(self.url)
        img_arr = array(bytearray(img_resp.content), dtype=uint8)
        img = imdecode(img_arr, -1)
        return resize(img, width=700, height=1300)
