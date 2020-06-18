import sys
sys.path.append("..")

import cv2
from socket import socket, AF_INET, SOCK_STREAM
from imutils.video import WebcamVideoStream
from threading import Thread
import numpy as np
import zlib
import struct
from utils import config 

HOST = config.HOST 
PORT = config.VIDEO_PORT

BufferSize = 4096
CHUNK=1024
lnF = 640*480*3
CHANNELS=2
RATE=44100
client = None


def SendFrame():
    cap =cv2.VideoCapture(0)
    while True:
        try:
            _,frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            
            frame = np.array(frame, dtype = np.uint8).reshape(1, lnF)
            jpg_as_text = bytearray(frame)

            databytes = zlib.compress(jpg_as_text, 9)
            length = struct.pack('!I', len(databytes))
            bytesToBeSend = b''
            client.sendall(length)
            # send 5000*chunk at one time
            while len(databytes) > 0:
                if (5000 * CHUNK) <= len(databytes):
                    bytesToBeSend = databytes[:(5000 * CHUNK)]
                    databytes = databytes[(5000 * CHUNK):]
                    client.sendall(bytesToBeSend)
                else:
                    bytesToBeSend = databytes
                    client.sendall(bytesToBeSend)
                    databytes = b''
            cv2.waitKey(1)
                
        except:
            continue


def RecieveFrame():
    while True:
        try:
            lengthbuf = recvallVideo(4)
            length, = struct.unpack('!I', lengthbuf)
            databytes = recvallVideo(length)
            img = zlib.decompress(databytes)
            if len(databytes) == length:
                
                img = np.array(list(img))
                #np.reshape(img, (480, 640, 3))
                img = np.array(img, dtype = np.uint8).reshape(480, 640, 3)
                cv2.imshow("Stream", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Data CORRUPTED")
        except:
            continue


def recvallVideo(size):
    databytes = b''
    while len(databytes) != size:
        to_read = size - len(databytes)
        if to_read > (5000 * CHUNK):
            databytes += client.recv(5000 * CHUNK)
        else:
            databytes += client.recv(to_read)
    return databytes

def StartVideoCall():
    global client
    client = socket(family=AF_INET, type=SOCK_STREAM)
    client.connect((HOST, PORT))
    

    initiation = client.recv(5).decode()

    if initiation == "start":
        RecieveFrameThread = Thread(target=RecieveFrame).start()
        SendFrameThread = Thread(target=SendFrame).start()
