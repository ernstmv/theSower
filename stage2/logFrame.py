from customtkinter import CTkFrame, CTkTextbox, CTkLabel


class LogFrame(CTkFrame):

    '''
    THIS FRAME SHOWS INFORMATION ABOUT THE SYSTEM JUST LIKE ERRORS
    '''

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.log_textbox = CTkTextbox(
                self, state='disabled',
                width=300, height=200,
                font=("ProFontWindowsNerdFont", 20))
        self.log_textbox.grid(
                row=0, column=0,
                padx=10, pady=5,
                sticky='nsew')

        self.show_greeting_message()

    def set_message(self, mssg):

        '''
        Sets the desired message to the log textbox
        '''

        self.log_textbox.configure(state='normal')
        self.log_textbox.insert('0.0', '>> ' + mssg + '\n')
        self.log_textbox.configure(state='disabled')

    def show_greeting_message(self):
        '''
        SHOWS A GREETING MESSAGE
        '''
        self.set_message('Welcome to The Sower')
