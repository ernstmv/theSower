from time import sleep
from threading import Thread
import serial.tools.list_ports as s
from serial import Serial, SerialException


class Robot:

    '''THIS CLASS MANAGES THE CARTESIAN ROBOT, IT CAN:
    DETECT PORTS,
    CREATE CONNECTIONS,
    READ AND WRITE SERIAL MESSAGES,
    UPDATE COORDINATES,
    MOVE TO SPECIFIC POSITIONS'''

    def __init__(self, master):
        self.master = master

        self.port = None
        self.robot = None
        self.absolute = False
        self.is_connected = False
        self.busy = False
        self.x_pos = 0

    # ----------------------------------PORTS--------------------------------
    def search_ports(self):
        '''GET THE AVAILABLE SERIAL PORTS AND SAVES THEM IN A LIST'''
        return [p.device for p in s.comports() if 'tty' in p.description]

    def set_port(self, port):
        '''SETS THE ROBOT PORT'''
        self.port = port

    # -----------------------------ROBOT-STATE-------------------------------
    def robot_on(self):
        '''UPDATES INTERFACE TO ON AND ENABLES ROBOT RELATIVE MOVEMENT'''
        self.is_connected = True
        self.unlock()
        self.relative_mode()
        Thread(target=self.update_coordinates).start()

    def robot_off(self):
        self.master.disconnect_robot()

    def unlock(self):
        '''UNLOKS THE ROBOT AFTER A RESTART'''
        self.void_write('$X')
        self.master.set_message('Robot unlocked')

    def relative_mode(self):
        '''SETS RELATIVE COORDINATES MODE'''
        self.void_write('G91')
        self.absolute = False
        self.master.set_message('Relative coordinates mode')

    def absolute_mode(self):
        '''SETS ABSOLUTE COORDINATES MODE'''
        self.void_write('G90')
        self.absolute = True
        self.master.set_message('Absolute coordinates mode')

    # --------------------------------CONNECTION--------------------------
    def connect_robot(self):

        '''TRY TO CONNECT, IF THEN UPDATES UI, ELSE THROWS ERROR'''

        try:
            self.robot = Serial(self.port, 115200, timeout=0.1)
            sleep(2)
            self.robot_on()
        except (SerialException, AttributeError):
            self.master.set_message(f'Cant connect robot at port {self.port}')

    def autoconnect(self):

        '''TRY TO CONNECT TO THE FIRST PORT IF IT IS'''

        ports = self.search_ports()
        if ports:
            self.set_port(ports[0])
            self.connect_robot()
        else:
            self.master.set_message('No serial devices found')

    # -------------------------COMUNNICATION---------------------------
    def read_serial(self):

        '''READS THE SERIAL BUFFER'''

        if self.is_connected and not self.busy:
            self.busy = True
            try:
                self.robot.reset_input_buffer()
                return self.robot.readline().decode('utf-8').strip()
            except Exception as e:
                self.robot_off()
                self.master.set_message('Connection lost...')
            finally:
                self.busy = False

    def write_serial(self, mssg):

        '''WRITES IN THE SERIAL BUFFER'''
        while True:
            if  not self.busy:
                self.busy = True
                try:
                    self.robot.reset_output_buffer()
                    self.robot.write(f'{mssg}\n'.encode())
                    self.robot.flush()
                except Exception as e:
                    self.robot_off()
                finally:
                    self.busy = False
                    break
            else:
                sleep(0.01)
                continue

    def void_write(self, mssg):

        '''WRITES IN THE SERIAL BUFFER AND TRASH RESPONSE'''
        self.write_serial(mssg)
        self.read_serial()

    def response_write(self, mssg):
        self.write_serial(mssg)
        while True:
            resp = self.read_serial()
            if resp and 'ok' in resp: break

    # ------------------MOVEMENT-METHODS----------------------

    def keys_manager(self, event):
        '''THIS FUNCTION INTERPRETS THE KEYS AND SEND COMMANDS'''
        if not self.is_connected: return
    
        step = 0.2
        key = event.keysym.lower()
        commands = {'w':'X-', 's':'X', 'a':'Y-', 'd':'Y', 'j':'Z-','k':'Z'}

        if key == 'h':
            self.go_home()
        elif key == 'r':
            if self.absolute:
                self.relative_mode()
            else:
                self.absolute_mode()
            
        elif key in commands.keys() and not self.absolute:
            self.void_write(f'G0 {commands[key]}{step}')

    def go_to(self, x=None, y=None, z=None):
        '''IF PASSED, THEN MOVES TO THERE IN ABS COORDINATES'''
        if x: self.void_write(f'G0 X{x}')
        if y: self.void_write(f'G0 Y{y}')
        if z: self.void_write(f'G0 Z{z}')


    def go_home(self):
        '''MOVES THE ROBOT TO THE HOME'''
        self.master.busy()
        self.master.update()
        self.response_write('$H')
        self.master.set_message('Robot on origin')
        self.master.not_busy()

    def recon_config(self):
        '''TAKES ROBOT TO START POSITION'''
        self.absolute_mode()
        self.go_to(y='-8.2', z='-18.2')
        self.void_write("$110=100")

    def pause(self, time):
        self.void_write(f'G4 P{time}')

    # ---------------------------COORDINATES---------------------------

    def get_coordinates(self):
        '''THIS FUNCTION REQUEST THE ROBOT COORDINATES'''
        self.write_serial('?')
        resp = self.read_serial()
        if resp and 'MPos' in resp:
            return resp.split('|')[1].split(':')[1].split(',')

    def update_coordinates(self):
        '''THIS FUNCTION UPDATES DE GUI WITH THE NEW
        ROBOT COORDINATES'''
        while self.robot:
            try:
                resp = self.get_coordinates() 
                if resp:
                    xax, yax, zax = resp
                    self.x_pos = float(xax)
                    self.master.set_coords(xax, yax, zax)
            except Exception:
                pass
            finally:
                sleep(0.2)

    def __del__(self):
        self.robot.close()
