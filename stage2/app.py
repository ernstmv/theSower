from customtkinter import CTk
from time import sleep
from threading import Thread

from infoFrame import InfoFrame
from videoFrame import VideoFrame
from coordinatesFrame import CoordinatesFrame
from graphFrame import GraphFrame
from logFrame import LogFrame
from controlsFrame import ControlsFrame
from stateFrame import StateFrame
from extraFrame import ExtraFrame

from robot import Robot
from camera import Camera
from auto import Autoset


class App(CTk):

    '''MAIN CLASS, CONTAINS ALL OTHER CLASSES
    AND IS RESPONSIBLE OF COMMUNICATING THEM'''

    def __init__(self):
        super().__init__()

        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure((2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.title('The Sower')
        self.stop_video = False
        self.stop_clock = False
        self.camera = None
        self.robot = None

        self.info_frame = InfoFrame(self)
        self.video_frame = VideoFrame(self)
        self.controls_frame = ControlsFrame(self)
        self.state_frame = StateFrame(self)
        self.log_frame = LogFrame(self)
        self.coordinates_frame = CoordinatesFrame(self)
        self.graph_frame = GraphFrame(self)
        self.extra_frame = ExtraFrame(self)

        self.extra_frame.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='ew')
        self.graph_frame.grid(
                row=1, column=0,
                padx=10, pady=10,
                sticky='ew',
                rowspan=2)
        self.log_frame.grid(
                row=3, column=0,
                padx=10, pady=10,
                rowspan=2,
                sticky='ew')
        self.controls_frame.grid(
                row=5, column=0,
                padx=10, pady=10,
                sticky='ew')

        self.info_frame.grid(
                row=0, column=1,
                padx=10, pady=10,
                rowspan=2,
                sticky='nsew')
        self.video_frame.grid(
                row=2, column=1,
                padx=10, pady=10,
                sticky='nsew',
                rowspan=2)
        self.coordinates_frame.grid(
                row=4, column=1,
                padx=10, pady=10,
                sticky='ew')
        self.state_frame.grid(
                row=5, column=1,
                padx=10, pady=10,
                sticky='ew')

    # -------------------CAMERA-METHODS--------------------------


    def connect_camera(self):
        self.camera = Camera(self)
        self.camera.autoconnect()
        if self.camera.is_connected:
            self.camera_on()
        else:
            del self.camera
            self.camera = None

    def disconnect_camera(self):
        del self.camera
        self.camera = None
        self.camera_off()

    def camera_on(self):
        self.state_frame.on_camera()

    def camera_off(self):
        self.state_frame.off_camera()
        self.controls_frame.camera_to_play()
        self.set_message("Camera disconnected")

    def play_video(self):
        if self.camera:
            self.controls_frame.camera_to_pause()
            self.stop_video = False
            while not self.stop_video:
                img = self.camera.get_image()
                if img is None:
                    self.disconnect_camera()
                    self.set_message('Cannot get image, camera error')
                    break
                self.set_image(img)
                self.update()
        else:
            self.set_message("No camera connected")

    def pause_video(self):
        self.stop_video = True
        self.controls_frame.camera_to_play()


    # ---------------------ROBOT-METHODS-------------------------

    def connect_robot(self):
        self.robot = Robot(self)
        self.robot.autoconnect()
        if self.robot.is_connected:
            self.robot_on()
            self.bind("<KeyPress>", self.robot.keys_manager)
        else:
            del self.robot
            self.robot = None

    def disconnect_robot(self):
        self.unbind("<KeyPress>")
        del self.robot
        self.robot = None
        self.robot_off()

    def robot_on(self):
        self.state_frame.on_robot()

    def robot_off(self):
        self.state_frame.off_robot()
        self.set_message('Robot disconnected')

    # --------------FRAME-METHODS----------------------------------

    def set_image(self, image):
        self.video_frame.set_image(image)

    def set_message(self, message):
        self.log_frame.set_message(message)

    def set_coords(self, x, y, z):
        self.coordinates_frame.set_coords(x, y, z)

    def set_graph(self, graph):
        self.graph_frame.show_image(graph)

    def busy(self):
        self.state_frame.busy()

    def not_busy(self):
        self.state_frame.not_busy()

    # --------------SEEDING-METHODS----------------------------------

    def autoseed(self):
        '''STARTS AUTOSEED SECUENCE'''
        self.busy()
        Thread(target=self.start_clock).start()

        self.auto = Autoset(self, self.info_frame)
        self.auto.auto()

        self.stop_clok()
        self.not_busy()

    def start_clock(self):
        self.stop_clock = False
        seconds = 0 
        minutes = 0
        while not self.stop_clock:
            self.info_frame.set_time(
                f'{minutes}:{seconds}')
            sleep(1)
            seconds += 1
            if seconds == 60:
                minutes += 1
                seconds = 0

    def stop_clok(self):
        self.stop_clock = True
