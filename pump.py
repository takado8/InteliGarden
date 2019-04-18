import time


class Pump:
    gp = None
    pin = None
    is_working = False
    tested = False

    def turn_on(self):
        print('turning on')

        #if self.pin is not None and not self.is_working:
        self.gp.setup(self.pin, 0)
        self.is_working = True

    def turn_off(self):
        print('turning off')
        #if self.pin is not None:# and self.is_working:
        self.gp.setup(self.pin, 1)
        self.is_working = False

    def turn_on_for_time(self, seconds):
        if self.pin is not None and not self.is_working:
            print('turning on for ' +  str(seconds)+' seconds')
            self.gp.setup(self.pin, 0)
            self.is_working = True
            time.sleep(seconds)
            self.gp.setup(self.pin, 1)
            self.is_working = False
            print('turning off')
