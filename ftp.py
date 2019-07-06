from ftplib import FTP  
import os


class Ftp:
    HOST_NAME = 'serwer1868028.home.pl'
    USER = 'inteligarden01@serwer1868028.home.pl'
    PASS = 'sgHR5$6yUO12jqQ3'

    @staticmethod
    def upload_file(file_path, ftp_file_name):
        try:
            if os.path.isfile(file_path):
                ftp = FTP(Ftp.HOST_NAME)  
                ftp.login(Ftp.USER, Ftp.PASS)
                with open(file_path, 'rb') as f:  
                    ftp.storbinary('STOR ' + ftp_file_name, f)
                ftp.quit()
            else:
                print('file not found.')
        except Exception as ex:
            print(ex)
        
    @staticmethod
    def download_file(file_path, ftp_file_name):
        try:
            ftp = FTP(Ftp.HOST_NAME)  
            ftp.login(Ftp.USER, Ftp.PASS)
            file = open(file_path, 'wb+')
            ftp.retrbinary("RETR " + ftp_file_name, file.write)
            ftp.quit()
            #print('file downloaded.')
        except Exception as ex:
                print(ex)
