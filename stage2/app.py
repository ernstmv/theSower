from customtkinter import CTk, CTkSegmentedButton, CTkLabel

from headerFrame import HeaderFrame
from visualizeFrame import VisualizeFrame
from configFrame import ConfigFrame
from videoFrame import VideoFrame
from buttonsFrame import ButtonsFrame
from logFrame import LogFrame

from robot import Robot
from camera import Camera
from auto import Autoset


class App(CTk):

    '''MAIN CLASS, CONTAINS ALL OTHER CLASSES
    AND IS RESPONSIBLE OF COMMUNICATING THEM'''

    def __init__(self):
        super().__init__()

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.frames_icons = [' ', ' ']
        mssg = 'Universidad Autonoma Chapingo\nCIIARAA DIMA\n2024'

        self.title('theSower')
        self.stop_video = False
        self.stop_clock = False
        self.camera = None
        self.robot = None

        self.z_scan = None
        self.planting_depth = None
        self.z_tray = None
        self.crop = None
        self.greenhouse = None

        self.header_frame = HeaderFrame(self)
        self.vis_frame = VisualizeFrame(self)
        self.conf_frame = ConfigFrame(self)
        self.video_frame = VideoFrame(self)
        self.buttons_frame = ButtonsFrame(self)
        self.log_frame = LogFrame(self)

        self.switch_button = CTkSegmentedButton(
                self, values=self.frames_icons,
                command=self.switch_frame)

        self.switch_button.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='ew')

        self.conf_frame.grid(
                row=1, column=0,
                rowspan=4,
                padx=10, pady=10,
                sticky='nsew')

        self.vis_frame.grid(
                row=1, column=0,
                rowspan=4,
                padx=10, pady=10,
                sticky='nsew')

        self.header_frame.grid(
                row=0, column=1,
                padx=10, pady=10,
                columnspan=2,
                sticky='ew')
        self.video_frame.grid(
                row=1, column=1,
                columnspan=2,
                padx=10, pady=10,
                sticky='nsew')
        self.buttons_frame.grid(
                row=2, column=1,
                padx=10, pady=10,
                sticky='ew')
        self.log_frame.grid(
                row=2, column=2,
                rowspan=2,
                padx=10, pady=10,
                sticky='nsew')

        self.registered_label = CTkLabel(self, text=mssg)
        self.registered_label.grid(
                row=3, column=1,
                padx=10, pady=10,
                sticky='nsew')

        self.vis_frame.tkraise()

    # -------------------CAMERA-METHODS--------------------------

    def connect_camera(self):
        '''HERE WE CREATE A NEW CAMERA OBJECT AND TRY TO CONNECT IT, IF IT
        THEN UPDATES UI, ELSE DELETE AND DO NOTHING'''
        self.camera = Camera(self)
        self.camera.autoconnect()
        if self.camera.is_connected:
            self.camera_on()
        else:
            del self.camera
            self.camera = None

    def camera_on(self):
        '''UPDATES BUTTONS FRAME AND CHECK IF BOTH DEVICES ARE AVAILABLE'''
        self.buttons_frame.camera_on()
        self.buttons_frame.to_play()
        self.check_available()

    def disconnect_camera(self):
        del self.camera
        self.camera = None
        self.camera_off()

    def camera_off(self):
        self.buttons_frame.camera_off()
        self.buttons_frame.disable_camera()
        self.buttons_frame.disable_auto()
        self.set_message("Camara desconectada")

    def play_video(self):
        self.buttons_frame.to_pause()
        self.stop_video = False
        while not self.stop_video:
            img = self.camera.get_image()
            try:
                self.set_image(img)
            except Exception:
                self.disconnect_camera()
                self.set_message("Error en la camara")
                self.stop_video = True
            self.update()

    def pause_video(self):
        self.stop_video = True

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
        self.robot.close()
        self.robot = None
        self.robot_off()

    def robot_on(self):
        self.buttons_frame.robot_on()
        self.check_available()

    def robot_off(self):
        self.buttons_frame.robot_off()
        self.buttons_frame.disable_auto()
        self.set_message('Robot desconectado')

    # --------------FRAME-METHODS----------------------------------

    def set_image(self, image):
        self.video_frame.set_image(image)

    def set_message(self, message):
        self.log_frame.set_message(message)

    def set_coords(self, x, y, z):
        self.header_frame.set_coords(x, y, z)

    def busy(self):
        self.buttons_frame.busy()

    def not_busy(self):
        self.buttons_frame.not_busy()

    # --------------SEEDING-METHODS----------------------------------

    def autoseed(self):
        '''STARTS AUTOSEED SECUENCE'''
        self.busy()

        try:
            self.auto = Autoset(
                    self, self.vis_frame,
                    self.z_scan, self.planting_depth, self.z_tray)
            self.vis_frame.set_crop(self.crop)
            self.vis_frame.set_greenhouse(greenhouse)
            self.auto.auto()

        except Exception as e:
            self.set_message('Error en el proceso, revise los parametros')

        self.not_busy()

    def stop_auto(self):
        pass
    # ------------------------------OTHER-METHODS-----------------------------

    def save_data(self):
        pass

    def check_available(self):
        if self.camera and self.robot:
            self.buttons_frame.to_auto()

    def switch_frame(self, choice):
        idx = self.frames_icons.index(choice)
        if idx == 0:
            self.vis_frame.tkraise()
        elif idx == 1:
            self.conf_frame.tkraise()

    def set_graph(self, graph):
        self.video_frame.set_graph(graph)
