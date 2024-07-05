from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton


class InfoFrame(CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure(tuple(i for i in range(0, 5)), weight=1)

        self.title_label = CTkLabel(self, text='Process information')
        self.title_label.grid(
                row=0, column=0,
                columnspan=6,
                sticky='ew',
                padx=10, pady=5)

        self.tray_size_label = CTkLabel(self, text='Tray size:')
        self.holes_label = CTkLabel(self, text='Viable holes:')
        self.crop_label = CTkLabel(self, text='Crop:')
        self.seeded_label = CTkLabel(self, text='Sown holes:')
        self.progresas_label = CTkLabel(self, text='Progress:')
        self.time_label = CTkLabel(self, text='Time transcurred:')

        self.tray_size_label.grid(
                row=1, column=0,
                padx=5, pady=0,
                sticky='ew')
        self.holes_label.grid(
                row=1, column=1,
                padx=5, pady=0,
                sticky='ew')
        self.crop_label.grid(
                row=1, column=2,
                padx=5, pady=0,
                sticky='ew')
        self.seeded_label.grid(
                row=1, column=3,
                padx=5, pady=0,
                sticky='ew')
        self.progresas_label.grid(
                row=1, column=4,
                padx=5, pady=0,
                sticky='ew')
        self.time_label.grid(
                row=1, column=5,
                padx=5, pady=0,
                sticky='ew')

        self.tray_size_entry = CTkEntry(self, state='disabled')
        self.holes_entry = CTkEntry(self, state='disabled')
        self.crop_entry = CTkEntry(self, state='disabled')
        self.seeded_entry = CTkEntry(self, state='disabled')
        self.progresas_entry = CTkEntry(self, state='disabled')
        self.time_entry = CTkEntry(self, state='disabled')

        self.tray_size_entry.grid(
                row=2, column=0,
                padx=5, pady=10,
                sticky='ew')
        self.holes_entry.grid(
                row=2, column=1,
                padx=5, pady=10,
                sticky='ew')
        self.crop_entry.grid(
                row=2, column=2,
                padx=5, pady=10,
                sticky='ew')
        self.seeded_entry.grid(
                row=2, column=3,
                padx=5, pady=10,
                sticky='ew')
        self.progresas_entry.grid(
                row=2, column=4,
                padx=5, pady=10,
                sticky='ew')
        self.time_entry.grid(
                row=2, column=5,
                padx=5, pady=10,
                sticky='ew')
