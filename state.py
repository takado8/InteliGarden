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
        time.sleep(0.5)
        server_state = State.load_state_from_server_file()
        local_state = State.load_state_from_file()
        local_state['pump_1_interval'] = server_state['pump_1_interval']
        local_state['pump_2_interval'] = server_state['pump_2_interval']
        local_state['pump_1_water_amount'] = server_state['pump_1_water_amount']
        local_state['pump_2_water_amount'] = server_state['pump_2_water_amount']
        local_state['tank_capacity'] = server_state['tank_capacity']
        if server_state['tank_refilled'] == 1: # tank refilled
            local_state['water_level'] = local_state['tank_capacity']
            local_state['tank_refilled'] = 0
            local_state['low_water_level_alert'] = 0
            Log.append('tank refilled')
        if server_state['run_test'] == 2: # test request
            if local_state['run_test'] == 0: # request not taken
                local_state['run_test'] = 2
            elif local_state['run_test'] == 1: # request satisfied
                local_state['run_test'] = 0


        State.save_state_to_file(local_state)
        Ftp.upload_file(State.state_file_path, 'state.json')
        #Log.append('state sync.')
        
    
    @staticmethod
    def load_state_from_server_file():
        if os.path.isfile(State.state_server_file_path):
            with open(State.state_server_file_path) as json_file:  
                state_dict = json.load(json_file)
                # for val in state_dict:
                #     state_dict[val] = float(state_dict[val])
                return state_dict

    @staticmethod
    def save_state_to_file(state_obj):
        with open(State.state_file_path, 'w') as fp:
            json.dump(state_obj, fp)

    @staticmethod
    def load_state_from_file():
        if os.path.isfile(State.state_file_path):
            with open(State.state_file_path) as json_file:  
                state_dict = json.load(json_file)
                # for val in state_dict:
                #     state_dict[val] = float(state_dict[val])
                return state_dict
        else:  # init state dict and file
            state_dict = {
                'water_level': 0,    # water volume in tank, in mililiters
                'tank_capacity': 0, # water tank max capacity
                'tank_refilled': 0, # water tank has been refilled; 0 or 1
                'low_water_level_alert': 0, # tank water level sensor input; 0 or 1
                'dry_alert_1': 0,          # for how many sec dry alert is on
                'dry_alert_2': 0,          
                'last_rain' : 0,          # time.time()
                'last_loop_time': 0,   # time.time() value for last loop in run() func
                'pump_1_interval': 0,     # time in seconds between watering cycles
                'pump_2_interval': 0,
                'pump_1_water_amount': 0, # water volume that will be pumped on one watering event
                'pump_2_water_amount': 0,
                'pump_1_last_watering': 0, # time.time()
                'pump_2_last_watering': 0,
                'run_test': 0
                }
            # State.save_state_to_file(state_dict)  we call it in control class.
            return state_dict

