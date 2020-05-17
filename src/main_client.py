from socket import *
import cv2
import numpy as np
from multiprocessing import Process, Queue
import os
import config

class Client(object):
    def __init__(self):
        self.username = None
        self.password = None
        self.queue_GUI_SOCKET = Queue()

    def StartGUI(self):
        pass

    def StartSocket(self):
        client_main = socket(family=AF_INET, type=SOCK_STREAM)
        client_main.connect((config.HOST, config.MAIN_PORT))

    def StartVideoCall(self):
        pass

        