from customtkinter import CTk
from videoFrame import VideoFrame
from infoFrame import InfoFrame
from logFrame import LogFrame
from controlsFrame import ControlsFrame
from stateFrame import StateFrame
from camera import Camera
from configWindow import ConfigWindow
from robot import Robot
from coordinatesFrame import CoordinatesFrame
from auto import Autoset


class App(CTk):

    '''MAIN CLASS, CONTAINS ALL THE FRAMES AND IS IN CHARGE
    OF COMMUNICATION BELONG THEM'''

    def __init__(self):
        super().__init__()

        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.title('The Sower')
        self.stop_video = False
        self.config_window = None

        self.info_frame = InfoFrame(self)
        self.video_frame = VideoFrame(self)
        self.controls_frame = ControlsFrame(self)
        self.state_frame = StateFrame(self)
        self.log_frame = LogFrame(self)
        self.coordinates_frame = CoordinatesFrame(self)

        self.info_frame.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='nsew')
        self.video_frame.grid(
                row=1, column=0,
                padx=10, pady=10,
                sticky='nsew',
                rowspan=2)
        self.coordinates_frame.grid(
                row=3, column=0,
                padx=10, pady=10,
                sticky='ew')

        self.log_frame.grid(
                row=0, column=1,
                padx=10, pady=10,
                sticky='ew',
                rowspan=2)
        self.controls_frame.grid(
                row=2, column=1,
                padx=10, pady=10,
                sticky='ew')
        self.state_frame.grid(
                row=3, column=1,
                padx=10, pady=10,
                sticky='ew')

        self.robot = Robot(self)
        self.robot.autoconnect()

        self.camera = Camera(self)
        self.camera.autoconnect()

    # -------------------CAMERA-METHODS--------------------------

    def camera_on(self):
        self.state_frame.on_camera()

    def camera_off(self):
        self.state_frame.off_camera()

    def play_video(self):
        while not self.stop_video:
            img = self.camera.get_image()
            self.set_image(img)
            self.controls_frame.camera_to_pause()
            self.update()
        self.stop_video = False
        self.controls_frame.camera_to_play()

    def pause_video(self):
        self.stop_video = True

    # ---------------------ROBOT-METHODS-------------------------

    def robot_on(self):
        self.state_frame.on_robot()
        self.controls_frame.robot_to_off()
        self.robot.is_connected = True
        self.set_message(f'Robot connected at {self.robot.port}')

    def robot_off(self):
        self.state_frame.off_robot()
        self.controls_frame.robot_to_on()
        self.robot.is_connected = False
        self.set_message('Robot disconnected')

    def connect_robot(self):
        self.robot.connect_robot()

    def disconnect_robot(self):
        self.robot_off()
        self.robot = Robot(self)

    # --------------FRAME-METHODS----------------------------------

    def set_image(self, image):
        self.video_frame.set_image(image)

    def set_message(self, message):
        self.log_frame.set_message(message)

    def set_x_coord(self, x):
        self.coordinates_frame.set_x(x)

    def set_y_coord(self, y):
        self.coordinates_frame.set_y(y)

    def set_z_coord(self, z):
        self.coordinates_frame.set_z(z)

    # --------------SPECIAL-METHODS----------------------------------

    def launch_config_window(self):
        self.controls_frame.camera_to_play()
        self.config_window = ConfigWindow(self)
        self.config_window.grab_set()

    def autoseed(self):
        '''STARTS AUTOSEED SECUENCE'''
        self.auto = Autoset(self)
        self.auto.auto()
