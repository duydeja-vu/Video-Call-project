import sys
sys.path.append("..")

from MainWindow.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import time
from multiprocessing import Process, Queue
import os
import signal
from socket import *
import config
from threading import Thread




class MainProcessing(object):
    def __init__(self):
        #self.queue_gui_socket = Queue()
        self.client_address = []

    def StartGui(self):
        pass

    # Accept connection to main socket.
    # Receive buffer that contain client's username and password
    # Call database and verify client account
    # If match, reply "200_OK" to client, else, reply "500_NOTOK" to client
    def VerifyClientAccount(self):
        pass

    # If client receive "200_OK", who will connect to server's sound socket and video socket and start video call.
    # Two method below handle that.
    def ConnectionsSound(self):
        pass

    
    def ConnectionsVideo(self):
        pass

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
        verify_client_account = Thread(target=self.VerifyClientAccount)
        verify_client_account.start()

        server_audio.listen(2)
        print("Waiting for connection..")
        thread_audio = Thread(target=self.ConnectionsSound)
        thread_audio.start()

        server_video.listen(2)
        print("Waiting for connection..")
        thread_video = Thread(target=self.ConnectionsVideo)
        thread_video.start()


main_processing = MainProcessing()

def main():

    process_gui = Process(target=main_processing.StartGui)
    process_socket = Process(target=main_processing.StartSocket)

    process_gui.start()
    process_socket = process_socket.start()

    while process_gui.is_alive() == True:
        continue
    
    my_pid = os.getpid()
    os.system("pkill -P {0}".format(my_pid))
