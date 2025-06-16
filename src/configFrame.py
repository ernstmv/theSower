from customtkinter import CTkFrame, CTkButton,  CTkLabel, CTkEntry


class ConfigFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.deep_label = CTkLabel(self, text="Profundidad (cm):")
        self.z_tray_label = CTkLabel(self, text="Z de charola (cm):")
        self.z_scan_label = CTkLabel(self, text='Z de escaneo (cm):')

        self.deep_label.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='w')
        self.z_tray_label.grid(
                row=1, column=0,
                padx=10, pady=10,
                sticky='w')
        self.z_scan_label.grid(
                row=2, column=0,
                padx=10, pady=10,
                sticky='ew')

        self.deep_entry = CTkEntry(self)
        self.z_tray_entry = CTkEntry(self)
        self.z_scan_entry = CTkEntry(self)

        self.deep_entry.grid(
                row=0, column=1,
                padx=10, pady=10,
                sticky='ew')
        self.z_tray_entry.grid(
                row=1, column=1,
                padx=10, pady=10,
                sticky='ew')
        self.z_scan_entry.grid(
                row=2, column=1,
                padx=10, pady=10,
                sticky='ew')

        self.deep_button = CTkButton(
                self, text='Aceptar', command=self.set_deep)
        self.z_tray_button = CTkButton(
                self, text='Aceptar', command=self.set_z_tray)
        self.z_scan_button = CTkButton(
                self, text='Aceptar', command=self.set_z_scan)

        self.deep_button.grid(
                row=0, column=2,
                padx=10, pady=10,
                sticky='ew')
        self.z_tray_button.grid(
                row=1, column=2,
                padx=10, pady=10,
                sticky='ew')
        self.z_scan_button.grid(
                row=2, column=2,
                padx=10, pady=10,
                sticky='ew')

    def set_deep(self):
        content = self.deep_entry.get()
        try:
            self.master.planting_depth = float(content)
        except ValueError:
            self.master.set_message(f'{content} no es un numero')

    def set_z_tray(self):
        content = self.z_tray_entry.get()
        try:
            self.master.z_tray = float(content)
        except ValueError:
            self.master.set_message(f'{content} no es un numero')

    def set_z_scan(self):
        content = self.height_entry.get()
        try:
            self.master.z_scan = float(content)
        except ValueError:
            self.master.set_message(f'{content} no es un numero')
