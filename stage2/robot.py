from time import sleep
from threading import Thread
import serial.tools.list_ports as s
from serial import Serial, SerialException


class Robot:

    '''
    THIS CLASS MANAGES THE CARTESIAN ROBOT CAN DETECT PORTS, CREATE CONNECTIONS
    READ AND WRITE SERIAL MESSAGES
    '''

    def __init__(self, master):
        self.master = master
        self.a_prts = []
        self.port = None
        self.robot = None
        self.is_connected = False

    def get_ports(self):
        '''GET THE AVAILABLE SERIAL PORTS AND SAVES THEM IN A LIST'''
        self.a_prts = [prt.device for prt in s.comports() if 'tty' in prt.description]

    def set_port(self, port):
        '''SETS THE ROBOT PORT'''
        self.port = port

    def robot_on(self):
        self.master.robot_on()
        Thread(target=self.communicate).start()

    def robot_off(self):
        self.master.robot_off()

    def connect_robot(self):

        '''TRY TO CONNECT, IF THEN UPDATES UI, ELSE THROWS ERROR'''

        try:
            self.robot = Serial(self.port, 115200, timeout=0.1)
            sleep(3)
            self.robot_on()
        except (SerialException, AttributeError):
            self.master.set_message(f'Cant connect robot at port {self.port}')
            self.robot_off()

    def autoconnect(self):

        '''TRY TO CONNECT TO THE FIRST PORT IF IT IS'''

        self.get_ports()
        if self.a_prts:
            self.set_port(self.a_prts[0])
            self.connect_robot()
        else:
            self.master.set_message('No serial devices found')

    def read_serial(self):

        '''READS THE SERIAL BUFFER'''

        if self.is_connected:
            try:
                return self.robot.readline().decode('utf-8').strip()
            except (SerialException, AttributeError):
                self.robot_off()
        return None

    def write_serial(self, mssg):

        '''WRITES IN THE SERIAL BUFFER'''
        if self.is_connected:
            try:
                self.robot.write(f'{mssg}\n'.encode())
                self.robot.flush()
            except OSError:
                self.robot_off()

    def communicate(self):
        while self.is_connected:
            self.update_coordinates()
            sleep(0.1)
        print('Hilo terminado')

    def update_coordinates(self):
        self.write_serial('?')
        resp = self.read_serial()
        if resp is not None and 'MPos' in resp:
            xax, yax, zax = resp.split('|')[1].split(':')[1].split(',')
            self.master.set_x_coord(xax)
            self.master.set_y_coord(yax)
            self.master.set_z_coord(zax)
