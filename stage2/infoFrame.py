from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton


class InfoFrame(CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.holes_label = CTkLabel(self, text='Viable holes:')
        self.seeded_label = CTkLabel(self, text='Sown holes:')
        self.progress_label = CTkLabel(self, text='Progress:')
        self.time_label = CTkLabel(self, text='Time transcurred:')

        self.holes_label.grid(
                row=0, column=0,
                padx=5, pady=0,
                sticky='ew')
        self.seeded_label.grid(
                row=0, column=1,
                padx=5, pady=0,
                sticky='ew')
        self.progress_label.grid(
                row=0, column=2,
                padx=5, pady=0,
                sticky='ew')
        self.time_label.grid(
                row=0, column=3,
                padx=5, pady=0,
                sticky='ew')

        self.holes_entry = CTkEntry(self, state='disabled')
        self.seeded_entry = CTkEntry(self, state='disabled')
        self.progress_entry = CTkEntry(self, state='disabled')
        self.time_entry = CTkEntry(self, state='disabled')

        self.holes_entry.grid(
                row=1, column=0,
                padx=5, pady=10,
                sticky='ew')
        self.seeded_entry.grid(
                row=1, column=1,
                padx=5, pady=10,
                sticky='ew')
        self.progress_entry.grid(
                row=1, column=2,
                padx=5, pady=10,
                sticky='ew')
        self.time_entry.grid(
                row=1, column=3,
                padx=5, pady=10,
                sticky='ew')

    def set_viable(self, viable):
        self.holes_entry.configure(state='normal')
        self.holes_entry.delete(0, 'end')
        self.holes_entry.insert(0, viable)
        self.holes_entry.configure(state='disabled')

    def set_sown(self, sown):
        self.seeded_entry.configure(state='normal')
        self.seeded_entry.delete(0, 'end')
        self.seeded_entry.insert(0, sown)
        self.seeded_entry.configure(state='disabled')

    def set_progress(self, progress):
        self.progress_entry.configure(state='normal')
        self.progress_entry.delete(0, 'end')
        self.progress_entry.insert(0, progress)
        self.progress_entry.configure(state='disabled')

    def set_time(self, time):
        self.time_entry.configure(state='normal')
        self.time_entry.delete(0, 'end')
        self.time_entry.insert(0, time)
        self.time_entry.configure(state='disabled')
