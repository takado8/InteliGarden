import RPi.GPIO as gp
from pump import Pump



pump1.turn_on_for_time(5)

class Control:
	# pumps
	PUMP_1 = None
	PUMP_2 = None
	# pins
	PUMP_1_pin = 17
	PUMP_2_pin = 27
	
	def setup_gpio(self):
		pin = [17,27]
		gp.setmode(gp.BCM)
		gp.setwarnings(0)
		gp.setup(pin, gp.OUT)
		pump1 = Pump()
		pump1.pin = pin
		pump1.gp = gp
