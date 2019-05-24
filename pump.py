import time
from log import Log

class Pump:
    gp = None
    pin = None
    id = None

    WORKING = 1
    NOT_WORKING = 0

    def __init__(self, gp, pin, id):
        self.gp = gp
        self.pin = pin
        self.id = id
        gp.setup(pin, gp.OUT, initial=gp.HIGH)

    def state(self):
        # 0 - on
        # 1 - off
        if self.gp.input(self.pin) == 0:
            return self.WORKING
        else:
            return self.NOT_WORKING

    def turn_on(self):
        Log.append('Turning on pump... ' + str(self.id))
        # if self.pin is not None and not self.is_working:
        self.gp.output(self.pin, 0)
        Log.append('...turned on')

    def turn_off(self):
        Log.append('Turning off pump ' + str(self.id))
        self.gp.output(self.pin, 1)
        Log.append('...turned off')

    def turn_on_for_time(self, seconds):
        self.turn_on()
        time.sleep(seconds)
        self.turn_off()

    def pump_ml(self, mililiters, water_level):
        # 100ml pumps in 17 sec from 600ml
        tank_max = 600
        time_needed = (mililiters * (16 + ((tank_max - water_level) / 100))) / 100
        self.turn_on()
        time.sleep(time_needed)
        self.turn_off()
        return True