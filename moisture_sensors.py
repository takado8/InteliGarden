import time
from log import Log

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
        gp.setup(sensor_pin, gp.IN, pull_up_down=gp.PUD_UP)
        gp.setup(relay_pin, gp.OUT, initial=gp.HIGH)

    def state(self):
        # turn on sensor, measure, turn off
        try:
            self.gp.output(self.relay_pin, self.gp.LOW)
        
            time.sleep(1)
            state = self.gp.input(self.sensor_pin)
            time.sleep(1)
            self.gp.output(self.relay_pin, self.gp.HIGH)
            time.sleep(1)
        except Exception as ex:
            Log.append('moisture sensore error')
            Log.append(str(ex))
            state = 1
        # 0 - over the threshold
        # 1 - below the threshold
        if state == 0:
            return self.WET
        else:
            return self.DRY
