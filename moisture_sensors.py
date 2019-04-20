import time

class MSensor:
    sensor_pin = None
    relay_pin = None
    gp = None
    # states
    WET = 1
    DRY = 0

    def __init__(self, gp, sensor_pin, relay_pin):
        self.gp = gp
        self.sensor_pin = sensor_pin
        self.relay_pin = relay_pin
        gp.setup(sensor_pin, gp.IN)
        gp.setup(relay_pin, gp.OUT, initial=gp.HIGH)

    def state(self):
        # turn on sensor, measure, turn off
        self.gp.output(self.relay_pin, self.gp.LOW)
        time.sleep(1)
        state = self.gp.input(self.sensor_pin)
        time.sleep(1)
        self.gp.output(self.relay_pin, self.gp.HIGH)
        # 0 - over the threshold
        # 1 - below the threshold
        if state == 0:
            return self.WET
        else:
            return self.DRY