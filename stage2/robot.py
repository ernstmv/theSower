import serial.tools.list_ports
from serial import Serial, SerialException
from time import sleep


class Robot:

    '''
    THIS CLASS MANAGES THE CARTESIAN ROBOT CAN DETECT PORTS, CREATE CONNECTIONS
    READ AND WRITE SERIAL MESSAGES
    '''

    def __init__(self, master):
        self.master = master
        self.available_ports = []
        self.port = None
        self.robot = None

    def get_ports(self):
        self.available_ports = []
        ports = serial.tools.list_ports.comports()

        for port in ports:
            if "tty" in port.description:
                self.available_ports.append(port.device)

    def set_port(self, port):
        self.port = port

    def connect_robot(self):
        try:
            self.robot = Serial(self.port, 115200, timeout=0.1)
            sleep(3)
            self.master.robot_on()
            self.master.controls_frame.robot_to_off()
            self.master.set_message(f'Robot connected at {self.port}')
        except SerialException:
            self.master.set_message(
                    f'Unable to connect with robot at port {self.port}')
            self.port = None
            self.master.robot_off()
            self.master.controls_frame.robot_to_on()

    def autoconnect(self):
        self.get_ports()
        if len(self.available_ports) > 0:
            self.set_port(self.available_ports[0])
            self.connect_robot()
            return None
        self.master.set_message('No serial devices available')
        return None

    def read_serial(self):
        pass

    def write_serial(self, mssg):
        pass
