from cv2 import (
            cvtColor, COLOR_RGB2HSV, addWeighted, inRange, GaussianBlur,
            findContours, RETR_EXTERNAL, CHAIN_APPROX_NONE,
            boundingRect, rectangle, imwrite)

import matplotlib.pyplot as plt

from numpy import array, zeros_like, frombuffer, uint8

from threading import Thread
from datetime import datetime
from time import sleep


class Autoset:

    '''CLASS FOR MANAGING THE SEED TASK'''

    def __init__(self, master, visualize, z_scan, planting_depth, z_tray):

        self.master = master
        self.visualize_f = visualize

        self.img = None
        self.mask = None

        self.total = 0
        self.to_seed = []
        self.sown = 0
        self.missing = []
        self.seed_centers = []

        self.rbt = None
        self.cam = None

        self.show_video = False
        self.is_working = False
        self.stop_clock = False

        self.z_scan = -10
        self.planting_depth = -3
        self.z_tray = -21

    def auto(self):
        '''AUTOSEED SEQUENCE'''

        Thread(target=self.start_sequence).start()
        Thread(target=self.start_clock).start()
        Thread(target=self.capture_images).start()

        self.is_working = True
        self.show_video = True

        while self.is_working:
            if self.show_video:
                self.get_image()
                self.detect_holes()
                self.put_image()
            else:
                self.show_graph()
            self.master.update()

    def start_sequence(self):
        self.prepare()
        self.master.set_message('Robot ready')
        self.recognize()
        self.master.set_message('Recognize done')
        self.seed()
        self.master.set_message('Seeding task done')
        self.reset()
        self.master.set_message('Tray finished')

    def prepare(self):
        '''IT TAKES THE ROBOT TO THE STARTING POSITION'''

        self.rbt = self.master.robot
        self.cam = self.master.camera
        self.rbt.go_home()
        self.rbt.absolute_mode()

    def recognize(self):
        '''THIS METHOD MOVES THE ROBOT AND TAKES PHOTOS
        IN EACH POSITION'''

        locs = [('-1.00', '-9.40'), ('-12.2', '-9.40'),
                ('-25.0', '-9.40'), ('-38.1', '-9.40'),
                ('-50.0', '-9.40'), ('-50.0', '-33.2'),
                ('-38.1', '-33.2'), ('-25.0', '-33.2'),
                ('-12.2', '-33.2'), ('-1.00', '-33.2')]

        for region, loc in enumerate(locs):

            self.master.set_message(f"Moving to region {region+1}")

            self.rbt.complex_movement(
                    x=loc[0], y=loc[1], z=self.z_scan)

            self.rbt.wait_to(
                    x=float(loc[0]), y=float(loc[1]), z=float(self.z_scan))

            self.rbt.pause(1)

            holes = self.detect_holes()
            self.get_coordinates(holes, region)
            self.visualize_f.set_viable(len(self.to_seed))

        self.show_video = False

    def seed(self):
        '''THIS METHOD IS ON CHARGE OF SOWING THE
        IDENTIFIED HOLES'''

        self.rows_and_cols_sort()
        self.sown = 0

        for pos in self.seed_centers:
            self.put_seed(pos)
            self.sown += 5
            self.visualize_f.set_sown(self.sown)
            self.visualize_f.set_progress(self.sown / self.total)

            sleep(3)

    def reset(self):
        '''THIS TAKES THE ROBOT TO THE STARTING
        POSTION AFTER SEEDING'''

        self.rbt.go_home()
        self.is_working = False

