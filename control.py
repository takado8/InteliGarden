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
    STEP_TIME = 60     # 7200 s == 2h
    # state
    state =  {}
    # pumps
    pump_1 = None
    pump_2 = None
    # moisture sensors
    m_sensor_1 = None
    m_sensor_2 = None
    # rain sensor
    rain_sensor = None
    # water level sensor
    water_level_sensor = None
    WATER_RESERVE_CAPACITY = 5000 # ml
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
        Log.append("Init Control.")
        # GPIO settings
        gp.setmode(gp.BCM)
        gp.setwarnings(False)
        # read state file
        self.state = State.load_state_from_file()
        # init pumps
        self.pump_1 = Pump(gp, self.PUMP_1_pin, id=1)
        self.pump_2 = Pump(gp, self.PUMP_2_pin, id=2)
        # moisture sensors
        self.m_sensor_1 = MSensor(gp, self.M_SENSOR_1_pin, self.M_SENSORS_RELAY_pin)
        # water level sensor
        self.water_level_sensor = WaterLevel(gp, self.WATER_LEVEL_SENSOR_pin_out, self.WATER_LEVEL_SENSOR_pin_in)
       
    def __del__(self):
        print('Cleanup on end.')
        gp.cleanup()

    def tank_refilled(self):
        Log.append('Tank refilled.')
        self.state['low_water_level_alert'] = 0
        self.state['water_level'] = self.state['tank_capacity']   #  tank is always refilled fully.
        State.save_state_to_file(self.state)

    def pumped(self, pump_nr):
        self.state['water_level'] -= self.state['pump_'+str(pump_nr)+'_water_amount']
        self.state['pump_'+str(pump_nr)+'_last_watering'] = time.time()
        Log.append('Pump '+str(pump_nr)+' pumped ' + str(self.state['pump_'+str(pump_nr)+'_water_amount']) + ' ml. ' +\
             str(self.state['water_level']) +' ml left in tank.')

    def run(self):
        # check if all necessary variables are assigned in self.state
        if self.state['water_level'] is None:
            warning = 'Water level is none. Check if tank is full. Aborting.'
            Log.append(warning)
            print(warning)
            return
        
        if self.state['pump_1_interval'] is None:   ## later --> or self.state['pump_2_interval']
            warning = 'pump 1 interval is None.'
            Log.append(warning)
            print(warning)
            return
        
        if self.state['pump_1_water_amount'] is None:
            warning = 'pump 1 water amount is None.'
            Log.append(warning)
            print(warning)
            return

        while True:
            if self.state['last_loop_time'] is None or time.time() - self.state['last_loop_time'] >= self.STEP_TIME: # perform step
                Log.append('--------------- New Loop ----------------')
                
                State.sync()
                self.state = State.load_state_from_file()
                # #
                # rain sensor check
                # if it was raining and moisture sensor state == WET - skip this watering cycle, but when moisture sensor show state==DRY
                # water right away. But this will affect whole schedule, so correction will be needed. It would be good to find out how
                # long and intense rain was. Also, temperature difference on non-raing days may vary a lot, if there was scoarching for last
                # few days, an earlier watering might be needed. Light sensor could do the trick.
                # #

                # moisture sensors check
                m1_state = self.m_sensor_1.state()
                if m1_state == MSensor.DRY:
                    if self.state['dry_alert_1'] == 0:
                        self.state['dry_alert_1'] = time.time()
                        Log.append('Moisturness sensor 1 is dry.')
                    else:
                        dry_time = time.time() - self.state['dry_alert_1']
                        # if dry_time > 60 * 3:  # 3 min
                        #     Log.append('Moisturness sensor 1 is dry for 3 mins now.')
                        #     # emergency watering, alert for user etc.
                else:
                    if self.state['dry_alert_1'] != 0:
                        Log.append('Moisturness sensor 1 is wet again.')
                        self.state['dry_alert_1'] = 0
                
                # #
                # second sensor
                # #

                # check if watering is scheduled 
                # PUMP_1
                if self.state['pump_1_last_watering'] is None or time.time() - self.state['pump_1_last_watering'] >= self.state['pump_1_interval']:
                    # watering is needed
                    Log.append('Pump 1 watering is required.')
                    if self.state['low_water_level_alert'] == 1:
                        # send warning to user APK
                        Log.append("Low water level in main tank.")    
                        if self.state['water_level'] < self.state['pump_1_water_amount']:
                            # if no water, don't run pumps.
                            Log.append("Water tank is empty. Skipping watering.")
                            # send alert to user APK    
                        else:
                            # run pump
                            if self.pump_1.pump_ml(self.state['pump_1_water_amount']):
                                self.pumped(pump_nr=1)
                            else:
                                # write to error log
                                Log.append('Pump 1 watering error.')
                    else: # no water level alert
                        # run pump
                        if self.pump_1.pump_ml(self.state['pump_1_water_amount']):
                            self.pumped(pump_nr=1)
                        else:
                            # write to an error log
                            Log.append('Pump 1 watering error.')
                
                # #
                # same for PUMP_2 
                # #

                # check water level
                if self.water_level_sensor.state() == WaterLevel.LOW:
                    if self.state['low_water_level_alert'] == 0:
                        Log.append('Low water level reached.' )
                        self.state['low_water_level_alert'] = 1
                        self.state['water_level'] = self.WATER_RESERVE_CAPACITY
                else:
                    if self.state['low_water_level_alert'] == 1:
                        self.tank_refilled()    # if alert was 1, and now is 0, tank was refilled.
               

                # on loop end.
                #if self.state['last_loop_time'] is None or time.time() - self.state['last_loop_time'] > self.step_delay_time + 60:
                self.state['last_loop_time'] = time.time()
                State.save_state_to_file(self.state)
                Log.append('-------------- End of loop --------------')
            else:
                time.sleep(10)