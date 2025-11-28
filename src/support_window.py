
from customtkinter import CTkToplevel, CTkLabel, CTkImage
from PIL import Image


class SupportWindow(CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("400x400")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.image_label = CTkLabel(self, text=None)
        self.image_label.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky="nsew"
                )

        img_pil = Image.open(".theme/contact.png")
        img_ctk = CTkImage(light_image=img_pil, size=(370, 370))
        self.image_label.configure(text=None, image=img_ctk)
