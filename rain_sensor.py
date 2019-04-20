

class RainSensor:
    gp = None
    pin = None

    WET = 1
    DRY = 0

    def __init__(self, gp, pin):
        self.gp = gp
        self.pin = pin
        gp.setup(pin, gp.IN)

    def state(self):
        # 1 - no rain
        # 0 - rain
        if self.gp.input(self.pin) == 0:
            return self.WET
        else:
            return self.DRY