from customtkinter import CTkFrame, CTkButton


class StateFrame(CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.is_camera = CTkButton(self)
        self.is_robot = CTkButton(self)
        self.is_busy = CTkButton(self, state='disabled')

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
                text_color='#228B22',
                hover_color='#4E780E',
                command=self.disconnect_camera)
    def on_robot(self):
        self.is_robot.configure(
                text='Robot online',
                text_color='#228B22',
                hover_color='#4E780E',
                command=self.disconnect_robot)
    def busy(self):
        self.is_busy.configure(
                text='Busy',
                border_color='#F2AB27')

    def off_camera(self):
        self.is_camera.configure(
                text='Camera offline',
                fg_color='#D90D1E',
                hover_color='#40010D',
                command=self.connect_camera)
    def off_robot(self):
        self.is_robot.configure(
                text='Robot offline',
                fg_color='#D90D1E',
                hover_color='#40010D',
                command=self.connect_robot)
    def not_busy(self):
        self.is_busy.configure(
                text='Available',
                fg_color='#228B22')

    def disconnect_camera(self):
        self.master.disconnect_camera()

    def connect_camera(self):
        self.master.connect_camera()

    def disconnect_robot(self):
        self.master.disconnect_robot()

    def connect_robot(self):
        self.master.connect_robot()
