from customtkinter import (
    CTkFrame, CTkLabel, CTkImage)
from cv2 import (
        cvtColor, COLOR_BGR2RGB, imread, resize,
        INTER_AREA, circle)
from PIL import Image


class VideoFrame(CTkFrame):

    ''' THIS FRAME SHOWS THE DESIRED IMAGE IN A CTKLABEL
    USING A CTKIMAGE FORMAT FOR IMAGES '''

    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.video_label = CTkLabel(self, text=None)
        self.video_label.grid(
                row=0, column=0,
                padx=10, pady=5,
                sticky='nsew')

        self.load_default_image()

    def set_image(self, image):

        ''' RECIBES AN IMAGE, THEN CONVERTS TO CTK IMAGE
        AND FINALLY SHOWS IT IN CTKLABEL '''
        image = cvtColor(image, COLOR_BGR2RGB)
        height, width = image.shape[:2]

        center_x, center_y = width // 2, height // 2

        circle(
            image, (center_x, center_y),
            1, (0, 0, 255), 1)

        image = self.convert_image(image, 1)
        self.video_label.configure(text='', image=image)

    def set_graph(self, graph):
        graph = self.convert_image(graph, 1.5)
        self.video_label.configure(text='', image=graph)

    def convert_image(self, img, scale):

        ''' TAKES AND IMAGE, THEN CONVERTS IT TO PIL.IMAGE
        AND FINALLY TO CTKIMAGE '''

        img_pil = Image.fromarray(img)
        img_ctk = CTkImage(
                light_image=img_pil,
                size=(img.shape[1]*scale, img.shape[0]*scale))
        return img_ctk

    def load_default_image(self):

        ''' READS AN DEFAULT IMAGE TO SHOW UNTIL CAMERA IS
        CONNECTED '''

        img = imread('/home/user/autonomous_sowing_system/theSower/stage2/.theme/default.jpg')
        new_size = (1280, 720)
        img = resize(img, new_size, interpolation=INTER_AREA)
        self.set_image(img)
