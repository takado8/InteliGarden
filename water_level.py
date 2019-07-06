import time
from log import Log

class WaterLevel:
    # GPIO object and pins numbers
    gp = None
    pin_out = None
    pin_in = None
    # states
    HIGH = 1
    LOW = 0

    def __init__(self, gp, pin_out, pin_in):
        self.gp = gp
        self.pin_out = pin_out
        self.pin_in = pin_in
        gp.setup(pin_out, gp.OUT, initial=gp.LOW)
        gp.setup(pin_in, gp.IN, pull_up_down=gp.PUD_DOWN)
    
    def state(self):
        try:
            self.gp.output(self.pin_out, self.gp.HIGH)
            time.sleep(1)
            input_state = self.gp.input(self.pin_in)
            time.sleep(1)
            self.gp.output(self.pin_out, self.gp.LOW)
        except Exception as ex:
            Log.append('water level sensore error')
            Log.append(str(ex))
            return self.LOW

        if input_state == 1:
            return self.HIGH
        else:
            return self.LOW