from customtkinter import CTkFrame, CTkButton,  CTkLabel, CTkEntry


class ConfigFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.deep_label = CTkLabel(self, text="Deep (mm):")
        self.z_tray_label = CTkLabel(self, text="Z of tray (mm):")
        self.z_scan_label = CTkLabel(self, text='Z of scan (mm):')
        self.crop_label = CTkLabel(self, text='Crop: ')

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
        self.crop_label.grid(
                row=3, column=0,
                padx=10, pady=10,
                sticky='ew')

        self.deep_entry = CTkEntry(self)
        self.z_tray_entry = CTkEntry(self)
        self.z_scan_entry = CTkEntry(self)
        self.crop_entry = CTkEntry(self)

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
        self.crop_entry.grid(
                row=3, column=1,
                padx=10, pady=10,
                sticky='ew')

        self.deep_button = CTkButton(
                self, text='Set deep', command=self.set_deep)
        self.z_tray_button = CTkButton(
                self, text='Set zero', command=self.set_z_tray)
        self.z_scan_button = CTkButton(
                self, text='Set height', command=self.set_z_scan)
        self.crop_button = CTkButton(
                self, text='Set crop', command=self.set_crop)

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
        self.crop_button.grid(
                row=3, column=2,
                padx=10, pady=10,
                sticky='ew')

    def set_deep(self):
        content = self.deep_entry.get()
        try:
            self.master.planting_depth = float(content)
        except ValueError:
            self.master.set_message(f'{content} is not a number')

    def set_z_tray(self):
        content = self.z_tray_entry.get()
        try:
            self.master.z_tray = float(content)
        except ValueError:
            self.master.set_message(f'{content} is not a number')

    def set_z_scan(self):
        content = self.height_entry.get()
        try:
            self.master.z_scan = float(content)
        except ValueError:
            self.master.set_message(f'{content} is not a number')

    def set_crop(self):
        self.master.crop = self.crop_entry.get()