# ------------------------------AUXILIAR-METHODS---------------

    def get_image(self):
        '''SETTER FOR SELF.IMG, ALSO CREATES SELF.MASK'''

        self.img = self.cam.get_image()
        self.mask = zeros_like(self.img)

    def put_image(self):
        '''ADDS THE MASK TO THE IMAGE AND SHOWS IT'''

        img = addWeighted(self.img, 0.6, self.mask, 0.8, 0)
        self.master.set_image(img)

    def get_coordinates(self, holes, loc):
        '''USING THE HOLES PARAMETER IDENTIFIES
        THE COORDINATES (X, Y) OF EACH HOLE'''

        xlims = [(-1, -15), (-15, -28.3),
                 (-28.3, -40.9), (-40.9, -53.5),
                 (-53.5, -66.8)]

        ylims = [(-1, -22), (-22, -39.5)]

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

        # -------------------GET-DIST-X-Y-----------------------
        rel_holes_pos = [None] * size
        for i, element in enumerate(holes_centers):
            x_rel = element[0] - cam_x
            y_rel = element[1] - cam_y
            rel_holes_pos[i] = (x_rel, y_rel)

        # -----------------CONVERT-PIXEL-COORD-TO-CNC----------
        kx = 2.6 / 98
        ky = 2.45 / 97

        rel_cnc_pos = [None] * size
        for i, pos in enumerate(rel_holes_pos):
            xcnc = pos[0] * kx
            ycnc = pos[1] * ky
            rel_cnc_pos[i] = (xcnc, ycnc)

        # -----------------------GET-CNC-CAM-COORDINATES-------
        sedx, sedy, _ = self.rbt.get_coordinates()
        cam_pos = (float(sedx) + (-9.8), float(sedy) + (-0))

        # ------------------------CONVERT-REL-CNC-TO-REAL-CNC--
        to_seed = [None] * size
        for i, pos in enumerate(rel_cnc_pos):
            to_seed[i] = (cam_pos[0]+pos[1], cam_pos[1]+pos[0])

        viable = []

        for c in to_seed:
            if c[0] < xlim[0] and c[0] > xlim[1]:
                if c[1] < ylim[0] and c[1] > ylim[1]:
                    viable.append(c)

        self.to_seed += viable

    def detect_holes(self):
        '''THIS METHOD APPLIES CV TECHNICHES FOR
        FINDING HOLES'''

        # ----------------------FILTRO-DE-COLOR---------------
        inf = array([0, 0, 0])
        sup = array([100, 100, 120])

        img = GaussianBlur(self.img, (21, 21), 0)

        img_hsv = cvtColor(img, COLOR_RGB2HSV)

        b_mask = inRange(img_hsv, inf, sup)

        # --------------FILTROS-DE-AREA-Y-FORMA----------------

        conts, _ = findContours(b_mask, RETR_EXTERNAL, CHAIN_APPROX_NONE)
        holes = []

        for cont in conts:
            x, y, w, h = boundingRect(cont)
            area = w * h
            r = h / w
            if area < 16000 and area > 8000 and r > 0.8 and r < 1.2:
                holes.append(cont)
                rectangle(self.mask, (x, y), (x+w, y+h), (0, 255, 0), -1)

        return holes

    def put_seed(self, pos):

        pos = (round(pos[0], 1), round(pos[1], 1))

        self.rbt.complex_movement(x=pos[0], y=pos[1])
        self.rbt.go_to(z=self.planting_depth + self.z_tray)

        self.rbt.wait_to(
                x=pos[0], y=pos[1],
                z=self.planting_depth + self.z_tray)

        self.rbt.seed()
        self.rbt.go_to(z=self.z_tray)

    # -----------------ROUTE-COMPUTING-METHODS-----------------

    def rows_and_cols_sort(self):
        '''THIS FUNCTION SORTS THE IDENTIFIED HOLES
        IN ROWS, AND APPEND THEM INTO A LIST'''

        CENTERS = sorted(self.to_seed)

        # ---------------------SORT-IN-ROWS-AND-COLUMNS--------------------

        matrix = []
        row = []
        row_head = 0
        size = len(CENTERS)

        for i in range(size):

            if i == size - 1:
                row.append((CENTERS[row_head][0], CENTERS[i][1]))
                matrix.append(sorted(row))
                continue

            if abs(CENTERS[i+1][0] - CENTERS[i][0]) < 1:
                row.append((CENTERS[row_head][0], CENTERS[i][1]))
            else:
                row.append((CENTERS[row_head][0], CENTERS[i][1]))
                row_head = i+1
                matrix.append(sorted(row))
                row = []

        # --------------------FINDING-MISSING-HOLES----------------------

        for row in matrix:
            for i, element in enumerate(row):

                if i == 0:
                    mean = abs(element[1] - row[1][1]) if len(row) != 1 else 3.4
                    continue

                if i == len(row)-1:
                    continue

                dist = abs(element[1] - row[i+1][1])
                if dist < mean * 1.5:
                    mean = (mean*(i-1) + dist) / i
                else:
                    self.missing.append(
                            (element[0], element[1] + int(mean)))

        # --------------ORDENAR-POR-SEGUNDA-VEZ--------------------------

        CENTERS = sorted(CENTERS + self.missing)
        matrix = []
        row = []
        row_head = 0
        size = len(CENTERS)

        for i in range(size):

            if i == size - 1:
                row.append((CENTERS[row_head][0], CENTERS[i][1]))
                matrix.append(sorted(row))
                continue

            if abs(CENTERS[i+1][0] - CENTERS[i][0]) < 1:
                row.append((CENTERS[row_head][0], CENTERS[i][1]))
            else:
                row.append((CENTERS[row_head][0], CENTERS[i][1]))
                row_head = i+1
                matrix.append(sorted(row))
                row = []

        # -------------------------FILTER-OF-HOLES-PER-ROW----------------

        n_matrix = []

        for row in matrix:
            n_row = []
            for i, element in enumerate(row):
                if i == len(row) - 1:
                    n_row.append(element)
                    continue

                if abs(element[1] - row[i+1][1]) > 2:
                    n_row.append(element)
                else:
                    continue
            n_matrix.append(n_row)

        self.to_seed = []
        for row in n_matrix:
            self.to_seed += row

        self.total = len(self.to_seed)
        self.visualize_f.set_viable(self.total)

        self.seed_centers = []

        for row in matrix:
            cont = 1
            for element in row:
                if cont == 3 or cont == 8:
                    self.seed_centers.append(element)
                cont += 1

    def start_clock(self):
        '''THIS METHOD UPDATES THE TIME TEXTBOX IN THE UI, SECOND BY SECOND
        TO TAKE CARE ABOUT THE TRANSCURRED TIME'''

        self.stop_clock = False
        seconds = 0
        minutes = 0
        while not self.stop_clock:
            m = f'0{minutes}' if minutes < 10 else minutes
            s = f'0{seconds}' if seconds < 10 else seconds
            self.visualize_f.set_time(f'{m}:{s}')
            sleep(1)
            seconds += 1
            if seconds == 60:
                minutes += 1
                seconds = 0

    def stop_clock(self):
        '''THIS METHOD STOPS THE CLOCK AT THE END OF THE PROCESS'''
        self.stop_clock = True

    def show_graph(self):
        '''SHOWS A SCATTER FROM PYPLOT TO SHOW THE DETECTED HOLES
        AND THE SOWING PROGRESS'''

        fig, ax = plt.subplots()

        x = [coord[0] for coord in self.to_seed]
        y = [coord[1] for coord in self.to_seed]
        ax.scatter(x, y, color='r')

        if self.missing:
            xm = [coord[0] for coord in self.missing]
            ym = [coord[1] for coord in self.missing]
            ax.scatter(xm, ym, color='b', marker='x')

        if self.seed_centers:
            xc = [coord[0] for coord in self.seed_centers]
            yc = [coord[1] for coord in self.seed_centers]
            ax.scatter(xc, yc, color='black', marker='x')

        ax.set_facecolor('#262626')
        fig.set_facecolor('#262626')

        ax.tick_params(axis='x', colors='yellow', which='both')
        ax.tick_params(axis='y', colors='yellow', which='both')

        ax.spines['top'].set_edgecolor('yellow')
        ax.spines['right'].set_edgecolor('yellow')
        ax.spines['bottom'].set_edgecolor('yellow')
        ax.spines['left'].set_edgecolor('yellow')

        ax.set_xlabel('X Coordinate', color='yellow')
        ax.set_ylabel('Y Coordinate', color='yellow')

        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_aspect('equal')

        fig.canvas.draw()
        img_np = frombuffer(fig.canvas.tostring_rgb(), dtype=uint8)
        img_np = img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close(fig)
        self.master.set_graph(img_np)

    def capture_images(self):
        sleep(2)
        time = datetime.now().strftime("%H_%M_%S")
        imwrite(f'{time}.jpg', self.img)
