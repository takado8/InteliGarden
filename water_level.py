

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
        gp.setup(pin_out, gp.OUT, initial=gp.HIGH)
        gp.setup(pin_in, gp.IN)
    
    def state(self):
        if self.gp.input(self.pin_in) == 1:
            return self.HIGH
        else:
            return self.LOW