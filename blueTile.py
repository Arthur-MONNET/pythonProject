from __future__ import print_function
from websocket import create_connection
from builderProtocole import BuilderProtocole
import sys
import os
import time
from abc import abstractmethod

from blue_st_sdk.manager import Manager
from blue_st_sdk.manager import ManagerListener
from blue_st_sdk.node import NodeListener
from blue_st_sdk.feature import FeatureListener
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm import FeatureAudioADPCM
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm_sync import FeatureAudioADPCMSync

# PRECONDITIONS
#
# In case you want to modify the SDK, clone the repository and add the location
# of the "BlueSTSDK_Python" folder to the "PYTHONPATH" environment variable.
#
# On Linux:
#   export PYTHONPATH=/home/<user>/BlueSTSDK_Python
"""
sudo python blueTile.py BCN-727 5
"""

# CONSTANTS
ws = create_connection("ws://localhost:8000")
initX = 0
initY = 0
initZ = 0
sensibility = 100
pos = "None"
initBool = 1
double = False
stSensorName = sys.argv[1]
stSensorPropsStr = sys.argv[2].split(",")
stSensorProps = list(map(int, stSensorPropsStr))
# Bluetooth Scanning time in seconds (optional).
SCANNING_TIME_s = 5
print(ws.recv)
# Number of notifications to get before disabling them.
NOTIFICATIONS = 1


# INTERFACES

#
# Implementation of the interface used by the Manager class to notify that a new
# node has been discovered or that the scanning starts/stops.
#
class MyManagerListener(ManagerListener):

    #
    # This method is called whenever a discovery process starts or stops.
    #
    # @param manager Manager instance that starts/stops the process.
    # @param enabled True if a new discovery starts, False otherwise.
    #
    def on_discovery_change(self, manager, enabled):
        #print("**BLUETILE**  => "+'Discovery %s.' % ('started' if enabled else 'stopped'))
        if not enabled:
            #print("**BLUETILE**  => "+)
            pass

    #
    # This method is called whenever a new node is discovered.
    #
    # @param manager Manager instance that discovers the node.
    # @param node    New node discovered.
    #
    def on_node_discovered(self, manager, node):
         #print("**BLUETILE**  => "+'New device discovered: %s.' % (node.get_name()))
        pass


#
# Implementation of the interface used by the Node class to notify that a node
# has updated its status.
#
class MyNodeListener(NodeListener):
    pass
    def on_connect(self, node):
        pass
        #print("**BLUETILE**  => "+'Device %s connected.' % (node.get_name()))
    def on_disconnect(self, node, unexpected=False):
        global double
        print('**BLUETILE**  => Device %s disconnected%s.' % (node.get_name(), ' unexpectedly' if unexpected else ''))
        if unexpected and not double:
            # Exiting.
            double = True
            main(sys.argv[1:])
            time.sleep(1)
            double = False
class MyFeatureListener(FeatureListener):
    _notifications = 0
    """Counting notifications to print only the desired ones."""

    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        global initBool,initX,initY,initZ,pos
        if self._notifications < NOTIFICATIONS:
            self._notifications += 1
            #print("**BLUETILE**  => "+feature)
            x = sample.get_data()[0]
            y = sample.get_data()[1]
            z = sample.get_data()[2]
            if(initBool==2):
                initX = x
                initY = y
                initZ = z
                print("**BLUETILE**  => "+'x : '+str(x)+'|y : '+str(y)+'|z : '+str(z))
            if(y < initY-sensibility):
                if pos != "right":
                    pos = "right"
                    ws.send(BuilderProtocole("blueTile",sys.argv[1],[["pos","right"]]).build())
                    time.sleep(2)
            elif(y > initY+sensibility):
                if pos != "left":
                    pos = "left"
                    ws.send(BuilderProtocole("blueTile",sys.argv[1],[["pos","left"]]).build())
                    time.sleep(2)
            elif(x < initX-sensibility):
                if pos != "bottom":
                    pos = "bottom"
                    ws.send(BuilderProtocole("blueTile",sys.argv[1],[["pos","bottom"]]).build())
                    time.sleep(2)
            elif(x > initX+sensibility):
                if pos != "top":
                    pos = "top"
                    ws.send(BuilderProtocole("blueTile",sys.argv[1],[["pos","top"]]).build())
                    time.sleep(2)
            initBool+=1
            #print("**BLUETILE**  => "+sample.get_data()[0]+sample.get_data()[0])
            #ws.send(BuilderProtocole("blueTile",[sample.get_description()[0].get_name()+">"+str(sample.get_data()[0])]).build())


