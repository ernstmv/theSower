from customtkinter import (
        CTkFrame, CTkButton, CTkOptionMenu, CTkLabel, CTkEntry)


class HeaderFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=0)
        self.grid_columnconfigure((6), weight=1)
        self.grid_columnconfigure((7, 8, 9, 10, 11), weight=0)
        self.grid_rowconfigure((0), weight=1)

        greenhouses = [
                'invernadero 1',
                'invernadero 2']
        self.x_label = CTkLabel(self, text='X: ')
        self.x_entry = CTkEntry(self, state='disabled')
        self.y_label = CTkLabel(self, text='Y: ')
        self.y_entry = CTkEntry(self, state='disabled')
        self.z_label = CTkLabel(self, text='Z: ')
        self.z_entry = CTkEntry(self, state='disabled')

        self.x_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.x_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.y_label.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        self.y_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')
        self.z_label.grid(row=0, column=4, padx=10, pady=10, sticky='w')
        self.z_entry.grid(row=0, column=5, padx=10, pady=10, sticky='w')

        self.support_button = CTkButton(
                self, text='Support', command=self.support_window)
        self.greenh_menu = CTkOptionMenu(
                self, values=greenhouses, command=self.select_greenh)
        self.greenhouse_icon = CTkLabel(self, text='󰹖 ')
        self.user_button = CTkButton(
                self, text='User',
                command=self.user_window,
                fg_color='#262626',
                text_color='#fff',
                hover_color='#F2D23A')
        self.user_icon = CTkLabel(self, text=' ')

        self.support_button.grid(row=0, column=7, padx=10, pady=5, sticky='e')
        self.greenh_menu.grid(row=0, column=8, padx=10, pady=5)
        self.greenhouse_icon.grid(row=0, column=9, padx=10, pady=5, sticky='e')
        self.user_button.grid(row=0, column=10, padx=10, pady=5)
        self.user_icon.grid(row=0, column=11, padx=10, pady=5, sticky='e')

    def set_x(self, x):
        self.x_entry.configure(state='normal')
        self.x_entry.delete(0, 'end')
        self.x_entry.insert(0, x)
        self.x_entry.configure(state='disabled')

    def set_y(self, y):
        self.y_entry.configure(state='normal')
        self.y_entry.delete(0, 'end')
        self.y_entry.insert(0, y)
        self.y_entry.configure(state='disabled')

    def set_z(self, z):
        self.z_entry.configure(state='normal')
        self.z_entry.delete(0, 'end')
        self.z_entry.insert(0, z)
        self.z_entry.configure(state='disabled')

    def support_window(self):
        pass

    def user_window(self):
        pass

    def select_greenh(self, choice):
        pass

    def set_coords(self, x, y, z):
        self.set_x(x)
        self.set_y(y)
        self.set_z(z)
