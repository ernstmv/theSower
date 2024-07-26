from customtkinter import (
    CTkFrame, CTkLabel, CTkImage)
from cv2 import (
        cvtColor, COLOR_BGR2RGB, imread, resize,
        INTER_AREA)
from PIL import Image


class VideoFrame(CTkFrame):

    ''' THIS FRAME SHOWS THE DESIRED IMAGE IN A CTKLABEL
    USING A CTKIMAGE FORMAT FOR IMAGES '''

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.title_label = CTkLabel(self, text='Camera')
        self.title_label.grid(
                row=0, column=0,
                padx=10, pady=5,
                sticky='ew')

        self.video_label = CTkLabel(self, text=None)
        self.video_label.grid(
                row=1, column=0,
                padx=10, pady=5,
                sticky='nsew')

        self.load_default_image()

    def set_image(self, image):

        ''' RECIBES AN IMAGE, THEN CONVERTS TO CTK IMAGE
        AND FINALLY SHOWS IT IN CTKLABEL '''

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

    def load_default_image(self):

        ''' READS AN DEFAULT IMAGE TO SHOW UNTIL CAMERA IS
        CONNECTED '''

        scale = 0.8
        img = imread('/home/ernstmv/theSower/stage2/.theme/default.jpg')
        height, width = img.shape[:2]
        new_size = (int(width*scale), int(height*scale))
        img = resize(img, new_size, interpolation=INTER_AREA)
        self.set_image(img)
