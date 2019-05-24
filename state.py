import os
import json
import time
from ftp import Ftp
from log import Log

class State:
    state_file_path = os.path.join(os.path.dirname(__file__), 'data','state.json')
    state_server_file_path = os.path.join(os.path.dirname(__file__), 'data','state_server.json')

    @staticmethod
    def sync():
        Ftp.download_file(State.state_server_file_path, 'state.json')
        time.sleep(1)
        server_state = State.load_state_from_server_file()
        local_state = State.load_state_from_file()
        local_state['pump_1_interval'] = server_state['pump_1_interval']
        local_state['pump_2_interval'] = server_state['pump_2_interval']
        local_state['pump_1_water_amount'] = server_state['pump_1_water_amount']
        local_state['pump_2_water_amount'] = server_state['pump_2_water_amount']
        if server_state['tank_refilled'] == True: # tank refilled
            local_state['water_level'] = server_state['tank_capacity']
            local_state['tank_refilled'] = False
        State.save_state_to_file(local_state)
        Ftp.upload_file(State.state_file_path, 'state.json')
        time.sleep(1)
        Log.append('state sync.')
        
    
    @staticmethod
    def load_state_from_server_file():
        if os.path.isfile(State.state_server_file_path):
            with open(State.state_server_file_path) as json_file:  
                return json.load(json_file)

    @staticmethod
    def save_state_to_file(state_obj):
        with open(State.state_file_path, 'w') as fp:
            json.dump(state_obj, fp)

    @staticmethod
    def load_state_from_file():
        if os.path.isfile(State.state_file_path):
            with open(State.state_file_path) as json_file:  
                return json.load(json_file)
        else:  # init state dict and file
            state_dict = {
                'water_level': None,    # water volume in tank, in mililiters
                'tank_capacity': None, # water tank max capacity
                'tank_refilled': False, # water tank has been refilled
                'low_water_level_alert': False, # tank water level sensor input
                'water_reserve_state': None,  # if water level is LOW, this is more precise than general water_level
                'dry_alert_1': None,          # for how many sec dry alert is on
                'dry_alert_2': None,          
                'last_rain' : None,          # time.time()
                'last_loop_time': None,   # time.time() value for last loop in run() func
                'pump_1_interval': None,     # time in seconds between watering cycles
                'pump_2_interval': None,
                'pump_1_water_amount': None, # water volume that will be pumped on one watering event
                'pump_2_water_amount': None,
                'pump_1_last_watering': None, # time.time()
                'pump_2_last_watering': None
                }
            # State.save_state_to_file(state_dict)  we call it in control class.
            return state_dict

