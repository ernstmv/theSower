from customtkinter import CTkFrame, CTkButton


class StateFrame(CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.is_camera = CTkButton(
                self,
                fg_color='#011F26',
                border_width=1,
                command=None)
        self.is_robot = CTkButton(
                self,
                fg_color='#011F26',
                border_width=1,
                command=None)
        self.is_busy = CTkButton(
                self,
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
        self.is_busy.grid(
                row=0, column=2,
                padx=10, pady=10,
                sticky='ew')

        self.off_camera()
        self.off_robot()
        self.not_busy()

    def on_camera(self):
        self.is_camera.configure(
                text='Camera online',
                border_color='#228B22',
                text_color='#228B22',
                command=self.disconnect_camera)
    def on_robot(self):
        self.is_robot.configure(
                text='Robot online',
                border_color='#228B22',
                text_color='#228B22',
                command=self.disconnect_robot)
    def busy(self):
        self.is_busy.configure(
                text='Busy',
                border_color='#F2AB27',
                text_color='#F2AB27')

    def off_camera(self):
        self.is_camera.configure(
                text='Camera offline',
                border_color='#730220',
                text_color='#730220',
                command=self.connect_camera)
    def off_robot(self):
        self.is_robot.configure(
                text='Robot offline',
                border_color='#730220',
                text_color='#730220',
                command=self.connect_robot)
    def not_busy(self):
        self.is_busy.configure(
                text='Available',
                border_color='#333333',
                text_color='#333333')

    def disconnect_camera(self):
        self.master.disconnect_camera()

    def connect_camera(self):
        self.master.connect_camera()

    def disconnect_robot(self):
        self.master.disconnect_robot()

    def connect_robot(self):
        self.master.connect_robot()
