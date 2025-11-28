from customtkinter import CTkFrame, CTkImage, CTkLabel, StringVar
from cv2 import cvtColor, COLOR_BGR2RGB
from PIL import Image


class ScanFrame(CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)

        self.grid_columnconfigure((0), weight=1)

        message = "The z scan directly affects the precision of the \
                identification system, altought it also makes the recognition\
                faster, make sure you are setting the most effective value or \
                use the defaults"

        self.picture_label = CTkLabel(self)
        self.picture_label.grid(
                row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.info_label = CTkLabel(self, text=message, textcolor='#E8352C')
        self.info_label.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

    def set_image(self, image):

        ''' RECIBES AN IMAGE, THEN CONVERTS TO CTK IMAGE
        AND FINALLY SHOWS IT IN CTKLABEL '''
        height, width = image.shape[:2]

        image = self.convert_image(image)
        self.video_label.configure(text='', image=image)

    def convert_image(self, image):

        ''' TAKES AND IMAGE, THEN CONVERTS IT TO PIL.IMAGE
        AND FINALLY TO CTKIMAGE '''

        img = cvtColor(image, COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_ctk = CTkImage(
                light_image=img_pil,
                size=(img.shape[1], img.shape[0]))
        return img_ctk
