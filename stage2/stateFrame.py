from customtkinter import CTkFrame, CTkButton


class StateFrame(CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.is_camera = CTkButton(
                self, state='disabled',
                fg_color='#011F26',
                border_width=1)
        self.is_robot = CTkButton(
                self, state='disabled',
                fg_color='#011F26',
                border_width=1)
        self.is_seed = CTkButton(
                self, state='disabled',
                fg_color='#011F26',
                border_width=1)

        self.is_camera.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='ew')
        self.is_robot.grid(
                row=0, column=1,
                padx=10, pady=10,
                sticky='ew')
        self.is_seed.grid(
                row=0, column=2,
                padx=10, pady=10,
                sticky='ew')

        self.off_camera()
        self.off_robot()
        self.off_seed()

    def on_camera(self):
        self.is_camera.configure(
                text='Camera online',
                border_color='#228B22',
                text_color_disabled='#228B22')
    def on_robot(self):
        self.is_robot.configure(
                text='Robot online',
                border_color='#228B22',
                text_color_disabled='#228B22')
    def on_seed(self):
        self.is_seed.configure(
                text='Seeding',
                border_color='#228B22',
                text_color_disabled='#228B22')

    def off_camera(self):
        self.is_camera.configure(
                text='Camera offline',
                border_color='#730220',
                text_color_disabled='#730220')
    def off_robot(self):
        self.is_robot.configure(
                text='Robot offline',
                border_color='#730220',
                text_color_disabled='#730220')
    def off_seed(self):
        self.is_seed.configure(
                text='Not seeding',
                border_color='#730220',
                text_color_disabled='#730220')
