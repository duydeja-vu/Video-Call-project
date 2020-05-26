import sys
sys.path.append("..")

import sys
import time
from multiprocessing import Process, Queue
import os
from socket import *
from utils import config
from threading import Thread
import pickle




class MainProcessing(object):
    def __init__(self):
        #self.queue_gui_socket = Queue()
        self.client_address = []

    
    def VerifyClientAccount(self, user_data):
        user_status = user_data[0]
        user_name = user_data[1]
        user_pass = user_data[2]
        user_valid = False
        infor_save = user_name + " " + user_pass + " " + "\n"
        server_response = ""

        if user_status == "Register":
            f = open("database.txt","r")
            while True:
                line = f.readline()
                if line == "":
                    user_valid = False
                    break
                else:
                    data = line.split()
                    if user_name == data[0]:
                        user_valid = True
                        break
            f.close()
            if user_valid == False:
                f = open("database.txt","a")
                f.writelines(infor_save)
                f.close()
                server_response = "200_OK"
            else:
                server_response = "500_NOTOK"
        
        if user_status == "Login":
            f = open("database.txt","r")
            while True:
                line = f.readline()
                if line == "":
                    user_valid = False
                    break
                else:
                    data = line.split()
                    if user_name == data[0]:
                        user_valid = True
                        break
            f.close()
            if user_valid == True:
                server_response = "200_OK"
            else:
                server_response = "500_NOTOK"
        return server_response
        

    def StartSocket(self):
        # Create new socket handling verify client account
        main_socket = socket(family=AF_INET, type=SOCK_STREAM)
        main_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            
            main_socket.bind((config.HOST, config.MAIN_PORT))
        except OSError:
            print("Can't bind video port")

        # Create new socket handling client video
        server_video = socket(family=AF_INET, type=SOCK_STREAM)
        server_video.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            server_video.bind((config.HOST, config.VIDEO_PORT))
        except OSError:
            print("Can't bind video port")

        # Create new socket handling client audio
        server_audio = socket(family=AF_INET, type=SOCK_STREAM)
        server_audio.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            server_audio.bind((config.HOST, config.AUDIO_PORT))
        except OSError:
            print("Can't bind audio port")

        main_socket.listen(2)
        print("Main Socket Waiting for connection..")
        # verify_client_account = Thread(target=self.VerifyClientAccount)
        # verify_client_account.start()
        client_socket, client_addr = main_socket.accept()
        mess = client_socket.recv(config.BUFFSIZE)
        user_data = mess.decode('utf-8')
        user_data = eval(user_data)
        user_validate = self.VerifyClientAccount(user_data)
        print(user_validate)

        
            # if mess.decode('utf-8') == "end":
            #     print("End call")
            #     main_socket.close()
            # else:
            #     mess = input("Server: ")
            #     client_socket.send(mess.encode('utf-8'))

        # server_audio.listen(2)
        # print("Waiting for connection..")
        # thread_audio = Thread(target=self.ConnectionsSound)
        # thread_audio.start()

        # server_video.listen(2)
        # print("Waiting for connection..")
        # process_video = Thread(target=self.ConnectionsVideo)
        # process_video.start()


main_processing = MainProcessing()

def main():

    process_socket = Process(target=main_processing.StartSocket)

    process_socket = process_socket.start()

    

if __name__ == "__main__":
    main()
