from customtkinter import CTkToplevel, CTkLabel, CTkOptionMenu, CTkButton


class ConfigWindow(CTkToplevel):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title = 'Config window'
        self.ports = []

        self.camera_label = CTkLabel(self, text='CAMERA')
        self.camera_label.grid(
                row=0, column=0,
                columnspan=4,
                padx=10, pady=10,
                sticky='ew')

        self.camera_ports_button = CTkButton(
                self, text='Scan for ports',
                command=self.get_camera_ports)
        self.camera_ports_button.grid(
                row=1, column=0,
                padx=10, pady=10,
                sticky='ew')
        self.camera_menu = CTkOptionMenu(
                self, values=self.ports,
                command=self.select_camera_port)
        self.camera_menu.grid(
                row=1, column=1,
                padx=10, pady=10,
                sticky='ew')

        self.connect_camera_button = CTkButton(
                self, text='Connect camera',
                command=self.connect_camera)
        self.connect_camera_button.grid(
                row=1, column=2,
                padx=10, pady=10,
                sticky='ew')

        self.robot_label = CTkLabel(self, text='Robot')
        self.robot_label.grid(
                row=2, column=0,
                columnspan=4,
                padx=10, pady=10,
                sticky='ew')

        self.robot_ports_button = CTkButton(
                self, text='Scan for ports',
                command=self.get_robot_ports)
        self.robot_ports_button.grid(
                row=3, column=0,
                padx=10, pady=10,
                sticky='ew')

        self.robot_menu = CTkOptionMenu(
                self, values=self.ports,
                command=self.select_robot_port)
        self.robot_menu.grid(
                row=3, column=1,
                padx=10, pady=10,
                sticky='ew')

        self.connect_robot_button = CTkButton(
                self, text='Connect robot',
                command=self.connect_robot)
        self.connect_robot_button.grid(
                row=3, column=2,
                padx=10, pady=10,
                sticky='ew')

    def get_camera_ports(self):
        self.master.camera.get_ports()
        devices = self.master.camera.available_cameras
        self.ports = [port for _, port in devices]
        self.devices = [device for device, _ in devices]
        self.camera_menu.configure(values=self.devices)

    def select_camera_port(self, choice):
        self.master.camera.set_port(self.ports[self.devices.index(choice)])
        self.master.camera.set_device(choice)

    def connect_camera(self):
        self.master.camera.connect_camera()

    def get_robot_ports(self):
        self.master.robot.get_ports()
        self.robot_menu.configure(values=self.master.robot.available_ports)

    def select_robot_port(self, choice):
        self.master.robot.set_port(choice)

    def connect_robot(self):
        self.master.robot.connect_robot()
