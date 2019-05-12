import os
import datetime

class Log:

    info_log_file_path = os.path.join(os.path.dirname(__file__), 'data','log', 'info_log.txt')
    error_log_file_path = os.path.join(os.path.dirname(__file__), 'data','log', 'error_log.txt')
    working_log_file_path = os.path.join(os.path.dirname(__file__), 'data','log', 'working_log.txt')
    
    @staticmethod
    def append(msg, log_file_path):
        today = datetime.datetime.today()
        msg = str(today)[:-7] + " :  " + msg + "\r\n"
        if os.path.isfile(log_file_path):
            file = open(log_file_path, 'a+')
            file.write(msg)
        else:
            file = open(log_file_path, 'w+')
            file.write(msg)
        file.close()


  

