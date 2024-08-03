import matplotlib.pyplot as plt
from python_tsp.heuristics import solve_tsp_simulated_annealing as solve_tsp

from cv2 import (
            cvtColor, COLOR_RGB2HSV, COLOR_RGB2BGR,
            addWeighted, inRange, GaussianBlur,
            findContours, RETR_EXTERNAL, CHAIN_APPROX_NONE,
            contourArea, boundingRect, rectangle
            )  

from numpy import (
            array, zeros_like, zeros, frombuffer, 
            uint8, sqrt, linalg
            )

from threading import Thread
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
        else:
            self.master.set_message(
                "Can't start, check devices")

    def start_sequence(self):
        '''THIS IS THE FULL SEEDING SEQUENCE'''

        self.prepare()
        print('prepare done')
        self.recognize()
        print('recognizee done')
        self.seed()
        print('seed done')
        self.reset()
        print('reset done')

    def prepare(self):
        '''IT TAKES THE ROBOT TO THE STARTING POSITION'''

        self.rbt.go_home()
        self.rbt.absolute_mode()

    def recognize(self):
        '''THIS METHOD MOVES THE ROBOT AND TAKES PHOTOS
        IN EACH POSITION'''

        locs = [('-0.20', '-3.20'), ('-6.60', '-3.20'),
                ('-12.8', '-3.20'), ('-19.2', '-3.20'),
                ('-24.0', '-3.20'), ('-24.0', '-11.8'),
                ('-19.2', '-11.8'), ('-12.8', '-11.8'),
                ('-6.60', '-11.8'), ('-0.20', '-11.8')]

        self.rbt.go_to(z='-26.0')

        for i, loc in enumerate(locs):

            self.master.set_message(f"Moving to region {i+1}")

            self.rbt.go_to(x=loc[0], y=loc[1])
            self.rbt.wait_to(x=float(loc[0]), y=float(loc[1]))
            self.rbt.pause(1)

            holes = self.detect_holes()
            self.get_coordinates(holes, i)
            self.info_f.set_viable(len(self.total))
            sleep(1)

    def seed(self):
        '''THIS METHOD IS ON CHARGE OF SOWING THE
        IDENTIFIED HOLES'''

        self.to_seed = self.total.copy()
        self.rows_and_cols_sort()
        self.show_graph()
        total = len(self.total)

        for i in range(len(self.to_seed)):

            pos = self.to_seed.pop()
            self.put_seed(pos)
            self.sown.append(pos)

            self.info_f.set_sown(i+1)
            self.info_f.set_progress(f"{i+1 * 100// total}%")
            self.show_graph()

            sleep(5)

    def reset(self):
        '''THIS TAKES THE ROBOT TO THE STARTING
        POSTION AFTER SEEDING'''

        self.rbt.go_home()
        self.is_working = False

