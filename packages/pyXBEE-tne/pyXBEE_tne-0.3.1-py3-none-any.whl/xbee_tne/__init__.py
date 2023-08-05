from time import sleep
import threading
import serial
from . import parser

class XBEEDevice:
    """ Superclass for all device. """

    def __init__(self, Frame):
        self.messagetype = Frame.messagetype
        self.devicetype = Frame.devicetype
        self.source_address = Frame.source_address

class XBEEEvent:
    """ Abstract class for all events. """
    
    def __init__(self,device):
        self.device = device

class SensorEvent:
    """ Concrete class for sensor events """

    def __init__(self, Frame):
        device = XBEEDevice(Frame)
        super(SensorEvent, self).__init__(device)

        self.values = {}
        self.Frame = Frame
        if isinstance(Frame, parser.WeatherStation):
            self.values['DHT22 temperature'] = Frame.DHT22_temp
            self.values['DHT22 humidity'] = Frame.DHT22_hum
            self.values['BMP280 pressure'] = Frame.BMP280_pres
            self.values['BMP280 temperature'] = Frame.BMP280_temp
            self.values['BME280 pressure'] = Frame.BME280_pres
            self.values['BME280 temperature'] = Frame.BME280_temp
            self.values['BME280 humidity'] = Frame.BME280_hum
            self.values['Luminescence'] = Frame.BH1750_lum
            self.values['UV index'] = Frame.UVM30A_uv

        if isinstance(Frame, parser.TestSensor):
            self.values['DHT22 temperature'] = Frame.DHT22_temp

class XBEEConnection:
    """ Abstract superclass for all connection mechanisms """

    @staticmethod
    def parse(frame):
        """ Parse the given data and return an XBEE Event """
        if frame is None:
            return None
        Frame = parser.parse(frame)
        if Frame is not None:
            if isinstance(Frame, parser.SensorFrame):
                obj = SensorEvent(Frame)
            else:
                obj = None #ControlEvent(Frame)

            # Store the latest RF signal data
            obj.data = frame
            return obj
        return None

    def close(self):
        """ close connection to rfxtrx device """
        pass

class SerialConnection(XBEEConnection):
    """ Implementation of a connection using PySerial """

    def __init__(self, port, baudrate, debug=False):
        self.debug = debug
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self._run_event = threading.Event()
        self._run_event.set()
        self.connect()

    def connect(self):
        """ Open a serial connexion """
        self.serial = serial.Serial(self.port, self.baudrate, timeout=0.1)

    def receive_blocking(self):
        """ Wait until a packet is received and return with an FrameEvent """
        data = None
        while self._run_event.is_set():
            try:
                data = self.serial.read()
            except TypeError:
                continue
            except serial.serialutil.SerialException:
                import time
                try:
                    self.connect()
                except serial.serialutil.SerialException:
                    time.sleep(5)
                    continue
            if not data or data is not 0x7E:
                continue
            frame = bytearray(1)
            frame[0] = data
            
            # Read the length (byte 2 and 3) (try again if timeout)
            try:
                data = self.serial.read(2)
            except serial.serialutil.SerialTimeoutException:
                import time
                time.sleep(0.1)
                try:
                    data = self.serial.read(2)
                except:
                    continue
            length = int.from_bytes(data,byteorder='big')
            frame.extend(bytearray(data))
            
            # Read remainder of data frame (try again of timeout)
            try:
                data = self.serial.read(4+length-3)
            except serial.serialutil.SerialTimeoutException:
                import time
                time.sleep(0.1)
                try:
                    data = self.serial.read(4+length-3)
                except:
                    continue
            frame.extend(bytearray(data))

            if self.debug:
                print("XBEE: Recv: " +
                      " ".join("0x{0:02x}".format(x) for x in frame))

            return self.parse(frame)

    def send(self, data):
        """ Send the given packet """
        if isinstance(data, bytearray):
            frame = data
        elif isinstance(data, (bytes, str)):
            frame = bytearray(data)
        else:
            raise ValueError("Invalid type")
        if self.debug:
            print("RFXTRX: Send: " +
                  " ".join("0x{0:02x}".format(x) for x in frame))
        self.serial.write(frame)


    def close(self):
        """ close connection to rfxtrx device """
        self._run_event.clear()
        self.serial.close()


class DummyConnection(XBEEConnection):
    """ Dummy transport for testing purposes """

    def __init__(self, device="", debug=True):
        self.device = device
        self.debug = debug

        api = []
        api.append(0x7E)    # begin
        api.append(0x00)    # length
        api.append(0x14)
        api.append(0x90)    # Frame type
        api.append(0xff)    # Address
        api.append(0xff)
        api.append(0xff)
        api.append(0xff)
        api.append(0xff)
        api.append(0xff)
        api.append(0xff)
        api.append(0xff)
        api.append(0xff)    # Address network
        api.append(0xfe)
        api.append(0x01)    # Receive options
        api.append(0x02)    # Msg type
        api.append(0x01)    # Device class
        api.append(0x00)    # Sensor type
        api.append(0x01)
        api.append(0x33)    # Data
        api.append(0x33)
        api.append(0xb3)
        api.append(0x41)

        api_byte = bytes(api)
        api.append((0xff - sum(api_byte[3:]) & 0xff))
        api_byte = bytes(api)

        self.api_byte = api_byte

    def receive(self, data=None):
        """ Emulate a receive by parsing the given data """
        if data is None:
            return None
        frame = bytearray(data)
        if self.debug:
            print("RFXTRX: Recv: " +
                  " ".join("0x{0:02x}".format(x) for x in frame))
        return self.parse(frame)

    def receive_blocking(self, data=None):
        """ Emulate a receive by parsing the given data """
        return self.receive(self.api_byte)

    def send(self, data):
        """ Emulate a send by doing nothing (except printing debug info if
            requested) """
        pkt = bytearray(data)
        if self.debug:
            print("RFXTRX: Send: " +
            " ".join("0x{0:02x}".format(x) for x in pkt))


class Connect:
    """ The main class for my XBEE-network """

    def __init__(self, port, baudrate, event_callback=None, debug=False, connection_type=SerialConnection):
        self._run_event = threading.Event()
        self._run_event.set()
        self._sensors = {}
        self._status = None
        self._debug = debug
        self.event_callback = event_callback

        self.connection = connection_type(port, baudrate, debug)
        self._thread = threading.Thread(target=self._connect)
        self._thread.setDaemon(True)
        self._thread.start()


    def _connect(self):
        """ Connect """
        
        while self._run_event.is_set():
            event = self.connection.receive_blocking()


    def sensors(self):
        """ Return all found sensors. return: dict of :class:`Sensor` instances. """
        return self._sensors

    def close_connection(self):
        """ Close connection to rfxtrx device """
        self._run_event.clear()
        self.connection.close()
        self._thread.join()

class Core(Connect):
    """ The main class for rfxcom-py. Has changed name to Connect """