import sys
sys.path.append("..")

from socket import socket, AF_INET, SOCK_STREAM
from socket import *
from threading import Thread
import struct
from utils import config


addressesAudio = {}
addresses = {}
threads = {}

def ConnectionsVideo():
    while True:
        try:
            clientVideo, addr = serverVideo.accept()
            print("{} is connected!!".format(addr))
            addresses[clientVideo] = addr
            if len(addresses) > 1:
                for sockets in addresses:
                    if sockets not in threads:
                        threads[sockets] = True
                        sockets.send(("start").encode())
                        Thread(target=ClientConnectionVideo, args=(sockets, )).start()
            else:
                continue
        except:
            continue

def ConnectionsSound():
    while True:
        try:
            clientAudio, addr = serverAudio.accept()
            print("{} is connected!!".format(addr))
            addressesAudio[clientAudio] = addr
            Thread(target=ClientConnectionSound, args=(clientAudio, )).start()
        except:
            continue

def ClientConnectionVideo(clientVideo):
    while True:
        try:
            lengthbuf = recvall(clientVideo, 4)
            length, = struct.unpack('!I', lengthbuf)
            recvall(clientVideo, length)
        except:
            continue

def ClientConnectionSound(clientAudio):
    while True:
        try:
            data = clientAudio.recv(BufferSize)
            broadcastSound(clientAudio, data)
        except:
            continue

def recvall(clientVideo, BufferSize):
        databytes = b''
        i = 0
        while i != BufferSize:
            to_read = BufferSize - i
            if to_read > (1000 * config.CHUNK):
                databytes = clientVideo.recv(1000 * config.CHUNK)
                i += len(databytes)
                broadcastVideo(clientVideo, databytes)
            else:
                if BufferSize == 4:
                    databytes += clientVideo.recv(to_read)
                else:
                    databytes = clientVideo.recv(to_read)
                i += len(databytes)
                if BufferSize != 4:
                    broadcastVideo(clientVideo, databytes)
        print("YES!!!!!!!!!" if i == BufferSize else "NO!!!!!!!!!!!!")
        if BufferSize == 4:
            broadcastVideo(clientVideo, databytes)
            return databytes

def broadcastVideo(clientSocket, data_to_be_sent):
    for clientVideo in addresses:
        if clientVideo != clientSocket:
            clientVideo.sendall(data_to_be_sent)

def broadcastSound(clientSocket, data_to_be_sent):
    for clientAudio in addressesAudio:
        if clientAudio != clientSocket:
            clientAudio.sendall(data_to_be_sent)

serverVideo = None
serverAudio = None

def HandleCallSession():
    global serverAudio, serverVideo
    serverVideo = socket(family=AF_INET, type=SOCK_STREAM)
    print(serverVideo)
    serverVideo.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try:
        serverVideo.bind((config.HOST, config.VIDEO_PORT))
    except OSError:
        print("Server Busy")
        exit(0)
    serverVideo.listen(10)


    serverAudio = socket(family=AF_INET, type=SOCK_STREAM)
    serverAudio.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try:
        serverAudio.bind((config.HOST, config.AUDIO_PORT))
    except OSError:
        print("Server Busy")
        exit(0)

    serverAudio.listen(10)
    print("Waiting for connection..")
    AcceptThreadAudio = Thread(target=ConnectionsSound)
    AcceptThreadAudio.start()


    serverVideo.listen(2)
    print("Waiting for connection..")
    AcceptThreadVideo = Thread(target=ConnectionsVideo)
    AcceptThreadVideo.start()
    AcceptThreadVideo.join()
    serverVideo.close()

#HandleCallSession()
