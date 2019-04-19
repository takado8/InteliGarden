import time


class Pump:
    gp = None
    pin = None
    is_working = False
    tested = False

    def state(self):
        return self.gp.input(self.pin)

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

