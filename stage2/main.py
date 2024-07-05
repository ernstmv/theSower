from customtkinter import set_appearance_mode, set_default_color_theme
from app import App


def main():
    set_appearance_mode('dark')
    set_default_color_theme('/home/ernstmv/theSower/stage2/.theme/theme.json')
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
