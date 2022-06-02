from simple_websocket_server import WebSocketServer, WebSocket
from decoderProtocole import DecoderProtocole, ConnectionDecoderProtocole

print("**SERVER**  => "+"start")
#sudo python blueTile.py BCN-727 5
#python button.py play 14
#python button.py onoff 15

import os
import subprocess
import pygame
from abc import ABC, abstractmethod
pygame.init()
pygame.mixer.init()
stepper = 0
work = False
blueTileBool = True
class PL :
    pass

PL.souvenir = ""
PL.pBottom = []
PL.pLeft = []
PL.pRight = []
PL.pTop = []
PL.pPlaylist = []
pathKey = "./audios/"

def setPlaylist():
    global PL
    PL.bottom = os.listdir( pathKey + "bottom")
    PL.left = os.listdir(pathKey + "left")
    PL.right = os.listdir(pathKey + "right")
    PL.top = os.listdir(pathKey + "top")
    PL.playlist = os.listdir(pathKey + "playlist")
    PL.souvenir = os.listdir(pathKey + "souvenir")
    print("**SERVER**  => "+str(PL.bottom))
    print("**SERVER**  => "+str(PL.left))
    print("**SERVER**  => "+str(PL.right))
    print("**SERVER**  => "+str(PL.top))
    print("**SERVER**  => "+str(PL.playlist))
    print("**SERVER**  => "+str(PL.souvenir))
#setPlaylist()
i=0

controlSound = "start"
#subprocess.call(["sudo","node","puck.js","image1","170f"])
#context = Context()
class SimpleEcho(WebSocket):
    def handle(self):
        global controlSound, stepper, work, blueTileBool
        print("**SERVER**  => "+self.data)
        split = self.data.split(":")
        if(split[0] == "connection"):
            data = ConnectionDecoderProtocole(self.data)
        else:
            data = DecoderProtocole(self.data)
            data.decodeData()
            print("**SERVER**  => "+data.typeVal)
            if data.typeVal == 'blueTile' and work :
                blueTileBool = True
                print("**SERVER**  => "+data.keyValues[0][1])
                pygame.mixer.music.load(pathKey + data.keyValues[0][1] + "/" + getattr(PL, data.keyValues[0][1])[0])
                print("**SERVER**  => "+"Playing:",pathKey + data.keyValues[0][1] + "/" + getattr(PL, data.keyValues[0][1])[0])
                pygame.mixer.music.play()
                controlSound = "pause"
                print("**SERVER**  => "+"end")
                for num, song in enumerate(getattr(PL, data.keyValues[0][1])):
                    if num == 0:
                        continue # already playing
                    pygame.mixer.music.queue(pathKey + data.keyValues[0][1] + "/" + song)
                print("**SERVER**  => "+"end2")

            if data.typeVal == 'button' and data.name == "play" and work and blueTileBool:
                print("**SERVER**  => "+"button press")
                if data.keyValues[0][1] == "True":
                    print("**SERVER**  => "+"button press : ", str(pygame.mixer.music.get_busy()))
                    if pygame.mixer.music.get_busy() == 0:
                        pygame.mixer.music.load(pathKey + 'playlist' + "/" + getattr(PL, 'playlist')[0])
                        print("**SERVER**  => "+"Playing:" + pathKey + 'playlist' + "/" + getattr(PL, 'playlist')[0])
                        pygame.mixer.music.play()
                        controlSound = "pause"
                        print("**SERVER**  => "+"end")
                        for num, song in enumerate(getattr(PL, 'playlist')):
                            if num == 0:
                                continue # already playing
                            pygame.mixer.music.queue(pathKey + 'playlist' + "/" + song)
                        print("**SERVER**  => "+"end2")
                    else :
                        print("**SERVER**  => "+controlSound)
                        if controlSound == "pause":
                            pygame.mixer.music.pause()
                            controlSound = "play"
                        elif controlSound == "play" :
                            pygame.mixer.music.unpause()
                            controlSound = "pause"
                            
            if data.typeVal == 'button' and data.name == "onoff":
                if data.keyValues[0][1] == "True":
                    if work :
                        work = False
                        pygame.mixer.music.stop()
                    else :
                        work = True
                
            self.send_message(self.data)

    def connected(self):
        #self.send_message('connected')
        print("**SERVER**  ")#=> "+self.address, 'connected')
        

    def handle_close(self):
        print("**SERVER** ")# => "+self.address, 'closed')
        
     
server = WebSocketServer('', 8000, SimpleEcho)
print("**SERVER**  => "+"server online")
server.serve_forever()