from customtkinter import CTkFrame, CTkButton

class ExtraFrame(CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=0)

        self.exit_button = CTkButton(
            self, text=' ',
            fg_color='#D90D1E',
            hover_color='#084F8C',
            anchor='center',
            width=30, height=30)
        self.exit_button.grid(
            row=0, column=0,
            padx=10, pady=10)

        self.config_button = CTkButton(
            self, text=' ',
            fg_color='#2074C3',
            hover_color='#084F8C',
            anchor='center',
            width=30, height=30)
        self.config_button.grid(
            row=0, column=1,
            padx=10, pady=10)

        self.config_button = CTkButton(
            self, text=' ',
            fg_color='#0CA491',
            hover_color='#084F8C',
            anchor='center',
            width=30, height=30)
        self.config_button.grid(
            row=0, column=2,
            padx=10, pady=10)

    def launch_config_window(self):
        pass

    def exit_action(self):
        pass
