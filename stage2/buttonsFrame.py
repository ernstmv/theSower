from customtkinter import CTkFrame, CTkButton
from threading import Thread


class ButtonsFrame(CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.play_button = CTkButton(self, text='Reproducir', state='disabled')
        self.auto_button = CTkButton(self, text='Sembrar', state='disabled')
        self.is_camera = CTkButton(self)
        self.is_robot = CTkButton(self)
        self.is_busy = CTkButton(self, state='disabled')

        self.play_button.grid(
                row=0, column=0,
                columnspan=3,
                padx=10, pady=10,
                sticky='ew')
        self.auto_button.grid(
                row=0, column=3,
                columnspan=3,
                padx=10, pady=10,
                sticky='ew')
        self.is_camera.grid(
                row=1, column=0,
                columnspan=2,
                padx=10, pady=10,
                sticky='ew')
        self.is_robot.grid(
                row=1, column=2,
                columnspan=2,
                padx=10, pady=10,
                sticky='ew')
        self.is_busy.grid(
                row=1, column=4,
                columnspan=2,
                padx=10, pady=10,
                sticky='ew')

        self.camera_off()
        self.robot_off()
        self.not_busy()

    # -----------------------CAMERA_STATE-CONFIG------------------------------

    def camera_on(self):
        '''WHEN CAMERA IS CONNECTED, CONFIGURES COLOR IN GREEN'''

        self.is_camera.configure(
                text='Camara conectada',
                fg_color='#262626',
                border_width=1,
                border_color='#00E069',
                text_color='#00E069',
                command=self.disconnect_camera)

    def camera_off(self):
        '''WHEN CAMERA IS DISCONNECTED, CONFIGURES COLOR IN RED'''

        self.is_camera.configure(
                text='Camara desconectada',
                fg_color='#262626',
                border_width=1,
                border_color='#CC1100',
                text_color='#CC1100',
                command=self.connect_camera)

    def connect_camera(self):
        '''CALLS THE CONNECT CAMERA FUNCTION IN MASATER CLASS'''

        self.master.connect_camera()

    def disconnect_camera(self):
        '''CALLS THE DISCONNECT CAMERA FUNCTION IN MASATER CLASS'''

        self.master.disconnect_camera()

    # -----------------------CAMERA_BUTTON_CONFIG-----------------------------

    def to_play(self):
        '''ACTIVATES THE PLAY BUTTON AND
        PUTS IN PLAY'''

        self.play_button.configure(
                text='Reproducir', command=self.play_video, state='normal')

    def play_video(self):
        '''CALL THE PLAY VIDEO METHOD FROM
        MASTER CLASS AND CHANGE THE
        BUTTON STATE TO PLAY'''

        self.master.play_video()
        self.to_pause()

    def to_pause(self):
        '''ACTIVATSE THE PLAY BUTTON AND
        PUTS IT IN PAUSE'''

        self.play_button.configure(
                text='Detener video', command=self.pause_video, state='normal')

    def pause_video(self):
        '''STOPS THE VIDEO REPRODUCTION
        AND CHANGE THE BUTTON STATE
        TO PAUSE'''

        self.master.pause_video()
        self.to_play()

    def disable_camera(self):
        '''DEACTIVATES THE BUTTON'''

        self.to_play()
        self.play_button.configure(state='disabled')

    # ----------------------------- ROBOT-------------------------------------

    def robot_on(self):
        self.is_robot.configure(
                text='Robot conectado',
                fg_color='#262626',
                border_width=1,
                border_color='#00E069',
                text_color='#00E069',
                command=self.disconnect_robot)

    def robot_off(self):
        self.is_robot.configure(
                text='Robot desconectado',
                fg_color='#262626',
                border_width=1,
                border_color='#CC1100',
                text_color='#CC1100',
                command=self.connect_robot)

    def connect_robot(self):
        self.master.connect_robot()

    def disconnect_robot(self):
        self.master.disconnect_robot()

    # -------------------------AUTO_BUTTON_CONFIG-----------------------------

    def to_auto(self):
        self.auto_button.configure(
                text='Sembrar', command=self.auto, state='normal')

    def to_stop(self):
        self.auto_button.configure(
                text='Detener siembra', command=self.stop, state='normal')

    def auto(self):
        self.master.autoseed()
        self.to_stop()

    def stop(self):
        self.master.stop_auto()
        self.to_auto()

    def disable_auto(self):
        self.to_auto()
        self.auto_button.configure(state='disabled')

    # ------------------------BUSY-BUTTON-CONFIG------------------------------

    def busy(self):
        self.is_busy.configure(
                text='Ocupado',
                fg_color='#262626',
                border_width=1,
                text_color_disabled='#A10D00',
                border_color='#A10D00')

    def not_busy(self):
        self.is_busy.configure(
                text='Disponible',
                fg_color='#262626',
                border_width=1,
                text_color_disabled='#00E069',
                border_color='#00E069')

