from customtkinter import CTkFrame, CTkLabel, CTkImage
from cv2 import cvtColor, COLOR_BGR2RGB, imread, resize, INTER_AREA, arrowedLine, circle
from PIL import Image


class VideoFrame(CTkFrame):

    '''
    THIS FRAME SHOWS THE DESIRED IMAGE IN A CTKLABEL USING
    A CTKIMAGE FORMAT FOR IMAGES
    '''

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

        '''
        RECIBES AN IMAGE, THEN CONVERTS TO CTK IMAGE AND FINALLY SHOWS
        IT IN CTKLABEL
        '''
        height, width = image.shape[:2]
        
        # Calcular el centro de la imagen
        center_x, center_y = width // 2, height // 2
        
        # Dibujar las flechas
        gap = 10
        thickness = 1
        arrow_size = 50
        # Flecha derecha
        arrowedLine(
            image, (center_x + gap, center_y), 
            (center_x + gap + arrow_size, center_y),
            (255, 0, 0), thickness, tipLength=1)
        # Flecha izquierda
        arrowedLine(
            image, (center_x - gap, center_y),
            (center_x - gap - arrow_size, center_y),
            (255, 0, 0), thickness, tipLength=1)
        # Flecha abajo
        arrowedLine(
            image, (center_x, center_y + gap),
            (center_x, center_y + gap + arrow_size),
            (255, 0, 0), thickness, tipLength=1)
        # Flecha arriba
        arrowedLine(
            image, (center_x, center_y - gap),
            (center_x, center_y - gap - arrow_size),
            (255, 0, 0), thickness, tipLength=1)
        
        # Dibujar el círculo central
        circle(
            image, (center_x, center_y),
            1, (0, 0, 255), thickness)

        image = self.convert_image(image)
        self.video_label.configure(text='', image=image)

    def convert_image(self, image):

        '''
        TAKES AND IMAGE, THEN CONVERTS IT TO PIL.IMAGE AND FINALLY TO CTKIMAGE
        '''

        scale = 1
        img = cvtColor(image, COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_ctk = CTkImage(
                light_image=img_pil,
                size=(int(img.shape[1]*scale), int(img.shape[0]*scale)))
        return img_ctk

    def load_default_image(self):

        '''
        READS AN DEFAULT IMAGE TO SHOW UNTIL CAMERA IS CONNECTED
        '''

        scale = 0.8
        img = imread('/home/ernstmv/theSower/stage2/.theme/default.jpg')
        height, width = img.shape[:2]
        new_size = (int(width*scale), int(height*scale))
        img = resize(img, new_size, interpolation=INTER_AREA)
        self.set_image(img)
