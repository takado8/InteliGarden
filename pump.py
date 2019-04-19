import time
from enum import Enum


class Pump:
    gp = None
    pin = None
    is_working = False

    WORKING = 1
    NOT_WORKING = 0

    def __init__(self, gp, pin):
        self.gp = gp
        self.pin = pin
        gp.setup(pin, gp.OUT, initial=gp.HIGH)

    def state(self):
        # 0 - on
        # 1 - off
        if self.gp.input(self.pin) == 0:
            return self.WORKING
        else:
            return self.NOT_WORKING

    def turn_on(self):
        print('turning on')
        # if self.pin is not None and not self.is_working:
        self.gp.output(self.pin, 0)
        self.is_working = True

    def turn_off(self):
        print('turning off')
        # if self.pin is not None:# and self.is_working:
        self.gp.output(self.pin, 1)
        self.is_working = False

    def turn_on_for_time(self, seconds):
        self.turn_on()
        time.sleep(seconds)
        self.turn_off()

    # class state(Enum):
    #     WORKING = 1
    #     NOT_WORKING = 0
