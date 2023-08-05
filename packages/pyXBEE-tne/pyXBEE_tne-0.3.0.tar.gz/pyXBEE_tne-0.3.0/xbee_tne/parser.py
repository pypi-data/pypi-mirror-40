import struct

# Define device classes
DEVICE_CLASS_WEATHER = 1
DEVICE_CLASS_MOTION = 2
DEVICE_CLASS_SENSOR = 4
DEVICE_CLASS_FAN = 8

# Define message types
MESSAGE_CONFIG = 1
MESSAGE_STATE = 2
MESSAGE_SET = 4
MESSAGE_PARAM_SET = 8

def parse(frame):

    frame_type = frame[3]

    if frame_type == 0x90:
        obj = process_rx_frame(frame)
    else:
        return None

    return obj

def process_rx_frame(frame):
    """ Process data in rx frame type (0x90) """
     
    # Determine if checksum is OK
    if (frame[-1] + sum(frame[3:-1]) & 0xff) == 0xff:
        # Find message type
        if (frame[15] == MESSAGE_STATE):
            if (frame[16] == DEVICE_CLASS_WEATHER):
                obj = WeatherStation()
            elif (frame[16] == DEVICE_CLASS_MOTION):
                return None
            elif (frame[16] == DEVICE_CLASS_SENSOR):
                return None
            elif (frame[16] == DEVICE_CLASS_FAN):
                return None
            else:
                return None
        else:
            return None
            
        obj.load_receive(frame)
        return obj
    else:
        return None

class Frame:
    """ Abstract superclass for all low level packets """

    def __init__(self):
        """Constructor"""
        self.data = None
        self.framelength = None
        self.frametype = None
        self.messagetype = None
        self.devicetype = None
        self.source_address = None
        self.network_address = None
        self.checksum = None

    def has_value(self, datatype):
        """Return True if the sensor supports the given data type.
        sensor.has_value(RFXCOM_TEMPERATURE) is identical to calling
        sensor.has_temperature().
        """
        return hasattr(self, datatype)

    def value(self, datatype):
        """Return the :class:`SensorValue` for the given data type.
        sensor.value(RFXCOM_TEMPERATURE) is identical to calling
        sensor.temperature().
        """
        return getattr(self, datatype, None)

    def __getattr__(self, name):
        typename = name.replace("has_", "", 1)
        if not name == typename:
            return lambda: self.has_value(typename)
        raise AttributeError(name)

    def __eq__(self, other):
        if not isinstance(other, Frame):
            return False
        return self.id_string == other.id_string

    def __str__(self):
        return self.id_string

    def __repr__(self):
        return self.__str__()

class SensorFrame(Frame):
    """ Superclass for sensors """

    # Define sensor types
    SENSOR_DHT22_TEMPERATURE = 1
    SENSOR_DHT22_HUMIDITY = 2
    SENSOR_BMP280_PRESSURE = 4
    SENSOR_BMP280_TEMPERATURE = 8
    SENSOR_BME280_PRESSURE = 16
    SENSOR_BME280_TEMPERATURE = 32
    SENSOR_BME280_HUMIDITY = 64
    SENSOR_BH1750_LUMINESCENCE = 128
    SENSOR_UVM30A_UV = 256
    SENSORS = [SENSOR_DHT22_TEMPERATURE, SENSOR_DHT22_HUMIDITY,SENSOR_BMP280_PRESSURE,SENSOR_BMP280_TEMPERATURE,
            SENSOR_BME280_PRESSURE,SENSOR_BME280_TEMPERATURE,SENSOR_BME280_HUMIDITY,SENSOR_BH1750_LUMINESCENCE,SENSOR_UVM30A_UV]
    SENSORS_NAMES = ['Temperature_DHT22','Humidity_DHT22','Pressure_BMP280','Temperature_BMP280','Pressure_BME280','Temperature_BME280','Humidity_BME280','Luminescence','UV index']
    SENSORS_TYPES = ['Temperature', 'Humidity', 'Pressure', 'Temperature', 'Pressure', 'Temperature', 'Humidity', 'Luminescence', 'UV index']
    SENSORS_UNITS = ['C','%','hPa','C','hPa','C','%','Lux','']

class WeatherStation(SensorFrame):
    """ Data class for my weather station """

    def __init__(self):
        """Constructor"""
        super(WeatherStation, self).__init__()
        self.DHT22_temp = None
        self.DHT22_hum = None
        self.BMP280_pres = None
        self.BMP280_temp = None
        self.BME280_pres = None
        self.BME280_temp = None
        self.BME280_hum = None
        self.BH1750_lum = None
        self.UVM30A_uv = None

    def load_receive(self, frame):
        """Load data from a bytearray"""
        self.data = frame[15:-1]
        self.framelength = int.from_bytes(frame[1:3],byteorder='big')
        self.frametype = frame[3]
        self.messagetype = self.data[0]
        self.devicetype = self.data[1]
        self.source_address = int.from_bytes(frame[4:12],byteorder='big')
        self.network_address = int.from_bytes(frame[12:14],byteorder='big')
        self.checksum = frame[-1]

        self.DHT22_temp = struct.unpack('<f',self.data[4:8])[0]
        self.DHT22_hum = struct.unpack('<f',self.data[8:12])[0]
        self.BMP280_pres = struct.unpack('<f',self.data[12:16])[0]
        self.BMP280_temp = struct.unpack('<f',self.data[16:20])[0]
        self.BME280_pres = struct.unpack('<f',self.data[20:24])[0]
        self.BME280_temp = struct.unpack('<f',self.data[24:28])[0]
        self.BME280_hum = struct.unpack('<f',self.data[28:32])[0]
        self.BH1750_lum = int.from_bytes(self.data[32:36],byteorder='little')
        self.UVM30A_uv = int.from_bytes(self.data[36:40],byteorder='little')