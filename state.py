import os
import pickle



class State:
    state_file_path = os.path.join(os.path.dirname(__file__), 'data','state.pkl')

    @staticmethod
    def sync_local_and_server_state():
        pass

    @staticmethod
    def save_state_to_file(state_obj):
        with open(State.state_file_path, 'wb') as f:
            pickle.dump(state_obj, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_state_from_file():
        if os.path.isfile(State.state_file_path):
            with open(State.state_file_path, 'rb') as f:
                return pickle.load(f)
        else:  # init state dict and file
            state_dict = {
                'water_level': None,    # water volume in tank, in mililiters
                'low_water_level_alert': False,
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

