import os
import RPi.GPIO as gp
from datetime import datetime
import time
from pump import Pump
from moisture_sensors import MSensor
from water_level import WaterLevel
from state import State
from log import Log

class Control:
    # water volume is always expressed in mililiters, any time lenght is in seconds, and time of last event is time.time() seconds
    # call functions in run() every n seconds
    step_delay_time = 7200   # == 2h
    # state
    state =  {}
    # pumps
    PUMP_1 = None
    PUMP_2 = None
    # moisture sensors
    M_SENSOR_1 = None
    M_SENSOR_2 = None
    # rain sensor
    RAIN_SENSOR = None
    # water level sensor
    WATER_LEVEL_SENSOR = None
    water_tank_max_capacity = 1000 # ml
    water_reserve_capacity = 500 # mililiters
    # pins
    PUMP_1_pin = 17
    PUMP_2_pin = 27
    M_SENSOR_1_pin = 14
    M_SENSOR_2_pin = None
    M_SENSORS_RELAY_pin = 12
    RAIN_SENSOR_pin = None
    WATER_LEVEL_SENSOR_pin_out = 1
    WATER_LEVEL_SENSOR_pin_in = 7

    def __init__(self):
        # GPIO settings
        gp.setmode(gp.BCM)
        gp.setwarnings(False)
        # read state file
        self.state = State.load_state_from_file()
        # pumps
        self.PUMP_1 = Pump(gp, self.PUMP_1_pin, id=1)
        self.PUMP_2 = Pump(gp, self.PUMP_2_pin, id=2)
        # moisture sensors
        self.M_SENSOR_1 = MSensor(gp, self.M_SENSOR_1_pin, self.M_SENSORS_RELAY_pin)
        # water level sensor
        self.WATER_LEVEL_SENSOR = WaterLevel(gp, self.WATER_LEVEL_SENSOR_pin_out, self.WATER_LEVEL_SENSOR_pin_in)
       

    def __del__(self):
        # An app should never be closed, so if it does, it means something crashed probably. Add to error log, send user a warning
        # and restart app
        print('Cleanup on end.')
        gp.cleanup()

    def run(self):
        # check if all necessary variables are assigned in self.state
            if self.state['water_level'] is None:
                Log.append('Water level is none. Check if tank is full. Aborting.', Log.info_log_file_path)
                return
            
            if self.state['pump_1_interval'] is None:   ## later --> or self.state['pump_2_interval']
                Log.append('pump 1 interval is None, setting it for 5 days as default for now', Log.info_log_file_path)
                self.state['pump_1_interval'] = 432000  # 5 days
            
            if self.state['pump_1_water_amount'] is None:
                Log.append('pump 1 water amount is None, setting it for 50 ml as default for now', Log.info_log_file_path)
                self.state['pump_1_water_amount'] = 50

        while True:
            
            if self.state['last_loop_time'] is None or time.time() - self.state['last_loop_time'] > self.step_delay_time: # perform step
                
                # check water level 
                if self.WATER_LEVEL_SENSOR.state == WaterLevel.LOW:
                    self.state['low_water_level_alert'] = True
                    if self.state['water_reserve_state'] is None:
                        self.state['water_reserve_state'] = self.reserve_capacity
                else:
                    if self.state['low_water_level_alert'] == True:  # if alert was True, and now is not, refill happend
                        self.state['low_water_level_alert'] = False
                        self.state['water_reserve_state'] = None
                        self.state['water_level'] = self.water_tank_max_capacity   #  tank is always refilled fully.
                
                # #
                # rain sensor check
                # if there was a rain, and moisture sensor state == WET - skip this watering cycle, but when moisture sensor show state==DRY
                # water right away. But this will affect whole schedule, so correction will be needed. It would be good to find out how
                # long and intense rain was. Also, temperature difference on non-raing days may vary a lot, if there was scoarching for last
                # few days, an earlier watering may be needed. Light sensor could do the trick.
                # #

                # moisture sensors check
                if self.M_SENSOR_1.state == MSensor.DRY:
                    if self.state['dry_alert_1'] == None:
                        self.state['dry_alert_1'] = time.time()
                    else:
                        dry_time = time.time() - self.state['dry_alert_1']
                        if dry_time > 259200:  # 3 days
                            # emergency watering, alert for user etc.
                            pass
                else:
                    if self.state['dry_alert_1'] is not None:
                        self.state['dry_alert_1'] = None
                
                # check if watering is scheduled 
                # PUMP_1
                if self.state['pump_1_last_watering'] is None or time.time() - self.state['pump_1_last_watering'] > self.state['pump_1_interval']:
                    # watering is needed
                    if self.state['low_water_level_alert'] == True:
                        # send warning to user APK
                        Log.append("low water level in main tank.", Log.info_log_file_path)    
                        if self.state['water_reserve_state'] < self.state['pump_1_water_amount'] + 50:
                            # if water is out, don't run pumps.
                            Log.append("Water is over in main tank.", Log.error_log_file_path)    
                            Log.append("Water is over in main tank.", Log.error_log_file_path)    
                            # send alert to user APK    
                            pass
                        else:
                            # run pump
                            if self.PUMP_1.pump_ml(self.state['pump_1_water_amount']):
                                self.state['water_reserve_state'] -= self.state['pump_1_water_amount']
                                self.state['water_level'] -= self.state['pump_1_water_amount']   # remove it from here later.
                                self.state['pump_1_last_watering'] = time.time()
                            else:
                                # write to error log
                                pass
                    else:
                        # run pump
                        if self.PUMP_1.pump_ml(self.state['pump_1_water_amount']):
                            self.state['water_level'] -= self.state['pump_1_water_amount']
                            self.state['pump_1_last_watering'] = time.time()
                        else:
                            # write to an error log
                            pass
                # #
                # same for PUMP_2 
                # #

                # on loop end.
                if self.state['last_loop_time'] is None or time.time() - self.state['last_loop_time'] > self.step_delay_time + 60:
                    self.state['last_loop_time'] = time.time()
                State.save_state_to_file(self.state)