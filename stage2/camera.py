from pyudev import Context
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, flip


class Camera:

    '''THIS CLASS MANAGES CAMERA, IT CAN GET PORTS, CREATE CONNECTIONS
    AND GET IMAGES'''

    def __init__(self, master):
        self.available_cameras = []
        self.port = None
        self.camera = None
        self.is_connected = False
        self.device = None
        self.master = master

    def get_ports(self):

        '''THIS METHOD SCAN FOR AVAILABLE CAMERA PORTS (USB PORTS)
        AND RETURNS A LIST OF TUPLES, (DEVICE NAME, PORT)'''

        self.available_cameras = []
        context = Context()
        for device in context.list_devices(subsystem='video4linux'):
            self.available_cameras.append((
                device.get('ID_MODEL', 'Desconocido'),
                device.device_node
                ))

    def set_port(self, port):

        '''SETS CAMERA PORT'''

        self.port = port

    def set_device(self, device):

        '''THIS METHOD SETS THE NAME OF THE CAMERA'''

        self.device = device

    def connect_camera(self):

        '''CONNECTS CAMERA TO SELF.CAMERA_PORT AND CHECKS CONNECTION'''

        self.camera = VideoCapture(self.port)
        width = 1280
        height = 720
        self.camera.set(CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(CAP_PROP_FRAME_HEIGHT, height)
        self.is_connected, _ = self.camera.read()

        if self.is_connected:
            self.master.camera_on()
            self.master.set_message(
                    f'{self.device} camera at {self.port}')
        else:
            self.master.set_message(
                    f'Camera not found at port {self.port}')

    def get_image(self):

        '''READS SELF.CAMERA TO GET IMAGES, ONE EACH TIME
        IF CANT, THEN RELEASE RESOURCES AND UPDATES APP'''

        if self.camera:
            self.is_connected, frame = self.camera.read()
            if not self.is_connected:
                self.set_port(None)
                self.set_device(None)
                self.master.stop_video = True
                self.master.camera_off()
                self.master.controls_frame.camera_to_play()
                self.master.set_message('Cannot get image, camera error')
                return None
            return flip(frame, -1)
        self.master.set_message("Not camera connected")
        return None

    def autoconnect(self):

        '''SEARCHES FOR PORTS AND CONNECTS CAMERA TO
        /DEV/VIDEO2 IF AVAILABLE, THE DEFAULT USB CAMERA'''

        self.get_ports()
        for device, port in self.available_cameras:
            if port in ('/dev/video3', '/dev/video2'):
                self.set_port(port)
                self.set_device(device)
                self.connect_camera()
                return None
            continue

        self.master.set_message('Not camera found, check connection manually')
        return None
