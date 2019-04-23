import RPi.GPIO as gp
from pump import Pump
from moisture_sensors import MSensor
from water_level import WaterLevel

class Control:
    # pumps
    PUMP_1 = None
    PUMP_2 = None
    # moisture sensors
    M_SENSOR_1 = None
    M_SENSOR_2 = None
    # rain sensor
    RAIN_SENSOR = None
    # water level sensor
    WATER_LEVEL_SENSOR = None
    # pins
    PUMP_1_pin = 17
    PUMP_2_pin = 27
    M_SENSOR_1_pin = 14
    M_SENSOR_2_pin = None
    M_SENSORS_RELAY_pin = 12
    RAIN_SENSOR_pin = None
    WATER_LEVEL_SENSOR_pin_out = 1
    WATER_LEVEL_SENSOR_pin_in = 7

    def __init__(self):
        # settings
        gp.setmode(gp.BCM)
        gp.setwarnings(False)
        # pumps
        self.PUMP_1 = Pump(gp, self.PUMP_1_pin)
        self.PUMP_2 = Pump(gp, self.PUMP_2_pin)
        # moisture sensors
        self.M_SENSOR_1 = MSensor(gp, self.M_SENSOR_1_pin, self.M_SENSORS_RELAY_pin)
        # water level sensor
        self.WATER_LEVEL_SENSOR = WaterLevel(gp, self.WATER_LEVEL_SENSOR_pin_out, self.WATER_LEVEL_SENSOR_pin_in)


    def __del__(self):
        print('Cleanup on end.')
        gp.cleanup()
