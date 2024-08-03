from customtkinter import CTkFrame, CTkButton


class ControlsFrame(CTkFrame):

    '''FRAME WITH BUTTONS TO CONTROL THE STATE OF THE SYSTEM'''

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0), weight=0)
        self.grid_columnconfigure((0, 1), weight=1)

        self.camera_button = CTkButton(
                self, text='Play video',
                border_color="#0DF205",
                fg_color="#0DF205",
                hover_color='#09A603',
                command=self.play_video)

        self.autoseed_button = CTkButton(
                self, text='Autoseed',
                border_color="#0DF205",
                fg_color="#0DF205",
                hover_color='#09A603',
                command=self.autoseed)

        self.camera_button.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='ew')
        self.autoseed_button.grid(
                row=0, column=1,
                padx=10, pady=10,
                sticky='ew')

    def play_video(self):
        '''GET VIDEO FOR CAMERA'''
        self.master.play_video()

    def stop_video(self):
        '''STOP VIDEO FOR CAMERA'''
        self.master.pause_video()

    def autoseed(self):
        '''STARTS THE AUTOSEED SECUENCE'''
        self.master.autoseed()

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
