
import RPi.GPIO as gp
from pump import Pump


class Control:
    # pumps
    PUMP_1 = None
    PUMP_2 = None
    # pins
    PUMP_1_pin = 17
    PUMP_2_pin = 27

    def setup_gpio(self):
        # settings
        gp.setmode(gp.BCM)
        gp.setwarnings(False)
        # pumps
        gp.setup([self.PUMP_1_pin, self.PUMP_2_pin], gp.OUT, initial=gp.HIGH)
        self.PUMP_1 = Pump()
        self.PUMP_1.pin = self.PUMP_1_pin
        self.PUMP_1.gp = gp


