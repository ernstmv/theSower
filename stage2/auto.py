import matplotlib.pyplot as plt

from cv2 import (
            cvtColor, COLOR_RGB2HSV, COLOR_RGB2BGR,
            addWeighted, inRange,
            GaussianBlur, findContours, RETR_EXTERNAL,
            CHAIN_APPROX_NONE, contourArea, boundingRect,
            rectangle, arrowedLine, circle)  

from threading import Thread
from numpy import array, zeros_like, frombuffer, uint8
from math import dist
from time import sleep


class Autoset:

    '''CLASS FOR MANAGING THE SEED TASK'''

    def __init__(self, master, info):
        self.master = master
        self.img = None
        self.mask = None
        self.total = []
        self.to_seed = []
        self.sown = []
        self.rbt = None
        self.cam = None
        self.is_working = False
        self.info_f = info

    def auto(self):

        '''AUTOSEED SEQUENCE'''
        if self.check_devices():
            self.is_working = True
            Thread(target=self.start_sequence).start()
            while self.is_working:
                self.get_image()
                self.detect_holes()
                self.put_image()
                self.master.update()

    def check_devices(self):
        '''THIS METHODS RESET CONNECTIONS'''
        self.master.disconnect_camera()
        self.master.disconnect_robot()
        sleep(1)
        self.master.connect_camera()
        self.master.connect_robot()
        self.rbt = self.master.robot
        self.cam = self.master.camera
        return self.cam.is_connected & self.rbt.is_connected

    def start_sequence(self):

        '''THIS METHOD MOVES THE ROBOT AND TAKES
        PHOTOS IN EACH POSITION'''

        locs = ['-1.1', '-7.6', '-13.8', '-19.4']
        self.rbt.go_home()
        self.rbt.absolute_mode()

        for i, loc in enumerate(locs):

            self.master.set_message(f"Moving to position {i}")
            self.rbt.go_to(x=loc, y='-8.2', z='-18.2')

            while True:
                if -18.2 == self.rbt.z_pos: break
                sleep(0.1)

            self.rbt.pause(1)
            holes = self.detect_holes()
            self.get_coordinates(holes, i)
            self.info_f.set_viable(len(self.total))
            self.seed()

        self.rbt.go_home()
        self.is_working = False

    def show_graph(self):
        '''SHOWS A SCATTER FROM PYPLOT TO SHOW THE DETECTED HOLES
        AND THE SOWING PROGRESS'''
        
        fig, ax = plt.subplots()
        
        x = [coord[0] for coord in self.total]
        y = [coord[1] for coord in self.total]
        ax.scatter(x, y)

        if self.sown:
            xs = [coord[0] for coord in self.sown]
            ys = [coord[1] for coord in self.sown]
            ax.scatter(xs, ys)
        
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Holes detected')
        
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_aspect('equal')
        
        fig.canvas.draw()
        img_np = frombuffer(fig.canvas.tostring_rgb(), dtype=uint8)
        img_np = img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close(fig)
        self.master.set_graph(img_np)


    def get_image(self):
        '''SETTER FOR SELF.IMG, ALSO CREATES SELF.MASK'''
        self.img = self.cam.get_image()
        self.mask = zeros_like(self.img)

    def put_image(self):
        '''ADDS THE MASK TO THE IMAGE AND SHOWS IT'''

        height, width = self.mask.shape[:2]
        
        center_x, center_y = width // 2, height // 2
        
        arrowedLine(
            self.mask, (center_x + 10, center_y), 
            (center_x + 10 + 50, center_y),
            (255, 0, 0), 1, tipLength=1)

        arrowedLine(
            self.mask, (center_x - 10, center_y),
            (center_x - 10 - 50, center_y),
            (255, 0, 0), 1, tipLength=1)

        arrowedLine(
            self.mask, (center_x, center_y + 10),
            (center_x, center_y + 10 + 50),
            (255, 0, 0), 1, tipLength=1)

        arrowedLine(
            self.mask, (center_x, center_y - 10),
            (center_x, center_y - 10 - 50),
            (255, 0, 0), 1, tipLength=1)
        
        circle(
            self.mask, (center_x, center_y),
            1, (0, 0, 255), 1)

        img = addWeighted(self.img, 0.6, self.mask, 0.8, 0)
        self.master.set_image(img)


    def get_coordinates(self, holes, loc):

        '''USING THE HOLES PARAMETER IDENTIFIES THE COORDINATES (X, Y)
        OF EACH HOLE'''

        limits = [ (0.0, -7.4), (-7.4, -13.8),
                   (-13.8, -20.2), (-20.2, -26.6) ]

        limit = limits[loc]

        size = len(holes)

        # -----------------------GET-HOLES-CENTERS--------------
        holes_centers = [None] * size 
        for i, hole in enumerate(holes):
            x, y, w, h = boundingRect(hole)
            center = (x + w // 2, y + h // 2)
            holes_centers[i] = center

        # --------------GET-PIXEL-CAM-COORDINATES-----------------

        height, width, _ = self.img.shape
        cam_x, cam_y = width // 2, height // 2

        #-------------------GET-DIST-X-Y-------------------------

        rel_holes_pos = [None] * size 
        for i, element in enumerate(holes_centers):
            x_rel = element[0] - cam_x
            y_rel = element[1] - cam_y
            rel_holes_pos[i] = (x_rel, y_rel)

        # -----------------CONVERT-PIXEL-COORD-TO-CNC------------
        kx = 1 / 90
        ky = 1 / 87 

        rel_cnc_pos = [None] * size 
        for i, pos in enumerate(rel_holes_pos):
            xcnc = pos[0] * kx
            ycnc = pos[1] * ky
            rel_cnc_pos[i] = (xcnc, ycnc)

        # -----------------------GET-CNC-CAM-COORDINATES-------------

        sedx, sedy, _  = self.rbt.get_coordinates()
        cam_pos = (float(sedx) + (-3.8), float(sedy)) 

        # ------------------------CONVERT-REL-CNC-TO-REAL-CNC---------
        to_seed = [None] * size
        for i, pos in enumerate(rel_cnc_pos):
            to_seed[i] = (cam_pos[0]+pos[1], cam_pos[1]+pos[0])

        self.to_seed = [c for c in to_seed if c[0] < limit[0] and c[0] > limit[1]]

        self.total += self.to_seed

    def detect_holes(self):
        '''THIS METHOD APPLIES CV TECHNICHES FOR
        FINDING HOLES'''

        holes = []

        # ----------------------FILTRO-DE-COLOR---------------
        inf = array([0, 0, 0])
        sup = array([90, 70, 120])

        img = GaussianBlur(self.img, (21, 21), 0)

        img_hsv = cvtColor(img, COLOR_RGB2HSV)

        b_mask = inRange(img_hsv, inf, sup)

        # --------------FILTROS-DE-AREA-Y-FORMA----------------

        conts, _ = findContours(
            b_mask, RETR_EXTERNAL, CHAIN_APPROX_NONE)

        for cont in conts:
            x, y, w, h = boundingRect(cont)
            area = w * h
            if not (area < 12000 and area > 6000):
                continue
            r = h / w
            if r > 0.8 and r < 1.2:
                holes.append(cont)
                rectangle(
                    self.mask, (x, y),
                    (x+w, y+h), (0, 255, 0), -1)

        return holes


    def seed(self):
        self.rbt.go_to(z=-50)
        for i, pos in enumerate(self.to_seed):
            self.show_graph()
            pos = (round(pos[0], 1), round(pos[1], 1))
            self.rbt.go_to(x=pos[0], y=pos[1])
            self.put_seed(pos)
            self.sown.append(pos)
            self.info_f.set_sown(len(self.sown))
            self.info_f.set_progress(round(len(self.sown)/len(self.total), 2))
            sleep(5)

    def put_seed(self, pos):
        self.rbt.go_to(z = -53)
        while True:
            if self.rbt.z_pos == -53:
                if self.rbt.x_pos == pos[0]:
                    if self.rbt.y_pos == pos[1]:
                        break
            sleep(0.1)
        self.rbt.seed()
        sleep(1)
        self.rbt.go_to(z=-50)