# ------------------------------AUXILIAR-METHODS---------------

    def show_graph(self):
        '''SHOWS A SCATTER FROM PYPLOT TO SHOW THE
        DETECTED HOLES AND THE SOWING PROGRESS'''
        
        fig, ax = plt.subplots()
        
        x = [coord[0] for coord in self.to_seed]
        y = [coord[1] for coord in self.to_seed]
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
        img_np = frombuffer(
            fig.canvas.tostring_rgb(), dtype=uint8)
        img_np = img_np.reshape(
            fig.canvas.get_width_height()[::-1] + (3,))
        plt.close(fig)
        self.master.set_graph(img_np)


    def get_image(self):
        '''SETTER FOR SELF.IMG, ALSO CREATES SELF.MASK'''

        self.img = self.cam.get_image()
        self.mask = zeros_like(self.img)

    def put_image(self):
        '''ADDS THE MASK TO THE IMAGE AND SHOWS IT'''

        img = addWeighted(self.img, 0.6, self.mask, 0.8, 0)
        self.master.set_image(img)

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

    def get_coordinates(self, holes, loc):
        '''USING THE HOLES PARAMETER IDENTIFIES
        THE COORDINATES (X, Y) OF EACH HOLE'''


        xlims = [(-0.20, -5.80), (-5.80, -12.2),
                 (-12.2, -18.6), (-18.6, -25.0),
                 (-25.0, -26.0)]

        ylims = [(-1.0, -9.0), (-9.0, -18.2)]

        ylim = ylims[0] if loc // 5 == 0 else ylims[1]
        index = loc if loc <= 4 else 4 - loc % 5
        xlim = xlims[index]

        size = len(holes)

        # -----------------------GET-HOLES-CENTERS-------------
        holes_centers = [None] * size 
        for i, hole in enumerate(holes):
            x, y, w, h = boundingRect(hole)
            center = (x + w // 2, y + h // 2)
            holes_centers[i] = center

        # --------------GET-PIXEL-CAM-COORDINATES--------------
        height, width, _ = self.img.shape
        cam_x, cam_y = width // 2, height // 2

        #-------------------GET-DIST-X-Y-----------------------
        rel_holes_pos = [None] * size 
        for i, element in enumerate(holes_centers):
            x_rel = element[0] - cam_x
            y_rel = element[1] - cam_y
            rel_holes_pos[i] = (x_rel, y_rel)

        # -----------------CONVERT-PIXEL-COORD-TO-CNC----------
        kx = 1 / 109
        ky = 1 / 106 

        rel_cnc_pos = [None] * size 
        for i, pos in enumerate(rel_holes_pos):
            xcnc = pos[0] * kx
            ycnc = pos[1] * ky
            rel_cnc_pos[i] = (xcnc, ycnc)

        # -----------------------GET-CNC-CAM-COORDINATES-------
        sedx, sedy, _  = self.rbt.get_coordinates()
        cam_pos = (float(sedx) + (-2.8), float(sedy) + (0.3)) 

        # ------------------------CONVERT-REL-CNC-TO-REAL-CNC--
        to_seed = [None] * size
        for i, pos in enumerate(rel_cnc_pos):
            to_seed[i] = (cam_pos[0]+pos[1], cam_pos[1]+pos[0])

        viable = []

        for c in to_seed:
            if c[0] < xlim[0] and c[0] > xlim[1]:
                if c[1] < ylim[0] and c[1] > ylim[1]:
                    viable.append(c)

        self.total += viable 

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
            if not (area < 16000 and area > 9000):
                continue
            r = h / w
            if r > 0.8 and r < 1.2:
                holes.append(cont)
                rectangle(
                    self.mask, (x, y),
                    (x+w, y+h), (0, 255, 0), -1)

        return holes

    def put_seed(self, pos):

        pos = (round(pos[0], 1), round(pos[1], 1))
        self.rbt.go_to(x=pos[0], y=pos[1], z=-53)
        self.rbt.wait_to(x=pos[0], y=pos[1], z=-53)

        self.rbt.seed()
        self.rbt.go_to(z=-50)
    
    # -----------------ROUTE-COMPUTING-METHODS-----------------

    def rows_and_cols_sort(self):
        '''THIS FUNCTION SORTS THE IDENTIFIED HOLES
        IN ROWS, AND APPEND THEM INTO A LIST'''

        centers = sorted(self.to_seed)
        to_seed = []
        row = []
        row_head = 0
        case = 0
        size = len(centers)

        for i in range(size):

            if i == size - 1:
                row.append((centers[row_head][0], centers[i][1]))
                if case % 2 == 0:
                    row = sorted(row)
                    to_seed += [row[-1 - i] for i in range(len(row))]
                else:
                    to_seed += sorted(row)
                continue

            if abs(centers[i+1][0] - centers[i][0]) < 1:
                row.append((centers[row_head][0], centers[i][1]))
            else:
                row.append((centers[row_head][0], centers[i][1]))
                row_head = i+1
                if case % 2 == 0:
                    row = sorted(row)
                    to_seed += [row[-1 - i] for i in range(len(row))]
                else:
                    to_seed += sorted(row)
                case += 1
                row = []

        self.to_seed = to_seed
