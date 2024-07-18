import matplotlib.pyplot as plt
from threading import Thread
from numpy import array, zeros_like
from math import dist
from time import sleep
import cv2
import numpy as np


class Autoset:

    '''CLASS FOR MANAGING THE SEED TASK'''

    def __init__(self, master):
        self.master = master
        self.img = None
        self.mask = None
        self.final_coordinates = []

    def auto(self):

        '''AUTOSEED SEQUENCE'''
        if not self.check_devices():
            return
        Thread(target=self.start_sequence).start()
        while True:
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
        return self.master.camera.is_connected and self.master.robot.is_connected

    def start_sequence(self):
        '''THIS METHOD MOVES THE ROBOT AND TAKES PHOTOS IN EACH POSITION'''
        locs = ['-1.1', '-3', '-6', '-9', '-12', '-15', '-18', '-21', '-23']
        self.master.robot.go_home()
        self.master.robot.recon_config()

        self.master.robot.go_to(x=locs[0])
        while self.master.robot.x_pos != float(locs[0]):
            sleep(0.1)
        self.master.robot.pause(1)
        try:
            holes = self.detect_holes()
            self.get_coordinates(holes)
            self.show_graph()
            self.seed()
        except Exception as e:
            print('ERROR')
            print(e)
        self.master.robot.go_to(z='-1')

        return


    def show_graph(self, sown = None):

        fig, ax = plt.subplots()
        
        # Asumiendo que self.final_coordinates es una lista de pares (x, y)
        x = [coord[0] for coord in self.final_coordinates]
        y = [coord[1] for coord in self.final_coordinates]
        ax.scatter(x, y)

        if sown:
            xs = [coord[0] for coord in sown]
            ys = [coord[1] for coord in sown]
            ax.scatter(xs, ys)
        
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Holes detected')
        
        # Añadir una cuadrícula para mejor referencia visual
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_aspect('equal')
        
        fig.canvas.draw()
        imagen_np = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        imagen_np = imagen_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close(fig)
        imagen_bgr = cv2.cvtColor(imagen_np, cv2.COLOR_RGB2BGR)
        self.master.set_graph(imagen_bgr)


    def get_image(self):
        '''SETTER FOR SELF.IMG, ALSO CREATES SELF.MASK'''
        self.img = self.master.camera.get_image()
        self.mask = zeros_like(self.img)

    def put_image(self):
        img = cv2.addWeighted(self.img, 0.6, self.mask, 0.8, 0)
        self.master.set_image(img)


    def get_coordinates(self, holes):

        # -----------------------GET-HOLES-CENTERS--------------
        holes_centers = []
        for hole in holes:
            center, _ = cv2.minEnclosingCircle(hole)
            center = tuple(map(int, center))
            holes_centers.append(center)

        # --------------GET-PIXEL-CAM-COORDINATES-----------------

        height, width, _ = self.img.shape
        cam_x, cam_y = width // 2, height // 2

        #-------------------GET-DIST-X-Y-------------------------

        rel_holes_pos = []
        for element in holes_centers:
            x_rel = element[0] - cam_x
            y_rel = element[1] - cam_y
            rel_holes_pos.append((x_rel, y_rel))

        # -----------------CONVERT-PIXEL-COORD-TO-CNC------------
        kx = 1 / 90
        ky = 1.1 / 87 


        rel_cnc_pos = []
        for pos in rel_holes_pos:
            xcnc = pos[0] * kx
            ycnc = pos[1] * ky
            rel_cnc_pos.append((xcnc, ycnc))


        # -----------------------GET-CNC-CAM-COORDINATES-------------
        sedx, sedy, _  = self.master.robot.get_coordinates()
        cam_pos = (float(sedx) + (-3.4), float(sedy) + (-0.2)) 

        # ------------------------CONVERT-REL-CNC-TO-REAL-CNC---------
        abs_cnc_coord = []
        for pos in rel_cnc_pos:
            abs_cnc_coord.append((cam_pos[0]+pos[1], cam_pos[1] + pos[0]))

        self.final_coordinates += abs_cnc_coord

    def detect_holes(self):
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
        holes = []

        for cont in conts:
            x, y, w, h = cv2.boundingRect(cont)

            r = h / w 

            if r > 0.8 and r < 1.2:
                holes.append(cont)
                cv2.rectangle(
                    self.mask, (x, y),
                    (x+w, y+h), (0, 255, 0), -1)

        return holes

    def seed(self):
        sown = []
        self.master.robot.absolute_mode()
        self.master.set_message(f"total holes: {len(self.final_coordinates)}")
        for i, pos in enumerate(self.final_coordinates):
            self.master.robot.go_to(z=-51)
            self.master.set_message(f"Hole No. {i}")
            x, y = pos
            x = round(x, 2)
            y = round(y, 2)

            self.master.robot.go_to(x=x, y=y, z=-55)
            self.master.robot.pause(1)
            sown.append(pos)
            self.show_graph(sown)
            sleep(5)
