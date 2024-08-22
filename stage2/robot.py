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
        self.arduino = None
        self.absolute = False
        self.is_connected = False
        self.busy = False

        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0

    # ----------------------------------PORTS------------------
    def search_ports(self):
        '''GET THE AVAILABLE SERIAL PORTS AND SAVES
        THEM IN A LIST'''

        return [p.device for p in s.comports() if 'tty' in p.description]

    def set_port(self, port):
        '''SETS THE ROBOT PORT'''

        self.port = port

    # -----------------------------ROBOT-STATE-----------------
    def robot_on(self):
        '''UPDATES INTERFACE TO ON AND ENABLES
        ROBOT RELATIVE MOVEMENT'''

        self.is_connected = True
        self.master.set_message("Robot connected")
        self.unlock()
        Thread(target=self.update_coordinates).start()

    def robot_off(self):
        '''THIS METHOD DISCONECT THE ROBOT FROM
        THE MASTER CLASS'''

        self.is_connected = False
        self.master.disconnect_robot()

    def unlock(self):
        '''UNLOCKS THE ROBOT AFTER A RESTART'''

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
            self.arduino = Serial(self.port, 115200, timeout=0.1)
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

        if not self.busy:
            self.busy = True
            try:
                self.arduino.reset_input_buffer()
                return self.arduino.readline().decode('utf-8').strip()
            except Exception:
                self.robot_off()
                self.master.set_message('Connection lost...')
            finally:
                self.busy = False

    def write_serial(self, mssg):
        '''WRITES IN THE SERIAL BUFFER'''

        while True:
            if not self.busy:
                self.busy = True
                try:
                    self.arduino.reset_output_buffer()
                    self.arduino.write(f'{mssg}\n'.encode())
                    self.arduino.flush()
                except Exception:
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
        '''WRITES IN THE SERIAL BUFFER AND WAITS AND OK IN RESPONSE'''

        self.write_serial(mssg)
        while True:
            resp = self.read_serial()
            if resp and 'ok' in resp:
                break
            sleep(0.01)

    # ------------------MOVEMENT-METHODS----------------------

    def keys_manager(self, event):
        '''THIS FUNCTION INTERPRETS THE KEYS AND SEND COMMANDS'''

        self.master.busy()
        step = 0.2
        key = event.keysym.lower()
        commands = {
                'w': 'X-', 's': 'X', 'a': 'Y-',
                'd': 'Y', 'j': 'Z-', 'k': 'Z'}

        if key == 'h':
            self.go_home()
        elif key == 'r':
            if self.absolute:
                self.relative_mode()
            else:
                self.absolute_mode()

        elif key in commands.keys() and not self.absolute:
            self.void_write(f'G0 {commands[key]}{step}')
        self.master.not_busy()

    def go_to(self, x=None, y=None, z=None):
        '''IF PASSED, THEN MOVES TO THERE IN ABS COORDINATES'''

        if x:
            self.void_write(f'G0 X{x}')
        if y:
            self.void_write(f'G0 Y{y}')
        if z:
            self.void_write(f'G0 Z{z}')

    def wait_to(self, x=None, y=None, z=None):
        '''THIS METHOD WAITS UNTIL THE ROBOT IS IN THE GIVEN
        COORDINATES'''
        limit = 0
        if x:
            limit += 1
        if y:
            limit += 1
        if z:
            limit += 1

        while True:
            axis = 0
            if x and self.x_pos == x:
                axis += 1
            if y and self.y_pos == y:
                axis += 1
            if z and self.z_pos == z:
                axis += 1
            if axis == limit:
                break
            sleep(0.1)

    def go_home(self):
        '''MOVES THE ROBOT TO THE HOME'''

        self.response_write('$H')
        self.master.set_message('Robot on origin')

    def pause(self, n):
        '''USES THE P FUNCTION TO PAUSE THE ROBOT N SECONDS'''

        self.void_write(f'G4 P{n}')

    def seed(self):
        '''STARTS THE SEEDING SEQUENCE OF THE SOWER MODULE'''

        self.void_write('M15')
    # ---------------------------COORDINATES---------------------------

    def get_coordinates(self):
        '''THIS FUNCTION REQUESTS THE ROBOT COORDINATES'''

        self.write_serial('?')
        resp = self.read_serial()
        if resp and 'MPos' in resp:
            coord = resp.split(':')[1].split(',')
            return coord[0], coord[1], coord[2]

    def update_coordinates(self):
        '''THIS FUNCTION UPDATES DE GUI WITH THE NEW ROBOT COORDINATES'''

        while self.is_connected:
            try:
                resp = self.get_coordinates()
                if resp:
                    xax, yax, zax = resp
                    self.x_pos = round(float(xax), 1)
                    self.y_pos = round(float(yax), 1)
                    self.z_pos = round(float(zax), 1)
                    self.master.set_coords(xax, yax, zax)
            except Exception:
                pass
            finally:
                sleep(0.1)

    def close(self):
        self.arduino.close()
