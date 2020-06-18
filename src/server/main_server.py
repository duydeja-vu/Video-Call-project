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
import serverVideo


class User(object):
    def __init__(self, my_socket, my_user_name):
        self.addresses = {}
        self.threads = {}


class MainProcessing(object):
    def __init__(self):
        #self.queue_gui_socket = Queue()
        self.user_online = []
        self.count_chat_room = 0
        

    def IsUserOnline(self, user_name):
        return True if self.user_online.count(user_name) != 0 else False

    def VerifyUserAccount(self, user_data):
        # print("user data", user_data)
        user_status = user_data[0]
        user_name = user_data[1]
        user_pass = user_data[2]
        user_valid = False
        infor_save = user_name + " " + user_pass + " " + "\n"
        temp_pass = ""
        server_response = ""

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
                    temp_pass = data[1]
                    break
        f.close()

        if self.IsUserOnline(user_name) == False:
            if user_status == "Register":
                if user_valid == False:
                    f = open("database.txt","a")
                    f.writelines(infor_save)
                    f.close()
                    server_response = "200_OK"
                else:
                    server_response = "500_NOTOK"
            
            if user_status == "Login":
                if user_valid == True and temp_pass == user_pass:
                    server_response = "200_OK"
                else:
                    server_response = "500_NOTOK"
        else:
            if user_status != "Exit":
                server_response = "500_NOTOK"
            else:
                server_response = "EXITOK"
        return server_response

   

    def HandleCallSession(self):
        # print("{} user in Chat Zoom".format(len(self.user_online)))
        # handle_call_process = Process(target=serverMedia.HandleCallSession)
        # handle_call_process.start()
        serverVideo.StartCall()
        
    def StartSocket(self):
        # Create new socket handling verify client account
        self.main_socket = socket(family=AF_INET, type=SOCK_STREAM)
        self.main_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print(self.main_socket)
        try:
            
            self.main_socket.bind((config.HOST, config.MAIN_PORT))
        except OSError:
            print("Can't bind main socket")
            exit(0)

        # serverVideo = socket(family=AF_INET, type=SOCK_STREAM)
        # serverVideo.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # print(serverVideo)

        self.main_socket.listen(10)
        print("Main Socket Waiting for connection..")
        while True: 
            client_socket, client_addr = self.main_socket.accept()
            while True:
                mess = client_socket.recv(config.BUFFSIZE)
                user_data = mess.decode('utf-8')
                print("110", user_data)
                user_data = eval(user_data)
                if len(user_data) != 0:
                    server_response = self.VerifyUserAccount(user_data)
                    client_socket.send(server_response.encode('utf-8'))
                    print("Server respone", server_response)
                    if server_response == "200_OK":
                        self.user_online.append(user_data[1])
                        print(self.user_online)
                        print("LOGIN SUCCESS !")
                        self.HandleCallSession()
                        break
                    elif server_response == "500_NOTOK":
                        print("Login or Register ERR")
                        continue
                    elif server_response == "EXITOK":
                        self.user_online.remove(user_data[1])
                        print(self.user_online)
                        continue
                else:
                    continue
        



main_processing = MainProcessing()

def main():

    process_socket = Process(target=main_processing.StartSocket)

    process_socket = process_socket.start()

    

if __name__ == "__main__":
    main()
