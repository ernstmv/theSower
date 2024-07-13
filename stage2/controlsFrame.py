from customtkinter import CTkFrame, CTkButton


class ControlsFrame(CTkFrame):

    '''FRAME WITH BUTTONS TO CONTROL THE STATE OF THE SYSTEM'''

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0), weight=0)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((3), weight=0)

        self.camera_button = CTkButton(
                self, text='Play video',
                command=self.play_video)

        self.robot_button = CTkButton(
                self, text='Connect robot',
                command=self.connect_robot)

        self.autoseed_button = CTkButton(
                self, text='Autoseed',
                command=self.autoseed)

        self.config_button = CTkButton(
                self, text=' ',
                command=self.launch_config_window)

        self.camera_button.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='ew')

        self.robot_button.grid(
                row=0, column=1,
                padx=10, pady=10,
                sticky='ew')
        self.autoseed_button.grid(
                row=0, column=2,
                padx=10, pady=10,
                sticky='ew')
        self.config_button.grid(
                row=0, column=3,
                padx=10, pady=10)

    def play_video(self):
        '''GET VIDEO FOR CAMERA'''
        self.master.play_video()

    def stop_video(self):
        '''STOP VIDEO FOR CAMERA'''
        self.master.pause_video()

    def connect_robot(self):
        '''CONNECTS ROBOT AT MASTER'''
        self.master.connect_robot()

    def disconnect_robot(self):
        '''DISCONNECTS ROBOT AT MASTER'''
        self.master.disconnect_robot()

    def autoseed(self):
        '''STARTS THE AUTOSEED SECUENCE'''

    def launch_config_window(self):
        '''LAUNCH CONFIG WINDOW AT MASTER'''
        self.master.launch_config_window()

    # --------------------------BOTTON-CONFIGURE-----------------------

    def camera_to_pause(self):
        '''SETS BUTTON TO PAUSE VIDEO'''
        self.camera_button.configure(
                text='Pause video',
                command=self.stop_video)

    def camera_to_play(self):
        '''SETS BUTTON TO PLAY VIDEO'''
        self.camera_button.configure(
                text='Play video',
                command=self.play_video)

    def robot_to_on(self):
        '''SETS BUTTON TO CONNECT ROBOT'''
        self.robot_button.configure(
                text='Connect robot',
                command=self.connect_robot)

    def robot_to_off(self):
        '''SETS BUTTON TO DISCONNECT ROBOT'''
        self.robot_button.configure(
                text='Disconnect robot',
                command=self.disconnect_robot)
