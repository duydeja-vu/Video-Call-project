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


HOST = config.HOST 
PORT = config.VIDEO_PORT
lnF = 640*480*3
CHUNK = 1024
addresses = {}
threads = {}
server = None

class MainProcessing(object):
    def __init__(self):
        #self.queue_gui_socket = Queue()
        self.addresses = {}
        self.threads = {}
        self.user_online = []
        self.count_chat_room = 0
        self.main_socket = None
        self.video_socket = None

    def Connections(self):
        while True:
            try:
                client, addr = self.video_socket.accept()
                print("{} is connected!!".format(addr))
                addresses[client] = addr
                if len(addresses) > 1:
                    for sockets in addresses:
                        if sockets not in threads:
                            threads[sockets] = True
                            sockets.send(("start").encode())
                            Thread(target=self.ClientConnection, args=(sockets, )).start()
                else:
                    continue
            except:
                continue

    def ClientConnection(self, client):
      
        while True:
            try:
                lengthbuf = self.recvall(client, 4)
                length, = struct.unpack('!I', lengthbuf)
                self.recvall(client, length)
            except:
                continue

    def broadcast(self, clientSocket, data_to_be_sent):
        for client in addresses:
            if client != clientSocket:
                client.sendall(data_to_be_sent)

    def recvall(self, client, BufferSize):
            databytes = b''
            i = 0
            while i != BufferSize:
                to_read = BufferSize - i
                if to_read > (1000 * CHUNK):
                    databytes = client.recv(1000 * CHUNK)
                    i += len(databytes)
                    self.broadcast(client, databytes)
                else:
                    if BufferSize == 4:
                        databytes += client.recv(to_read)
                    else:
                        databytes = client.recv(to_read)
                    i += len(databytes)
                    if BufferSize != 4:
                        self.broadcast(client, databytes)
    
            if BufferSize == 4:
                self.broadcast(client, databytes)
                return databytes

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
    
        
       

    def StartVideoSocket(self):
        self.video_socket = socket(family=AF_INET, type=SOCK_STREAM)
        self.video_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            
            self.video_socket.bind((config.HOST, config.VIDEO_PORT))
        except OSError:
            print("Can't bind video socket")
            exit(0)
        self.video_socket.listen(10)
        print("Video Socket Waiting for connection..")
        AcceptThread = Thread(target=self.Connections)
        AcceptThread.start()
        AcceptThread.join()
        self.video_socket.close()
        


    def StartMainSocket(self):
        self.main_socket = socket(family=AF_INET, type=SOCK_STREAM)
        self.main_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            
            self.main_socket.bind((config.HOST, config.MAIN_PORT))
        except OSError:
            print("Can't bind main socket")
            exit(0)

        self.main_socket.listen(10)

        print("Main Socket Waiting for connection..")
        while True: 
            client_socket, client_addr = self.main_socket.accept()
            while True:
                mess = client_socket.recv(config.BUFFSIZE)
                user_data = mess.decode('utf-8')
                user_data = eval(user_data)
                if len(user_data) != 0:
                    server_response = self.VerifyUserAccount(user_data)
                    client_socket.send(server_response.encode('utf-8'))
                    print("Server respone", server_response)
                    if server_response == "200_OK":
                        self.user_online.append(user_data[1])
                        print(self.user_online)
                        print("LOGIN SUCCESS !")
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
    process_main_socket = Process(target=main_processing.StartMainSocket)
    process_video_socket = Process(target=main_processing.StartVideoSocket)
    process_main_socket.start()
    process_video_socket.start()

main()
