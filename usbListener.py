import pyudev
import os
import time
from websocket import create_connection
from builderProtocole import BuilderProtocole, ConnectionBuilderProtocole
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')
ws = create_connection("ws://localhost:8000")
print("**USB**  => "+str(ws.recv()))
for device in iter(monitor.poll, None):
    print("**USB**  => "+str(device.action))
    if device.action == 'add':
        while not len(os.listdir("/media/pi/")):
            time.sleep(1)
        time.sleep(1)
        print(str(os.listdir("/media/pi/")))
        if(len(os.listdir("/media/pi/"))):
            print(str(os.listdir("/media/pi/"+os.listdir("/media/pi/")[0]+"/audios")))
            print("**USB**  => "+"path : "+"/media/pi/"+os.listdir("/media/pi/")[0]+"/audios/"+" | name : "+os.listdir("/media/pi/")[0]+" | connected")
            ws.send(BuilderProtocole("usb",os.listdir("/media/pi/")[0],[["connected",True],["path","/media/pi/"+os.listdir("/media/pi/")[0]+"/audios/"]]).build())
    elif device.action == 'remove':
        ws.send(BuilderProtocole("usb","None",[["connected",False]]).build())