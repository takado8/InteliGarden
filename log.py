import os
import datetime

class Log:

    log_file_path = os.path.join(os.path.dirname(__file__), 'data','log', 'log.txt')
    # error_log_file_path = os.path.join(os.path.dirname(__file__), 'data','log', 'error_log.txt')
    # working_log_file_path = os.path.join(os.path.dirname(__file__), 'data','log', 'working_log.txt')
    
    @staticmethod
    def append(msg):
        today = datetime.datetime.today()
        msg = str(today)[:-7] + "   " + msg + "\r\n"
        print(msg)
        if os.path.isfile(Log.log_file_path):
            file = open(Log.log_file_path, 'a+')     
        else:
            file = open(Log.log_file_path, 'w+')
        file.write(msg)    
        file.close()


  

