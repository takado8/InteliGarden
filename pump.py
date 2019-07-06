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
        try:
            self.gp.output(self.pin, 0)
            Log.append('...turned on')
        except Exception as ex:
            Log.append('pump \'on\' error '+ str(ex))

    def turn_off(self):
        Log.append('Turning off pump... ' + str(self.id))
        try:
            self.gp.output(self.pin, 1)
            Log.append('...turned off')
        except Exception as ex:
            Log.append('pump \'off\' error '+ str(ex))

    def turn_on_for_time(self, seconds):
        self.turn_on()
        time.sleep(seconds)
        self.turn_off()

    def pump_ml(self, mililiters):
        # 400 ml / 64s  FULL
        time_needed = 64
        loops = round(mililiters / 400, None)
        for i in range(loops):
            self.turn_on_for_time(time_needed)
            print(str(i+1) + '/' + str(loops))
            time.sleep(120)
        return True