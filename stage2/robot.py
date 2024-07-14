from time import sleep
import serial.tools.list_ports as s
from serial import Serial, SerialException


class Robot:

    '''THIS CLASS MANAGES THE CARTESIAN ROBOT, IT CAN DETECT PORTS,
    CREATE CONNECTIONS, AND READ AND WRITE SERIAL MESSAGES'''

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
        self.a_prts = [p.device for p in s.comports() if 'tty' in p.description]

    def set_port(self, port):
        '''SETS THE ROBOT PORT'''
        self.port = port

    def robot_on(self):
        '''UPDATES INTERFACE TO ON AND ENABLES ROBOT RELATIVE MOVEMENT'''
        self.master.robot_on()
        self.unlock()
        self.standard()
        self.update_coordinates()

    def unlock(self):
        '''UNLOKS THE ROBOT AFTER A RESTART'''
        self.void_write('$X')
        self.master.set_message('Robot unlocked')

    def standard(self):
        '''SETS RELATIVE COORDINATES MODE'''
        self.write_serial('G91')
        if 'ok' in self.read_serial():
            self.master.set_message('Relative coordinates mode')

    def robot_off(self):
        '''UPDATES INTERFACE TO OFF'''
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
            self.busy = True
            self.robot.reset_input_buffer()
            try:
                return self.robot.readline().decode('utf-8').strip()
            except (SerialException, AttributeError):
                self.robot_off()
            finally:
                self.busy = False
        return None

    def write_serial(self, mssg):

        '''WRITES IN THE SERIAL BUFFER'''
        if self.is_connected and not self.busy:
            self.busy = True
            self.robot.reset_output_buffer()
            try:
                self.robot.write(f'{mssg}\n'.encode())
                self.robot.flush()
            except OSError:
                self.robot_off()
            finally:
                self.busy = False

    def void_write(self, mssg):

        '''WRITES IN THE SERIAL BUFFER AND TRASH RESPONSE'''
        self.write_serial(mssg)
        self.read_serial()

    def send_command(self, event):
        '''THIS FUNCTION INTERPRETS THE KEYS AND SEND COMMANDS'''
    
        commands = {'w':'X-', 's':'X', 'a':'Y-', 'd':'Y', 'j':'Z-','k':'Z'}
        step = 0.2
        key = event.keysym.lower()
        if key == 'h':
            self.go_home()
            return
        try:
            self.void_write(f'G0 {commands[key]}{step}')
            self.update_coordinates()
        except KeyError:
            pass
        return

    def update_coordinates(self):
        '''THIS FUNCTION UPDATES THE ROBOT COORDINATES'''
        self.write_serial('?')
        resp = self.read_serial()
        if resp and 'MPos' in resp:
            xax, yax, zax = resp.split('|')[1].split(':')[1].split(',')
            self.master.set_x_coord(xax)
            self.master.set_y_coord(yax)
            self.master.set_z_coord(zax)

    def set_abs_mode(self):
        self.void_write('G90')
        self.void_write('G0 Z-50')

    def go_to(self, pos):
        self.write_serial(f'G0 X{pos[0]}')
        self.write_serial(f'G0 Y{pos[1]}')
        sleep(3)

    def get_coordinates(self):
        '''THIS FUNCTION UPDATES THE ROBOT COORDINATES'''
        self.write_serial('?')
        resp = self.read_serial()
        if resp and 'MPos' in resp:
            xax, yax, _ = resp.split('|')[1].split(':')[1].split(',')
            return xax, yax

    def go_home(self):
        '''MOVES THE ROBOT TO THE HOME'''
        self.write_serial('$H')
        resp = ''
        while 'ok' not in resp or resp is None:
            resp = self.read_serial()
        self.update_coordinates()
        self.master.set_message('Robot on origin')

    def get_into_position(self):
        '''MOVES THE ROBOT DOWN, TO START RECOGNISING HOLES'''
        self.void_write('G90')
        self.void_write('G0 Z-18.2')
        self.void_write('G0 Y-8.2')
        self.master.set_message('Robot into start position')
        self.void_write('G91')
