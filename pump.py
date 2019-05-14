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
        print('turning on pump ' + str(self.id))
        Log.append(('turning on pump ' + str(self.id), Log.working_log_file_path)
        # if self.pin is not None and not self.is_working:
        self.gp.output(self.pin, 0)

    def turn_off(self):
        print('turning off pump ' + str(self.id))
        Log.append(('turning off pump ' + str(self.id), Log.working_log_file_path)        # if self.pin is not None:# and self.is_working:
        self.gp.output(self.pin, 1)

    def turn_on_for_time(self, seconds):
        self.turn_on()
        time.sleep(seconds)
        self.turn_off()

    def pump_ml(self, mililiters):
        # 100ml pumps for 33 sec
        time_needed = (mililiters * 33) / 100
        self.turn_on()
        time.sleep(time_needed)
        self.turn_off()
        return True