# MAIN APPLICATION

#
# Main application.
#
def main(argv):
    
    #print("**BLUETILE**  => "+ws.recv())
    try:
        # Creating Bluetooth Manager.
        manager = Manager.instance()
        manager_listener = MyManagerListener()
        manager.add_listener(manager_listener)

        while True:
            # Synchronous discovery of Bluetooth devices.
            #print("**BLUETILE**  => "+'Scanning Bluetooth devices...\n')
            manager.discover(SCANNING_TIME_s)

            # Alternative 1: Asynchronous discovery of Bluetooth devices.
            # manager.discover(SCANNING_TIME_s, True)

            # Alternative 2: Asynchronous discovery of Bluetooth devices.
            # manager.start_discovery()
            # time.sleep(SCANNING_TIME_s)
            # manager.stop_discovery()

            # Getting discovered devices.
            discovered_devices = manager.get_nodes()

            # Listing discovered devices.
            if not discovered_devices:
                #print("**BLUETILE**  => "+'No Bluetooth devices found.\n')
                continue
            #print("**BLUETILE**  => "+'Available Bluetooth devices:')
            i = 1
            # Selecting a device.

            indexOfDevice = 0

            for i, device in enumerate(discovered_devices):
                if device.get_name() == stSensorName:
                    indexOfDevice = i

            device = discovered_devices[indexOfDevice]
            node_listener = MyNodeListener()
            device.add_listener(node_listener)

            # Connecting to the device.
            #print("**BLUETILE**  => "+'Connecting to %s...' % (device.get_name()))
            if not device.connect():
                #print("**BLUETILE**  => "+'Connection failed.\n')
                continue

            while True:
                # Getting features.
                features = device.get_features()
                i = 1
                """for feature in features:
                    if isinstance(feature, FeatureAudioADPCM):
                        audio_feature = feature
                        print("**BLUETILE**  => "+'%d,%d) %s' % (i, i + 1, "Audio & Sync"))
                        i += 1
                    elif isinstance(feature, FeatureAudioADPCMSync):
                        audio_sync_feature = feature
                    else:
                        print("**BLUETILE**  => "+'%d) %s' % (i, feature.get_name()))
                        i += 1"""

                # Selecting a feature.

                for i in stSensorProps:
                    feature = features[i]
                    # Enabling notifications.
                    feature_listener = MyFeatureListener()
                    feature.add_listener(feature_listener)
                    device.enable_notifications(feature)

                    # Handling audio case (both audio features have to be enabled).
                    if isinstance(feature, FeatureAudioADPCM):
                        audio_sync_feature_listener = MyFeatureListener()
                        audio_sync_feature.add_listener(audio_sync_feature_listener)
                        device.enable_notifications(audio_sync_feature)
                    elif isinstance(feature, FeatureAudioADPCMSync):
                        audio_feature_listener = MyFeatureListener()
                        audio_feature.add_listener(audio_feature_listener)
                        device.enable_notifications(audio_feature)

                    # Getting notifications.
                    notifications = 0
                    while notifications < NOTIFICATIONS:
                        if device.wait_for_notifications(0.05):
                            notifications += 1

                    # Disabling notifications.
                    device.disable_notifications(feature)
                    feature.remove_listener(feature_listener)

                    # Handling audio case (both audio features have to be disabled).
                    if isinstance(feature, FeatureAudioADPCM):
                        device.disable_notifications(audio_sync_feature)
                        audio_sync_feature.remove_listener(audio_sync_feature_listener)
                    elif isinstance(feature, FeatureAudioADPCMSync):
                        device.disable_notifications(audio_feature)
                        audio_feature.remove_listener(audio_feature_listener)

    except KeyboardInterrupt:
        try:
            #ws.close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])

