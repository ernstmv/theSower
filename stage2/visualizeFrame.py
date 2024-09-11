from customtkinter import (
        CTkFrame, CTkLabel, CTkImage, CTkEntry, CTkProgressBar)
from PIL import Image
from cv2 import cvtColor, COLOR_BGR2RGB


class VisualizeFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.date_label = CTkLabel(self, text='Date:')
        self.crop_label = CTkLabel(self, text='Crop:')
        self.greenhouse_label = CTkLabel(self, text='Greenhouse:')
        self.viable_label = CTkLabel(self, text='Viable holes:')
        self.sown_label = CTkLabel(self, text='Sown holes:')
        self.time_label = CTkLabel(self, text='Time:')
        self.progress_label = CTkLabel(self, text='Progress:')

        self.date_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.crop_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.greenhouse_label.grid(
                row=2, column=0, padx=10, pady=10, sticky='w')
        self.viable_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.sown_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.time_label.grid(row=5, column=0, padx=10, pady=10, sticky='w')
        self.progress_label.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        self.date_entry = CTkEntry(self, state='disabled')
        self.crop_entry = CTkEntry(self, state='disabled')
        self.greenhouse_entry = CTkEntry(self, state='disabled')
        self.viable_entry = CTkEntry(self, state='disabled')
        self.sown_entry = CTkEntry(self, state='disabled')
        self.time_entry = CTkEntry(self, state='disabled')
        self.progress_bar = CTkProgressBar(self, orientation='horizontal')

        self.date_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.crop_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.greenhouse_entry.grid(
                row=2, column=1,
                padx=10, pady=10,
                sticky='w')
        self.viable_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.sown_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        self.time_entry.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        self.progress_bar.grid(row=6, column=1, padx=10, pady=10, sticky='ew')

        self.progress_bar.set(0)

    def set_date(self, date):
        self.date_entry.configure(state='normal')
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, date)
        self.date_entry.configure(state='disabled')

    def set_crop(self, crop):
        self.crop_entry.configure(state='normal')
        self.crop_entry.delete(0, 'end')
        self.crop_entry.insert(0, crop)
        self.crop_entry.configure(state='disabled')

    def set_greenhouse(self, greenhouse):
        self.greenhouse_entry.configure(state='normal')
        self.greenhouse_entry.delete(0, 'end')
        self.greenhouse_entry.insert(0, greenhouse)
        self.greenhouse_entry.configure(state='disabled')

    def set_tray(self, tray):
        self.tray_entry.configure(state='normal')
        self.tray_entry.delete(0, 'end')
        self.tray_entry.insert(0, tray)
        self.tray_entry.configure(state='disabled')

    def set_viable(self, viable):
        self.viable_entry.configure(state='normal')
        self.viable_entry.delete(0, 'end')
        self.viable_entry.insert(0, viable)
        self.viable_entry.configure(state='disabled')

    def set_sown(self, sown):
        self.sown_entry.configure(state='normal')
        self.sown_entry.delete(0, 'end')
        self.sown_entry.insert(0, sown)
        self.sown_entry.configure(state='disabled')

    def set_time(self, time):
        self.time_entry.configure(state='normal')
        self.time_entry.delete(0, 'end')
        self.time_entry.insert(0, time)
        self.time_entry.configure(state='disabled')

    def set_progress(self, progress):
        self.progress_bar.set(progress)

    def set_graph(self, graph):
        graph = self.convert(graph)
        self.graph_iamge.configure(text=None, image=graph)

    def convert(self, graph):
        img = cvtColor(graph, COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_ctk = CTkImage(
                light_image=img_pil,
                size=(int(img.shape[1]*1), int(img.shape[0]*1)))
        return img_ctk
