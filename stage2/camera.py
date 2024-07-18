from pyudev import Context
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT


class Camera:

    '''MANAGES CAMERA, IT CAN GET PORTS, CREATE CONNECTIONS
    AND GET IMAGES'''

    def __init__(self, master):

        self.master = master

        self.port = None
        self.name = None
        self.camera = None
        self.is_connected = False

    def set_port(self, port):
        '''SETS CAMERA PORT'''
        self.port = port

    def set_name(self, name):
        '''SETS THE NAME OF THE CAMERA'''
        self.name = name

    def search_devices(self):

        '''SCAN FOR AVAILABLE CAMERA PORTS (USB PORTS)
        AND RETURNS A LIST OF TUPLES, (DEVICE NAME, PORT)'''

        c = Context()
        return [
            (d.get('ID_MODEL' ,'Desconocido'), d.device_node)
            for d in c.list_devices(subsystem='video4linux')]

    def autoconnect(self):

        '''SEARCHES FOR PORTS AND CONNECTS CAMERA TO
        /DEV/VIDEO2 IF AVAILABLE, THE DEFAULT USB CAMERA'''

        for name, port in self.search_devices():
            if 'Integrated_Camera' == name:
                continue
            elif port in ('/dev/video2', '/dev/video3'):
                self.set_port(port)
                self.set_name(name)
                self.connect_camera()
                break
            else:
                self.master.set_message("No USB cameras found")

    def connect_camera(self):

        '''CONNECTS CAMERA TO SELF.CAMERA_PORT AND CHECKS CONNECTION'''

        self.camera = VideoCapture(self.port)
        self.camera.set(CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(CAP_PROP_FRAME_HEIGHT, 720)
        self.is_connected, _ = self.camera.read()

        if not self.is_connected:
            self.master.set_message(
                f'ERROR; Cannot connect camera at {self.port}')
        else:
            self.master.set_message(
                f'Camera connected at {self.port}')

    def get_image(self):

        '''READS SELF.CAMERA TO GET IMAGES, ONE EACH TIME
        ELSE RERTURNS NONE VALUE'''

        self.is_connected, frame = self.camera.read()
        return frame if self.is_connected else None

    def __del__(self):
        try:
            self.camera.release()
        except AttributeError:
            pass
