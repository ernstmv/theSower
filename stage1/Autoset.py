import cv2
from math import dist, atan, degrees
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt


class Autoset:

    def __init__(self):
        self.kernel = 11
        self.c = 2
        self.change = False
        self.missing_points = []

    def set_image(self, img):
        self.img = img
        self.mask = np.zeros_like(img)

    def get_image(self):
        return cv2.addWeighted(self.img, 0.6, self.mask, 0.8, 0)

    def autoset_tray(self):

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (31, 31), 0)

        thresh = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY_INV,
                self.kernel,
                self.c)

        conts, _ = cv2.findContours(
                thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)

        try:
            self.tray = max(conts, key=cv2.contourArea)
        except Exception:
            return None

        cv2.drawContours(
                self.mask,
                self.tray,
                -1,
                (0, 0, 255),
                1)

        _, _, b = cv2.split(self.mask)
        edges = cv2.Canny(b, 50, 150)
        lines = cv2.HoughLinesP(
                edges,
                1,
                np.pi/180,
                100,
                minLineLength=500,
                maxLineGap=300)

        if lines is None:
            return None

        pos = []
        for line in lines:
            x, y, x1, y1 = line[0]
            pos.append([x, y])
            pos.append([x1, y1])
            cv2.circle(
                    self.mask,
                    (x, y),
                    5,
                    (0, 255, 255),
                    3)

            cv2.circle(
                    self.mask,
                    (x1, y1),
                    5,
                    (0, 255, 255),
                    3)

        if len(pos) < 4 or pos is None:
            return None

        kmeans = KMeans(n_clusters=4)
        kmeans.fit(np.array(pos))

        self.centers = kmeans.cluster_centers_
        colors = []

        for i in range(-1, 3):

            c = self.centers[i]
            slope = []

            dists = {dist(c, cent): cent for cent in self.centers}

            for distance in dists:
                if distance == 0 or distance == max(dists.keys()):
                    continue

                x = [c[0], dists[distance][0]]
                y = [c[1], dists[distance][1]]

                m, _ = np.polyfit(x, y, 1)
                slope.append(m)

                cv2.line(
                        self.mask,
                        (int(c[0]), int(c[1])),
                        (int(dists[distance][0]), int(dists[distance][1])),
                        (255, 0, 0),
                        2)
            if len(slope) < 2:
                return None

            angle = degrees(atan((slope[1] - slope[0])/(1+slope[1]*slope[0])))
            color = (0, 0, 0)
            angle = abs(angle)

            if angle < 95 and angle > 85:
                color = (255, 0, 255)
                colors.append(510)

            cv2.circle(
                    self.mask,
                    (int(self.centers[i][0]), int(self.centers[i][1])),
                    5,
                    color,
                    3)

        return sum(colors) == 510 * 4

    def detect_tray(self):
        if self.autoset_tray():
            self.detect_holes()
            return True
        elif self.change is False:
            if self.kernel < 19:
                self.kernel += 2
            else:
                self.kernel = 13
            self.change = True
        else:
            if self.c < 5:
                self.c += 0.1
            else:
                self.c = 2
                self.change = False

    def detect_holes(self):

        inf = np.array([30, 10, 10])
        sup = np.array([150, 60, 90])

        img = cv2.GaussianBlur(self.img, (21, 21), 0)

        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        b, _, _ = cv2.split(self.mask)
        conts, _ = cv2.findContours(
                b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.tray = max(conts, key=cv2.contourArea)

        b_mask = cv2.inRange(img_hsv, inf, sup)

        conts, _ = cv2.findContours(
                b_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        conts = [cont for cont in conts if cv2.contourArea(cont) > 20]
        conts = [cont for cont in conts if cv2.contourArea(cont) < 350]

        holes = []
        for cont in conts:
            ((x, y), _) = cv2.minEnclosingCircle(cont)
            center = (int(x), int(y))
            if cv2.pointPolygonTest(self.tray, center, False) > 0:
                holes.append(cont)

        self.holes_centers = [None] * len(holes)
        for index, hole in enumerate(holes):
            x, y, w, h = cv2.boundingRect(hole)
            cv2.rectangle(self.mask, (x, y), (x+w, y+h), (0, 255, 0), 2)
            center, _ = cv2.minEnclosingCircle(hole)
            center = tuple(map(int, center))
            self.holes_centers[index] = center

        self.find_missing_points()

        if self.missing_points:
            for point in self.missing_points:
                cv2.circle(self.mask, point, 5, (0, 0, 255), 2)

        self.get_cnc_coordinates()

    def get_cnc_coordinates(self):

        # Convert Pixels to milimeters
        hsv = cv2.cvtColor(self.img, cv2.COLOR_RGB2HSV)
        inf = np.array([110, 180, 130])
        sup = np.array([140, 255, 170])

        mask = cv2.inRange(hsv, inf, sup)
        conts, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cont = max(conts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cont)
        cv2.rectangle(self.mask, (x, y), (x+w, y+h), (0, 0, 255), 1)

        cnc_zero, _ = cv2.minEnclosingCircle(cont)
        x_cnc_zero, y_cnc_zero = cnc_zero

        constant = 12.7 / w
        relative_centers = []

        for center in self.holes_centers:
            x, y = center
            new_x = x - x_cnc_zero
            new_y = y_cnc_zero - y
            new_center = new_x, new_y
            relative_centers.append(new_center)

        holes_centers_cnc = []

        for center_rel in relative_centers:
            x_rel, y_rel = center_rel
            x_mm = x_rel * constant
            y_mm = y_rel * constant
            center_mm = (x_mm, y_mm)
            holes_centers_cnc.append(center_mm)

        x = [coord[0] for coord in holes_centers_cnc]
        y = [coord[1] for coord in holes_centers_cnc]

        # Crear el gráfico de dispersión
        plt.scatter(x, y, marker='x', c='green', label='Seeding marks')
        plt.scatter(0, 0, marker='x', c='red', label='CNC origin')

        # Añadir etiquetas y título
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Milimetric CNC coordinates of the holes')
        plt.axis('equal')
        plt.legend()

        # Mostrar el gráfico
        plt.show()

    def find_missing_points(self):
        self.missing_points = []
        centers = sorted(self.holes_centers)
        matrix = []
        row = []
        colo = (255, 0, 0)
        row_head = 0
        for i, p in enumerate(centers):
            if i == len(centers)-1:
                row.append((centers[row_head][0], p[1]))
                matrix.append(row)
                continue
            dist = abs(centers[i+1][0] - p[0])
            if dist < 15:
                row.append((centers[row_head][0], p[1]))
            else:
                row.append((centers[row_head][0], p[1]))
                row_head = i+1
                matrix.append(row)
                colo = (0, 0, 255) if colo == (255, 0, 0) else (255, 0, 0)
                row = []

        for row in matrix:
            row = sorted(row)
            for i, element in enumerate(row):
                if i == 0:
                    mean = abs(element[1] - row[1][1])
                    continue
                if i == len(row)-1:
                    continue
                dist = abs(element[1] - row[i+1][1])
                if dist < mean * 1.5:
                    mean = (mean*(i-1) + dist) / i
                else:
                    self.missing_points.append(
                            (element[0], element[1] + int(mean)))
