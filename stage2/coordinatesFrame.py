from customtkinter import CTkFrame, CTkLabel, CTkEntry


class CoordinatesFrame(CTkFrame):

    def __init__(self, master):

        super().__init__(master)
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.x_entry = CTkEntry(self, state='disabled')
        self.y_entry = CTkEntry(self, state='disabled')
        self.z_entry = CTkEntry(self, state='disabled')

        self.x_entry.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='ew')
        self.y_entry.grid(
                row=0, column=1,
                padx=10, pady=10,
                sticky='ew')
        self.z_entry.grid(
                row=0, column=2,
                padx=10, pady=10,
                sticky='ew')

    def set_coords(self, x, y, z):
        self.x_entry.configure(state='normal')
        self.x_entry.delete(0, 'end')
        self.x_entry.insert(0, f'X: {x}')
        self.x_entry.configure(state='disabled')

        self.y_entry.configure(state='normal')
        self.y_entry.delete(0, 'end')
        self.y_entry.insert(0, f'Y: {y}')
        self.y_entry.configure(state='disabled')

        self.z_entry.configure(state='normal')
        self.z_entry.delete(0, 'end')
        self.z_entry.insert(0, f'Z: {z}')
        self.z_entry.configure(state='disabled')
