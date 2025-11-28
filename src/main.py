from customtkinter import set_appearance_mode, set_default_color_theme
from app import App
from os import getcwd

CURRENT_DIRECTORY = getcwd()


def main():
    set_appearance_mode('dark')
    set_default_color_theme(CURRENT_DIRECTORY + '/.theme/theme.json')
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
