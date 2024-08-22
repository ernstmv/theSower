from customtkinter import CTkFrame, CTkButton
from threading import Thread


class ButtonsFrame(CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.play_button = CTkButton(self, text='Play', state='disabled')
        self.auto_button = CTkButton(self, text='Autoseed', state='disabled')
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

    # ----------------------CAMERA------------------------

    def camera_on(self):
        self.is_camera.configure(
                text='Camera online',
                fg_color='#262626',
                border_width=1,
                border_color='#00E069',
                text_color='#FFF',
                command=self.disconnect_camera)

    def camera_off(self):
        self.is_camera.configure(
                text='Camera offline',
                fg_color='#262626',
                border_width=1,
                border_color='#CC1100',
                text_color='#CC1100',
                command=self.connect_camera)

    def connect_camera(self):
        self.master.connect_camera()

    def disconnect_camera(self):
        self.master.disconnect_camera()

    def to_play(self):
        self.play_button.configure(
                text='Play video', command=self.play_video, state='normal')

    def play_video(self):
        self.master.play_video()
        self.to_pause()

    def to_pause(self):
        self.play_button.configure(
                text='Stop video', command=self.pause_video, state='normal')

    def pause_video(self):
        self.master.pause_video()
        self.to_play()

    def disable_camera(self):
        self.to_play()
        self.play_button.configure(state='disabled')

# ----------------------------- ROBOT----------------------------------

    def robot_on(self):
        self.is_robot.configure(
                text='Robot online',
                fg_color='#262626',
                border_width=1,
                border_color='#00E069',
                text_color='#00E069',
                command=self.disconnect_robot)

    def robot_off(self):
        self.is_robot.configure(
                text='Robot offline',
                fg_color='#262626',
                border_width=1,
                border_color='#CC1100',
                text_color='#CC1100',
                command=self.connect_robot)

    def connect_robot(self):
        self.master.connect_robot()

    def disconnect_robot(self):
        self.master.disconnect_robot()

# -------------------------OTHER-ACTIONS----------------------------

    def busy(self):
        self.is_busy.configure(
                text='Busy',
                fg_color='#262626',
                border_width=1,
                text_color_disabled='#A10D00',
                border_color='#A10D00')

    def not_busy(self):
        self.is_busy.configure(
                text='Available',
                fg_color='#262626',
                border_width=1,
                text_color_disabled='#00E069',
                border_color='#00E069')

    def disable_robot(self):
        pass

    def to_auto(self):
        self.auto_button.configure(
                text='Autoseed', command=self.autoseed, state='normal')

    def to_stop(self):
        self.auto_button.configure(
                text='Stop sequence', comand=self.stop, state='normal')

    def autoseed(self):
        pass

    def stop(self):
        pass

