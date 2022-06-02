import pyudev
import os
import time
from websocket import create_connection
from builderProtocole import BuilderProtocole, ConnectionBuilderProtocole
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')
#ws = create_connection("ws://localhost:8000")
#print("**USB**  => "+ws.recv())
for device in iter(monitor.poll, None):
    print("**USB**  => "+str(device.action))
    if device.action == 'add':
        print('<BLOCK INFORMATION>')
        print('Device name: %s' % device.get('DEVNAME'))
        print('Device type: %s' % device.get('DEVTYPE'))
        print('Bus system: %s' % device.get('ID_BUS'))
        print('Partition label: %s' % device.get('ID_FS_LABEL'))
        print('FS: %s' % device.get('ID_FS_SYSTEM_ID'))
        print('FS type: %s' % device.get('ID_FS_TYPE'))
        print('Device usage: %s' % device.get('ID_FS_USAGE'))
        print('Device model: %s' % device.get('ID_MODEL'))
        print('Partition type: %s' % device.get('ID_PART_TABLE_TYPE'))
        print('USB driver: %s' % device.get('ID_USB_DRIVER'))
        print('Path id: %s' % device.get('ID_PATH'))
        print('</BLOCK INFORMATION>')
        while not len(os.listdir("/media/pi/")):
            time.sleep(1)
            print(str(os.listdir("/media/pi/")))
        time.sleep(1)
        print(str(os.listdir("/media/pi/")))
        print(str(os.listdir("/media/pi/"+os.listdir("/media/pi/")[0]+"/audios")))
        print("**USB**  => "+"path : "+"/media/pi/"+os.listdir("/media/pi/")[0]+"/audios"+" | name : "+os.listdir("/media/pi/")[0]+"| connected")
        #ws.send(BuilderProtocole("usb",device.get('DEVNAME'),[["connected",True],["path",device.get('DEVPATH')]]).build())