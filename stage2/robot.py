from time import sleep
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
        self.busy = False
        self.master.bind("<KeyPress>", self.send_command)

    def get_ports(self):
        '''GET THE AVAILABLE SERIAL PORTS AND SAVES THEM IN A LIST'''
        self.a_prts = [
                p.device for p in s.comports() if 'tty' in p.description]

    def set_port(self, port):
        '''SETS THE ROBOT PORT'''
        self.port = port

    def robot_on(self):
        self.master.robot_on()
        self.unlock()
        self.standard()
        self.update_coordinates()

    def unlock(self):
        self.write_serial('$X')
        resp = self.read_serial()
        while 'Unlocked' not in resp:
            self.write_serial('$X')
            resp = self.read_serial()
        self.master.set_message('Robot unlocked')

    def standard(self):
        self.write_serial('G91')
        if 'ok' in self.read_serial():
            self.master.set_message('Relative coordinates mode')

    def robot_off(self):
        self.master.robot_off()

    def connect_robot(self):

        '''TRY TO CONNECT, IF THEN UPDATES UI, ELSE THROWS ERROR'''

        try:
            self.robot = Serial(self.port, 115200, timeout=0.1)
            sleep(2)
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

        if self.is_connected and not self.busy:
            self.robot.reset_input_buffer()
            self.busy = True
            try:
                resp = self.robot.readline().decode('utf-8').strip()
                if resp is not None and 'Alarm' in resp:
                    self.master.set_message("Alarm detected, robot blocked")
                    self.robot_off()
                return resp
            except (SerialException, AttributeError):
                self.robot_off()
            finally:
                self.busy = False
        return None

    def write_serial(self, mssg):

        '''WRITES IN THE SERIAL BUFFER'''
        if self.is_connected and not self.busy:
            self.robot.reset_output_buffer()
            self.busy = True
            try:
                self.robot.write(f'{mssg}\n'.encode())
                self.robot.flush()
            except OSError:
                self.robot_off()
            finally:
                self.busy = False

    def send_command(self, event):
        step = 0.2
        key = event.keysym.lower()
        mssg = None
        if key == 'w':
            mssg = f'G0 X-{step}'
        elif key == 's':
            mssg = f'G0 X{step}'
        elif key == 'a':
            mssg = f'G0 Y-{step}'
        elif key == 'd':
            mssg = f'G0 Y{step}'
        elif key == 'k':
            mssg = f'G0 Z{step}'
        elif key == 'j':
            mssg = f'G0 Z-{step}'
        elif key == 'h':
            mssg = '$H'

        if mssg:

            self.write_serial(mssg)
            self.read_serial()
            self.update_coordinates()


    def update_coordinates(self):
        self.write_serial('?')
        resp = self.read_serial()
        if resp is not None and 'MPos' in resp:
            xax, yax, zax = resp.split('|')[1].split(':')[1].split(',')
            self.master.set_x_coord(xax)
            self.master.set_y_coord(yax)
            self.master.set_z_coord(zax)
