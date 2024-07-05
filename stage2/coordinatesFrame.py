from customtkinter import CTkFrame, CTkLabel, CTkEntry


class CoordinatesFrame(CTkFrame):

    def __init__(self, master):

        super().__init__(master)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(tuple(i for i in range(6)), weight=1)

        self.title_label = CTkLabel(self, text='Coordinates')
        self.title_label.grid(
                row=0, column=0,
                columnspan=6,
                padx=10, pady=10,
                sticky='ew')

        self.x_label = CTkLabel(self, text='X:')
        self.x_label.grid(
                row=1, column=0,
                padx=10, pady=0,
                sticky='ew')
        self.y_label = CTkLabel(self, text='Y:')
        self.y_label.grid(
                row=1, column=2,
                padx=10, pady=0,
                sticky='ew')
        self.z_label = CTkLabel(self, text='Z:')
        self.z_label.grid(
                row=1, column=4,
                padx=10, pady=0,
                sticky='ew')

        self.x_entry = CTkEntry(self, state='disabled')
        self.y_entry = CTkEntry(self, state='disabled')
        self.z_entry = CTkEntry(self, state='disabled')

        self.x_entry.grid(
                row=1, column=1,
                padx=10, pady=0,
                sticky='ew')
        self.y_entry.grid(
                row=1, column=3,
                padx=10, pady=0,
                sticky='ew')
        self.z_entry.grid(
                row=1, column=5,
                padx=10, pady=0,
                sticky='ew')
