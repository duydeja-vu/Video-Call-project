from socket import *
import cv2
import numpy as np
from multiprocessing import Process, Queue
import os
import config
import pickle

class Client(object):
    def __init__(self):
        self.username = None
        self.password = None
        self.queue_GUI_SOCKET = Queue()

    def StartGUI(self):
        # Create GUI object
        pass

    def StartSocket(self):
        client_main = socket(family=AF_INET, type=SOCK_STREAM)
        client_main.connect((config.HOST, config.MAIN_PORT))

        if self.queue_GUI_SOCKET.qsize() != 0:
            client_data = self.queue_GUI_SOCKET.get()



    def StartVideoCall(self):
        pass

client = Client()

def main():
    process_gui = Process(target=client.StartGUI)
    process_socket = Process(target=client.StartSocket)

    process_gui.start()
    process_socket = process_socket.start()

    while process_gui.is_alive() == True:
        continue
    my_pid = os.getpid()
    os.system("pkill -P {0}".format(my_pid))




        