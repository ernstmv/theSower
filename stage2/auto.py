from numpy import array, zeros_like
from math import dist
from time import sleep
import cv2


class Autoset:

    '''CLASS FOR MANAGING THE SEED TASK'''

    def __init__(self, master):
        self.master = master
        self.stop = False
        self.img = None
        self.mask = None
        self.holes = []

    def get_image(self):
        '''SETTER FOR SELF.IMG'''
        self.img = self.master.camera.get_image()
        self.mask = zeros_like(self.img)

    def put_image(self):
        self.preprocess_image()
        img = cv2.addWeighted(self.img, 0.6, self.mask, 0.8, 0)
        self.master.set_image(img)

    def preprocess_image(self):
        '''THIS METHOD PREPROCESS THE IMAGE TO ENHACE DETECTION TASK'''
        height, width, _ = self.img.shape

        center_x, center_y = width // 2, height // 2

        arrow_length = 50

        cv2.arrowedLine(
                self.mask,
                (center_x - arrow_length, center_y), (center_x - 10, center_y),
                (255, 0, 0), 1, tipLength=0.3)
        cv2.arrowedLine(
                self.mask,
                (center_x + arrow_length, center_y), (center_x + 10, center_y),
                (255, 0, 0), 1, tipLength=0.3)
        cv2.arrowedLine(
                self.mask,
                (center_x, center_y - arrow_length), (center_x, center_y - 10),
                (255, 0, 0), 1, tipLength=0.3)
        cv2.arrowedLine(
                self.mask,
                (center_x, center_y + arrow_length), (center_x, center_y + 10),
                (255, 0, 0), 1, tipLength=0.3)
        cv2.circle(
                self.mask,
                (center_x, center_y),
                1, (0, 0, 255), 1)

    def auto(self):

        '''AUTOSEED SEQUENCE'''

        self.master.robot.go_home()
        self.master.robot.get_into_position()
        self.master.controls_frame.camera_to_pause()
        self.master.set_message('Camera activated')
        sleep(5)
        while True:
            self.get_image()
            self.detect_holes()
            self.get_coordinates()
            self.put_image()
            self.master.update()
            self.seed()

    def seed(self):
        self.master.robot.set_abs_mode()
        for pos in self.abs_cnc_coord:
            x, y = pos
            x = round(x, 2)
            y = round(y, 2)
            pos = (x, y)

            self.master.robot.go_to(pos)

    def get_coordinates(self):

        # -----------------------GET-HOLES-CENTERS--------------
        holes_centers = []
        for hole in self.holes:
            center, _ = cv2.minEnclosingCircle(hole)
            center = tuple(map(int, center))
            holes_centers.append(center)

        # ---------------------SORT-IN-ROWS-AND-COLUMNS------------
        centers = sorted(holes_centers)
        matrix = []
        row = []
        colo = (255, 0, 0)
        row_head = 0
        for i, p in enumerate(centers):
            if i == len(centers)-1:
                row.append((centers[row_head][0], p[1]))
                cv2.putText(self.mask, f'{i}', p, 1, 1, colo, 1)
                matrix.append(row)
                continue
            dist = abs(centers[i+1][0] - p[0])
            if dist < 30:
                row.append((centers[row_head][0], p[1]))
                cv2.putText(self.mask, f'{i}', p, 1, 1, colo, 1)
            else:
                row.append((centers[row_head][0], p[1]))
                cv2.putText(self.mask, f'{i}', p, 1, 1, colo, 1)
                row_head = i+1
                matrix.append(row)
                colo = (0, 0, 255) if colo == (255, 0, 0) else (255, 0, 0)
                row = []
        # --------------GET-PIXEL-CAM-COORDINATES-----------------

        height, width, _ = self.img.shape

        cam_x, cam_y = width // 2, height // 2

        #-------------------GET-DIST-X-Y-------------------------

        rel_holes_pos = []
        for row in matrix:
            for element in row:
                del_x = element[0] - cam_x
                del_y = element[1] - cam_y
                rel_holes_pos.append((del_x, del_y))

        # -----------------CONVERT-PIXEL-COORD-TO-CNC------------
        kx = 1 / 90
        ky = 1.1 / 87 
        rel_cnc_pos = []
        for pos in rel_holes_pos:
            xcnc = pos[0] * kx
            ycnc = pos[1] * ky
            rel_cnc_pos.append((xcnc, ycnc))

        # -----------------------GET-CNC-CAM-COORDINATES-------------
        sedx, sedy  = self.master.robot.get_coordinates()
        cam_pos = (float(sedx) + (-3.2), float(sedy) + (-0.2)) 

        # ------------------------CONVERT-REL-CNC-TO-REAL-CNC---------
        self.abs_cnc_coord = []
        for pos in rel_cnc_pos:
            self.abs_cnc_coord.append((cam_pos[1]+pos[1], cam_pos[0] + pos[0]))



    def detect_holes(self):
        self.holes = []
        '''THIS METHOD APPLIES CV TECHNICHES FOR FINDING HOLES'''

        # ----------------------FILTRO-DE-COLOR---------------
        inf = array([0, 0, 0])
        sup = array([90, 70, 120])

        img = cv2.GaussianBlur(self.img, (21, 21), 0)

        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        b_mask = cv2.inRange(img_hsv, inf, sup)

        # --------------------FILTRO-DE-AREA------------------

        conts, _ = cv2.findContours(
            b_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        conts = [cont for cont in conts if cv2.contourArea(cont) > 3000]
        conts = [cont for cont in conts if cv2.contourArea(cont) < 12000]

        # -------------------FILTRO-DE-FORMA--------------------
        for cont in conts:
            x, y, w, h = cv2.boundingRect(cont)

            r = h / w 

            if r > 0.8 and r < 1.2:
                self.holes.append(cont)
                cv2.rectangle(self.mask, (x, y), (x+w, y+h), (0, 255, 0), -1)
